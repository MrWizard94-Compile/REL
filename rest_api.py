"""
REL REST API layer.

Provides:
- FastAPI server with OpenAPI docs
- REST endpoints for all REL tools
- OAuth2 token auth + API key auth
- Rate limiting and CORS
- Request/response logging
- Analytics, plugin, collaboration, and realtime notifications APIs
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import re
import secrets
import threading
import time
from collections import defaultdict, deque
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Sequence, Set, Tuple
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

import mcp_server
from analytics_engine import generate_advanced_analytics
from plugin_system import PluginManager


logger = logging.getLogger("REL_API")

API_PREFIX = "/api/v1"
DATA_PATH = mcp_server.DATA_PATH

AUTH_REQUIRED = os.environ.get("REL_API_AUTH_REQUIRED", "true").lower() in {"1", "true", "yes"}
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REL_ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
RATE_LIMIT_PER_MINUTE = int(os.environ.get("REL_API_RATE_LIMIT_PER_MINUTE", "180"))
LOGIN_RATE_LIMIT_PER_MINUTE = int(os.environ.get("REL_API_LOGIN_RATE_LIMIT_PER_MINUTE", "12"))
RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("REL_API_RATE_LIMIT_WINDOW_SECONDS", "60"))

_oauth2_secret_raw = os.environ.get("REL_OAUTH2_SECRET", "").strip()
if _oauth2_secret_raw:
    OAUTH2_SECRET = _oauth2_secret_raw.encode("utf-8")
else:
    generated = secrets.token_urlsafe(48)
    OAUTH2_SECRET = generated.encode("utf-8")
    logger.warning(
        "REL_OAUTH2_SECRET is not set; generated an ephemeral secret for this process. "
        "Set REL_OAUTH2_SECRET in persistent environments."
    )

DEFAULT_ADMIN_USERNAME = os.environ.get("REL_ADMIN_USERNAME", "admin").strip() or "admin"
_default_admin_password_env = os.environ.get("REL_ADMIN_PASSWORD", "").strip()
if _default_admin_password_env:
    DEFAULT_ADMIN_PASSWORD = _default_admin_password_env
else:
    DEFAULT_ADMIN_PASSWORD = secrets.token_urlsafe(24)
    logger.warning(
        "REL_ADMIN_PASSWORD is not set; generated an ephemeral bootstrap admin password. "
        "Set REL_ADMIN_PASSWORD before startup in persistent environments."
    )


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _hash_value(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _json_read(path: Path, default: Dict[str, Any]) -> Dict[str, Any]:
    try:
        if not path.exists():
            return default
        raw = json.loads(path.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else default
    except Exception:
        return default


def _json_write(path: Path, payload: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _password_hash(password: str, salt: str) -> str:
    derived = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120_000,
    )
    return base64.urlsafe_b64encode(derived).decode("utf-8")


def _encode_token(payload: Dict[str, Any]) -> str:
    payload_bytes = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    body = base64.urlsafe_b64encode(payload_bytes).decode("utf-8").rstrip("=")
    signature = hmac.new(OAUTH2_SECRET, body.encode("utf-8"), hashlib.sha256).hexdigest()
    return f"{body}.{signature}"


def _decode_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        body, signature = token.split(".", 1)
    except ValueError:
        return None
    expected = hmac.new(OAUTH2_SECRET, body.encode("utf-8"), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return None
    padded = body + "=" * (-len(body) % 4)
    try:
        payload = json.loads(base64.urlsafe_b64decode(padded.encode("utf-8")).decode("utf-8"))
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None
    exp = payload.get("exp")
    if not isinstance(exp, int):
        return None
    if _utc_now().timestamp() > exp:
        return None
    return payload


class UserStore:
    """Simple JSON-backed user store for OAuth2 and RBAC."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()
        self._ensure_seed_admin()

    def _default_data(self) -> Dict[str, Any]:
        return {"users": {}}

    def _load(self) -> Dict[str, Any]:
        return _json_read(self.path, self._default_data())

    def _save(self, payload: Dict[str, Any]) -> None:
        _json_write(self.path, payload)

    def _ensure_seed_admin(self) -> None:
        admin_user = os.environ.get("REL_ADMIN_USERNAME", DEFAULT_ADMIN_USERNAME).strip() or DEFAULT_ADMIN_USERNAME
        admin_password = (
            os.environ.get("REL_ADMIN_PASSWORD", DEFAULT_ADMIN_PASSWORD).strip() or DEFAULT_ADMIN_PASSWORD
        )
        with self._lock:
            data = self._load()
            if any(user.get("role") == "admin" for user in data.get("users", {}).values()):
                return
            user_id = f"user_{uuid4().hex[:12]}"
            salt = secrets.token_hex(16)
            data.setdefault("users", {})[user_id] = {
                "id": user_id,
                "username": admin_user,
                "password_hash": _password_hash(admin_password, salt),
                "salt": salt,
                "role": "admin",
                "active": True,
                "created_at": _utc_now().isoformat(),
            }
            self._save(data)

    def create_user(self, username: str, password: str, role: str = "member") -> Dict[str, Any]:
        with self._lock:
            data = self._load()
            users = data.setdefault("users", {})
            lowered = username.strip().lower()
            if any(str(user.get("username", "")).lower() == lowered for user in users.values()):
                raise ValueError(f"Username already exists: {username}")
            user_id = f"user_{uuid4().hex[:12]}"
            salt = secrets.token_hex(16)
            users[user_id] = {
                "id": user_id,
                "username": username.strip(),
                "password_hash": _password_hash(password, salt),
                "salt": salt,
                "role": role,
                "active": True,
                "created_at": _utc_now().isoformat(),
            }
            self._save(data)
            return self._public_view(users[user_id])

    def list_users(self) -> List[Dict[str, Any]]:
        data = self._load()
        return [self._public_view(user) for user in data.get("users", {}).values()]

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        data = self._load()
        record = data.get("users", {}).get(user_id)
        if record is None:
            return None
        return self._public_view(record)

    def authenticate(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        data = self._load()
        users = data.get("users", {})
        for user in users.values():
            if str(user.get("username", "")).lower() != username.strip().lower():
                continue
            if not user.get("active", True):
                return None
            salt = str(user.get("salt", ""))
            if _password_hash(password, salt) == user.get("password_hash"):
                return self._public_view(user)
            return None
        return None

    @staticmethod
    def _public_view(user: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": user.get("id"),
            "username": user.get("username"),
            "role": user.get("role", "member"),
            "active": bool(user.get("active", True)),
            "created_at": user.get("created_at"),
        }


class APIKeyStore:
    """JSON-backed API key manager."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()

    def _default_data(self) -> Dict[str, Any]:
        return {"keys": {}}

    def _load(self) -> Dict[str, Any]:
        return _json_read(self.path, self._default_data())

    def _save(self, payload: Dict[str, Any]) -> None:
        _json_write(self.path, payload)

    def create_key(self, name: str, role: str, created_by: str) -> Dict[str, Any]:
        raw_key = f"rel_{secrets.token_urlsafe(32)}"
        record_id = f"key_{uuid4().hex[:12]}"
        now = _utc_now().isoformat()
        record = {
            "id": record_id,
            "name": name,
            "role": role,
            "key_hash": _hash_value(raw_key),
            "prefix": raw_key[:12],
            "created_by": created_by,
            "created_at": now,
            "last_used_at": None,
            "revoked": False,
            "revoked_at": None,
        }
        with self._lock:
            data = self._load()
            data.setdefault("keys", {})[record_id] = record
            self._save(data)
        return {"api_key": raw_key, "record": self._public_view(record)}

    def list_keys(self, include_revoked: bool = False) -> List[Dict[str, Any]]:
        data = self._load()
        items = []
        for record in data.get("keys", {}).values():
            if not include_revoked and record.get("revoked"):
                continue
            items.append(self._public_view(record))
        return items

    def revoke(self, key_id: str) -> bool:
        with self._lock:
            data = self._load()
            record = data.get("keys", {}).get(key_id)
            if record is None:
                return False
            record["revoked"] = True
            record["revoked_at"] = _utc_now().isoformat()
            self._save(data)
        return True

    def authenticate(self, raw_key: str) -> Optional[Dict[str, Any]]:
        if not raw_key:
            return None
        target = _hash_value(raw_key)
        with self._lock:
            data = self._load()
            for record in data.get("keys", {}).values():
                if record.get("revoked"):
                    continue
                if hmac.compare_digest(str(record.get("key_hash")), target):
                    record["last_used_at"] = _utc_now().isoformat()
                    self._save(data)
                    return self._public_view(record)
        return None

    @staticmethod
    def _public_view(record: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": record.get("id"),
            "name": record.get("name"),
            "role": record.get("role", "service"),
            "prefix": record.get("prefix"),
            "created_by": record.get("created_by"),
            "created_at": record.get("created_at"),
            "last_used_at": record.get("last_used_at"),
            "revoked": bool(record.get("revoked", False)),
            "revoked_at": record.get("revoked_at"),
        }


class SlidingWindowRateLimiter:
    """In-memory per-identity rate limiter."""

    def __init__(self, limit: int, window_seconds: int) -> None:
        self.limit = max(limit, 1)
        self.window_seconds = max(window_seconds, 1)
        self._events: Dict[str, Deque[float]] = defaultdict(deque)
        self._lock = threading.Lock()

    def consume(self, identity: str) -> Tuple[bool, int, int]:
        now = time.time()
        with self._lock:
            events = self._events[identity]
            cutoff = now - self.window_seconds
            while events and events[0] <= cutoff:
                events.popleft()
            if len(events) >= self.limit:
                retry_after = int(max((events[0] + self.window_seconds) - now, 0)) + 1
                return False, self.limit, retry_after
            events.append(now)
            remaining = max(self.limit - len(events), 0)
            return True, remaining, self.window_seconds


class CollaborationStore:
    """Shared project membership, comments, activity, and preferences."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()

    def _default_data(self) -> Dict[str, Any]:
        return {
            "project_members": {},
            "comments": {},
            "activity": [],
            "notification_preferences": {},
        }

    def _load(self) -> Dict[str, Any]:
        return _json_read(self.path, self._default_data())

    def _save(self, payload: Dict[str, Any]) -> None:
        _json_write(self.path, payload)

    def share_project(self, project_key: str, user_id: str, role: str, shared_by: str) -> Dict[str, Any]:
        with self._lock:
            data = self._load()
            members = data.setdefault("project_members", {}).setdefault(project_key, [])
            entry = {
                "user_id": user_id,
                "role": role,
                "shared_by": shared_by,
                "shared_at": _utc_now().isoformat(),
            }
            members = [m for m in members if m.get("user_id") != user_id]
            members.append(entry)
            data["project_members"][project_key] = members
            self._append_activity(
                data,
                "project_shared",
                {
                    "project": project_key,
                    "user_id": user_id,
                    "role": role,
                    "shared_by": shared_by,
                },
            )
            self._save(data)
            return entry

    def get_project_members(self, project_key: str) -> List[Dict[str, Any]]:
        data = self._load()
        return list(data.get("project_members", {}).get(project_key, []))

    def add_comment(self, project_key: str, author_id: str, comment: str) -> Dict[str, Any]:
        with self._lock:
            data = self._load()
            comments = data.setdefault("comments", {}).setdefault(project_key, [])
            item = {
                "id": f"comment_{uuid4().hex[:12]}",
                "project": project_key,
                "author_id": author_id,
                "comment": comment,
                "created_at": _utc_now().isoformat(),
            }
            comments.append(item)
            self._append_activity(
                data,
                "comment_added",
                {
                    "project": project_key,
                    "author_id": author_id,
                    "comment_id": item["id"],
                },
            )
            self._save(data)
            return item

    def get_comments(self, project_key: str) -> List[Dict[str, Any]]:
        data = self._load()
        return list(data.get("comments", {}).get(project_key, []))

    def set_notification_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            data = self._load()
            data.setdefault("notification_preferences", {})[user_id] = preferences
            self._save(data)
        return preferences

    def get_notification_preferences(self, user_id: str) -> Dict[str, Any]:
        data = self._load()
        prefs = data.get("notification_preferences", {}).get(user_id, {})
        return prefs if isinstance(prefs, dict) else {}

    def get_activity(self, limit: int = 100) -> List[Dict[str, Any]]:
        data = self._load()
        activity = data.get("activity", [])
        if not isinstance(activity, list):
            return []
        return activity[-max(limit, 1):]

    @staticmethod
    def _append_activity(data: Dict[str, Any], event_type: str, payload: Dict[str, Any]) -> None:
        data.setdefault("activity", []).append(
            {
                "id": f"act_{uuid4().hex[:12]}",
                "event_type": event_type,
                "payload": payload,
                "created_at": _utc_now().isoformat(),
            }
        )


class NotificationHub:
    """Realtime notifications via WebSocket."""

    def __init__(self) -> None:
        self._connections: Dict[str, Set[WebSocket]] = defaultdict(set)
        self._recent: Deque[Dict[str, Any]] = deque(maxlen=500)
        self._lock = threading.Lock()

    async def connect(self, user_id: str, websocket: WebSocket, subprotocol: Optional[str] = None) -> None:
        await websocket.accept(subprotocol=subprotocol)
        with self._lock:
            self._connections[user_id].add(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket) -> None:
        with self._lock:
            sockets = self._connections.get(user_id)
            if sockets is None:
                return
            sockets.discard(websocket)
            if not sockets:
                self._connections.pop(user_id, None)

    async def publish(
        self,
        event_type: str,
        payload: Dict[str, Any],
        target_users: Optional[Sequence[str]] = None,
    ) -> None:
        event = {
            "id": f"notif_{uuid4().hex[:12]}",
            "event_type": event_type,
            "payload": payload,
            "created_at": _utc_now().isoformat(),
        }
        with self._lock:
            self._recent.append(event)
            user_ids = list(target_users) if target_users is not None else list(self._connections.keys())
            targets = {
                user_id: list(self._connections.get(user_id, set()))
                for user_id in user_ids
            }

        stale: List[Tuple[str, WebSocket]] = []
        for user_id, sockets in targets.items():
            for socket in sockets:
                try:
                    await socket.send_json(event)
                except Exception:
                    stale.append((user_id, socket))

        for user_id, socket in stale:
            self.disconnect(user_id, socket)

    def recent(self, limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            items = list(self._recent)
        return items[-max(limit, 1):]


class Principal(BaseModel):
    subject: str
    role: str
    auth_type: str
    username: Optional[str] = None


class ToolInvocationRequest(BaseModel):
    arguments: Dict[str, Any] = Field(default_factory=dict)


class ToolInvocationResponse(BaseModel):
    tool: str
    success: bool
    result: Any
    invoked_at: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in_seconds: int
    user: Dict[str, Any]


class APIKeyCreateRequest(BaseModel):
    name: str = Field(min_length=2, max_length=64)
    role: str = Field(default="service")


class UserCreateRequest(BaseModel):
    username: str = Field(min_length=3, max_length=64)
    password: str = Field(min_length=8, max_length=128)
    role: str = Field(default="member")


class ProjectShareRequest(BaseModel):
    user_id: str
    role: str = Field(default="member")


class CommentRequest(BaseModel):
    comment: str = Field(min_length=1, max_length=2000)


class NotificationPreferencesRequest(BaseModel):
    websocket: bool = True
    email: bool = False
    slack: bool = False
    digest_hours: int = Field(default=24, ge=1, le=168)
    custom_triggers: List[str] = Field(default_factory=list)


class PluginExecuteRequest(BaseModel):
    payload: Dict[str, Any] = Field(default_factory=dict)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/auth/token", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
TOOL_INVOKE_ROLES: Tuple[str, ...] = ("admin", "manager", "member", "service")
PLUGIN_EXECUTE_ROLES: Tuple[str, ...] = ("admin", "manager")
PROJECT_ACCESS_ROLES: Tuple[str, ...] = ("admin", "manager", "member")

user_store = UserStore(DATA_PATH / "users.json")
api_key_store = APIKeyStore(DATA_PATH / "api_keys.json")
collaboration_store = CollaborationStore(DATA_PATH / "collaboration.json")
notification_hub = NotificationHub()
plugin_manager = PluginManager(mcp_server.REL_PATH / "plugins")
rate_limiter = SlidingWindowRateLimiter(RATE_LIMIT_PER_MINUTE, RATE_LIMIT_WINDOW_SECONDS)
login_rate_limiter = SlidingWindowRateLimiter(LOGIN_RATE_LIMIT_PER_MINUTE, RATE_LIMIT_WINDOW_SECONDS)


def _discover_tool_names() -> List[str]:
    """
    Discover tool names from mcp_server.py.

    This avoids async import-time calls while ensuring endpoint count stays aligned.
    """
    source_path = Path(mcp_server.__file__)
    try:
        source = source_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return []

    names = re.findall(r'Tool\(name="([^"]+)"', source)
    deduped: List[str] = []
    seen: Set[str] = set()
    for name in names:
        if name not in seen:
            seen.add(name)
            deduped.append(name)
    return deduped


TOOL_NAMES = _discover_tool_names()


def _create_access_token(user: Dict[str, Any]) -> Tuple[str, int]:
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire_dt = _utc_now() + expires_delta
    payload = {
        "sub": user["id"],
        "username": user.get("username"),
        "role": user.get("role", "member"),
        "exp": int(expire_dt.timestamp()),
    }
    return _encode_token(payload), int(expires_delta.total_seconds())


async def _publish_event(event_type: str, payload: Dict[str, Any], users: Optional[List[str]] = None) -> None:
    try:
        await notification_hub.publish(event_type, payload, users)
    except Exception:
        logger.exception("Failed to publish event")


def _identity_for_rate_limit(request: Request) -> str:
    api_key_value = request.headers.get("X-API-Key", "")
    if api_key_value:
        return f"api_key:{_hash_value(api_key_value)[:12]}"
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.removeprefix("Bearer ").strip()
        return f"bearer:{_hash_value(token)[:12]}"
    client = request.client.host if request.client else "unknown"
    return f"ip:{client}"


def _extract_websocket_auth_token(websocket: WebSocket) -> Tuple[Optional[str], Optional[str]]:
    requested_protocols = [
        value.strip()
        for value in websocket.headers.get("sec-websocket-protocol", "").split(",")
        if value.strip()
    ]
    selected_subprotocol = "rel-notify" if "rel-notify" in requested_protocols else None

    token: Optional[str] = None

    auth_header = websocket.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        candidate = auth_header.removeprefix("Bearer ").strip()
        if candidate:
            token = candidate

    if token is None:
        for value in requested_protocols:
            if value.startswith("bearer."):
                candidate = value.removeprefix("bearer.").strip()
                if candidate:
                    token = candidate
                    break

    return token, selected_subprotocol


async def get_current_principal(
    token: Optional[str] = Depends(oauth2_scheme),
    api_key: Optional[str] = Depends(api_key_header),
) -> Principal:
    if token:
        payload = _decode_token(token)
        if payload is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token.")
        return Principal(
            subject=str(payload.get("sub")),
            username=str(payload.get("username", "")) or None,
            role=str(payload.get("role", "member")),
            auth_type="oauth2",
        )

    if api_key:
        record = api_key_store.authenticate(api_key)
        if record is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key.")
        return Principal(
            subject=str(record["id"]),
            role=str(record.get("role", "service")),
            auth_type="api_key",
        )

    if AUTH_REQUIRED:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    return Principal(subject="anonymous", role="anonymous", auth_type="none")


def require_roles(allowed: Sequence[str]):
    async def _dependency(principal: Principal = Depends(get_current_principal)) -> Principal:
        if principal.role not in allowed:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role.")
        return principal

    return _dependency


def _load_project_record(project_key: str) -> Dict[str, Any]:
    state = mcp_server.load_state()
    projects = state.get("project_states", {})
    if not isinstance(projects, dict):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    project = projects.get(project_key)
    if not isinstance(project, dict):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found.")
    return project


def _project_member_ids(project_key: str) -> Set[str]:
    member_ids: Set[str] = set()
    for member in collaboration_store.get_project_members(project_key):
        if not isinstance(member, dict):
            continue
        user_id = member.get("user_id")
        if isinstance(user_id, str) and user_id:
            member_ids.add(user_id)
    return member_ids


def _enforce_project_access(project_key: str, principal: Principal) -> None:
    _load_project_record(project_key)
    if principal.role in {"admin", "manager"}:
        return
    if principal.role == "member" and principal.subject in _project_member_ids(project_key):
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Project access denied.")


def _tool_response_to_payload(response_items: List[Any]) -> Any:
    parsed: List[Any] = []
    for item in response_items:
        text = getattr(item, "text", "")
        if not isinstance(text, str):
            parsed.append(text)
            continue
        try:
            parsed.append(json.loads(text))
        except json.JSONDecodeError:
            parsed.append(text)
    if len(parsed) == 1:
        return parsed[0]
    return parsed


async def _invoke_tool(tool_name: str, arguments: Dict[str, Any]) -> ToolInvocationResponse:
    if tool_name not in TOOL_NAMES:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Unknown tool: {tool_name}")

    payload = dict(arguments)
    if mcp_server.AUTH_REQUIRED and mcp_server.AUTH_BEARER_TOKEN and "auth_token" not in payload:
        payload["auth_token"] = mcp_server.AUTH_BEARER_TOKEN

    result_items = await mcp_server.call_tool(tool_name, payload)
    payload_result = _tool_response_to_payload(result_items)

    success = True
    if isinstance(payload_result, dict) and payload_result.get("error"):
        success = False
    return ToolInvocationResponse(
        tool=tool_name,
        success=success,
        result=payload_result,
        invoked_at=_utc_now().isoformat(),
    )


@asynccontextmanager
async def app_lifespan(_: FastAPI):
    plugin_manager.discover_plugins()
    logger.info("REL API startup complete. tool_count=%s", len(TOOL_NAMES))
    yield


app = FastAPI(
    title="REL REST API",
    description="HTTP API for REL cognitive architecture and tool orchestration.",
    version="1.0.0",
    lifespan=app_lifespan,
)

origins_raw = os.environ.get("REL_CORS_ORIGINS", "*")
allow_origins = ["*"] if origins_raw.strip() == "*" else [o.strip() for o in origins_raw.split(",") if o.strip()]
allow_credentials = os.environ.get("REL_CORS_ALLOW_CREDENTIALS", "true").lower() in {"1", "true", "yes"}
if allow_origins == ["*"] and allow_credentials:
    allow_credentials = False
    logger.warning(
        "REL_CORS_ORIGINS='*' with credentials is unsafe. "
        "Disabling credentials; set explicit origins to enable credentialed CORS."
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def logging_and_rate_limit(request: Request, call_next):  # type: ignore[no-untyped-def]
    start = time.perf_counter()
    path = request.url.path
    selected_limiter = rate_limiter
    exempt_paths = {
        "/health",
        "/openapi.json",
        "/docs",
        "/redoc",
    }
    if path.startswith(API_PREFIX) and path not in exempt_paths:
        if path == f"{API_PREFIX}/auth/token":
            selected_limiter = login_rate_limiter
        identity = _identity_for_rate_limit(request)
        allowed, remaining, window_seconds = selected_limiter.consume(identity)
        if not allowed:
            response = JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={"error": "Rate limit exceeded."},
            )
            response.headers["X-RateLimit-Limit"] = str(selected_limiter.limit)
            response.headers["X-RateLimit-Remaining"] = "0"
            response.headers["Retry-After"] = str(window_seconds)
            return response
    else:
        remaining = selected_limiter.limit

    response = await call_next(request)
    response.headers["X-RateLimit-Limit"] = str(selected_limiter.limit)
    response.headers["X-RateLimit-Remaining"] = str(max(remaining, 0))

    latency_ms = (time.perf_counter() - start) * 1000.0
    logger.info(
        json.dumps(
            {
                "event": "http_request",
                "method": request.method,
                "path": path,
                "status": response.status_code,
                "latency_ms": round(latency_ms, 2),
            }
        )
    )
    return response


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "timestamp": _utc_now().isoformat(),
        "tool_count": len(TOOL_NAMES),
    }


@app.post(f"{API_PREFIX}/auth/token", response_model=TokenResponse)
async def issue_token(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    user = user_store.authenticate(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    token, expires_seconds = _create_access_token(user)
    return TokenResponse(access_token=token, expires_in_seconds=expires_seconds, user=user)


@app.get(f"{API_PREFIX}/auth/me")
async def whoami(principal: Principal = Depends(get_current_principal)) -> Dict[str, Any]:
    return principal.model_dump()


@app.post(f"{API_PREFIX}/api-keys")
async def create_api_key(
    request: APIKeyCreateRequest,
    principal: Principal = Depends(require_roles(["admin"])),
) -> Dict[str, Any]:
    created = api_key_store.create_key(request.name, request.role, principal.subject)
    await _publish_event("api_key_created", {"name": request.name, "created_by": principal.subject})
    return created


@app.get(f"{API_PREFIX}/api-keys")
async def list_api_keys(
    include_revoked: bool = False,
    principal: Principal = Depends(require_roles(["admin"])),
) -> Dict[str, Any]:
    return {"keys": api_key_store.list_keys(include_revoked=include_revoked), "requested_by": principal.subject}


@app.delete(f"{API_PREFIX}/api-keys/{{key_id}}")
async def revoke_api_key(
    key_id: str,
    principal: Principal = Depends(require_roles(["admin"])),
) -> Dict[str, Any]:
    revoked = api_key_store.revoke(key_id)
    if not revoked:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API key not found.")
    await _publish_event("api_key_revoked", {"key_id": key_id, "revoked_by": principal.subject})
    return {"revoked": True, "key_id": key_id}


@app.post(f"{API_PREFIX}/users")
async def create_user(
    request: UserCreateRequest,
    principal: Principal = Depends(require_roles(["admin"])),
) -> Dict[str, Any]:
    try:
        created = user_store.create_user(request.username, request.password, request.role)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    await _publish_event("user_created", {"user_id": created["id"], "created_by": principal.subject})
    return created


@app.get(f"{API_PREFIX}/users")
async def list_users(_: Principal = Depends(require_roles(["admin", "manager"]))) -> Dict[str, Any]:
    return {"users": user_store.list_users()}


@app.post(f"{API_PREFIX}/projects/{{project_key}}/share")
async def share_project(
    project_key: str,
    request: ProjectShareRequest,
    principal: Principal = Depends(require_roles(["admin", "manager", "member"])),
) -> Dict[str, Any]:
    _load_project_record(project_key)
    if principal.role == "member":
        _enforce_project_access(project_key, principal)
    member = collaboration_store.share_project(project_key, request.user_id, request.role, principal.subject)
    await _publish_event(
        "project_shared",
        {"project": project_key, "user_id": request.user_id, "role": request.role},
        users=[request.user_id],
    )
    return {"project": project_key, "member": member}


@app.get(f"{API_PREFIX}/projects/{{project_key}}/members")
async def get_project_members(
    project_key: str,
    principal: Principal = Depends(require_roles(PROJECT_ACCESS_ROLES)),
) -> Dict[str, Any]:
    _enforce_project_access(project_key, principal)
    return {"project": project_key, "members": collaboration_store.get_project_members(project_key)}


@app.post(f"{API_PREFIX}/projects/{{project_key}}/comments")
async def add_project_comment(
    project_key: str,
    request: CommentRequest,
    principal: Principal = Depends(require_roles(PROJECT_ACCESS_ROLES)),
) -> Dict[str, Any]:
    _enforce_project_access(project_key, principal)
    comment = collaboration_store.add_comment(project_key, principal.subject, request.comment)
    member_ids = [m.get("user_id") for m in collaboration_store.get_project_members(project_key)]
    target_users = [uid for uid in member_ids if isinstance(uid, str)]
    await _publish_event("project_comment", comment, users=target_users or None)
    return comment


@app.get(f"{API_PREFIX}/projects/{{project_key}}/comments")
async def get_project_comments(
    project_key: str,
    principal: Principal = Depends(require_roles(PROJECT_ACCESS_ROLES)),
) -> Dict[str, Any]:
    _enforce_project_access(project_key, principal)
    return {"project": project_key, "comments": collaboration_store.get_comments(project_key)}


@app.get(f"{API_PREFIX}/activity")
async def get_activity(
    limit: int = 100,
    _: Principal = Depends(get_current_principal),
) -> Dict[str, Any]:
    activity = collaboration_store.get_activity(limit=limit)
    return {"activity": activity, "count": len(activity)}


@app.post(f"{API_PREFIX}/users/{{user_id}}/notification-preferences")
async def set_notification_preferences(
    user_id: str,
    request: NotificationPreferencesRequest,
    principal: Principal = Depends(get_current_principal),
) -> Dict[str, Any]:
    if principal.role != "admin" and principal.subject != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can only modify own preferences.")
    prefs = collaboration_store.set_notification_preferences(user_id, request.model_dump())
    return {"user_id": user_id, "preferences": prefs}


@app.get(f"{API_PREFIX}/users/{{user_id}}/notification-preferences")
async def get_notification_preferences(
    user_id: str,
    principal: Principal = Depends(get_current_principal),
) -> Dict[str, Any]:
    if principal.role != "admin" and principal.subject != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can only view own preferences.")
    prefs = collaboration_store.get_notification_preferences(user_id)
    return {"user_id": user_id, "preferences": prefs}


@app.get(f"{API_PREFIX}/notifications/recent")
async def get_recent_notifications(
    limit: int = 50,
    _: Principal = Depends(get_current_principal),
) -> Dict[str, Any]:
    items = notification_hub.recent(limit=limit)
    return {"notifications": items, "count": len(items)}


@app.websocket("/ws/notifications")
async def websocket_notifications(websocket: WebSocket) -> None:
    token, selected_subprotocol = _extract_websocket_auth_token(websocket)
    user_id = websocket.query_params.get("user_id")
    if not token:
        await websocket.close(code=4401)
        return
    payload = _decode_token(token)
    if payload is None:
        await websocket.close(code=4401)
        return
    subject = str(payload.get("sub"))
    if user_id and user_id != subject:
        await websocket.close(code=4403)
        return

    await notification_hub.connect(subject, websocket, subprotocol=selected_subprotocol)
    try:
        await websocket.send_json({"event": "connected", "user_id": subject, "timestamp": _utc_now().isoformat()})
        while True:
            _ = await websocket.receive_text()
    except WebSocketDisconnect:
        notification_hub.disconnect(subject, websocket)
    except Exception:
        notification_hub.disconnect(subject, websocket)


@app.get(f"{API_PREFIX}/plugins")
async def list_plugins(_: Principal = Depends(get_current_principal)) -> Dict[str, Any]:
    return {"plugins": plugin_manager.list_plugins()}


@app.post(f"{API_PREFIX}/plugins/reload")
async def reload_plugins(_: Principal = Depends(require_roles(["admin"]))) -> Dict[str, Any]:
    reloaded = plugin_manager.reload_plugins()
    return {"plugins": [record.to_dict() for record in reloaded.values()]}


@app.post(f"{API_PREFIX}/plugins/{{plugin_name}}/enable")
async def enable_plugin(
    plugin_name: str,
    enabled: bool = True,
    _: Principal = Depends(require_roles(["admin"])),
) -> Dict[str, Any]:
    ok = plugin_manager.set_enabled(plugin_name, enabled=enabled)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plugin not found.")
    return {"plugin": plugin_name, "enabled": enabled}


@app.post(f"{API_PREFIX}/plugins/{{plugin_name}}/execute")
async def execute_plugin(
    plugin_name: str,
    request: PluginExecuteRequest,
    principal: Principal = Depends(require_roles(PLUGIN_EXECUTE_ROLES)),
) -> Dict[str, Any]:
    ok, payload = plugin_manager.execute_plugin(
        plugin_name,
        {
            "request": request.payload,
            "principal": principal.model_dump(),
            "timestamp": _utc_now().isoformat(),
        },
    )
    if not ok:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=payload.get("error", "Plugin failed."))
    await _publish_event("plugin_executed", {"plugin": plugin_name, "subject": principal.subject})
    return {"plugin": plugin_name, "output": payload.get("result")}


@app.get(f"{API_PREFIX}/tools")
async def list_tools(_: Principal = Depends(require_roles(TOOL_INVOKE_ROLES))) -> Dict[str, Any]:
    return {"tools": TOOL_NAMES, "count": len(TOOL_NAMES)}


@app.post(f"{API_PREFIX}/tools/{{tool_name}}", response_model=ToolInvocationResponse)
async def invoke_tool_generic(
    tool_name: str,
    request: ToolInvocationRequest,
    principal: Principal = Depends(require_roles(TOOL_INVOKE_ROLES)),
) -> ToolInvocationResponse:
    response = await _invoke_tool(tool_name, request.arguments)
    await _publish_event(
        "tool_invoked",
        {"tool": tool_name, "success": response.success, "subject": principal.subject},
    )
    return response


def _tool_endpoint(tool_name: str):
    async def _invoke(
        request: ToolInvocationRequest,
        principal: Principal = Depends(require_roles(TOOL_INVOKE_ROLES)),
    ) -> ToolInvocationResponse:
        response = await _invoke_tool(tool_name, request.arguments)
        await _publish_event(
            "tool_invoked",
            {"tool": tool_name, "success": response.success, "subject": principal.subject},
        )
        return response

    _invoke.__name__ = f"invoke_{tool_name}"
    return _invoke


for _tool_name in TOOL_NAMES:
    app.add_api_route(
        f"{API_PREFIX}/tools/{_tool_name}",
        _tool_endpoint(_tool_name),
        methods=["POST"],
        name=f"tool_{_tool_name}",
        tags=["tools"],
        response_model=ToolInvocationResponse,
    )


@app.get(f"{API_PREFIX}/dashboard/overview")
async def dashboard_overview(_: Principal = Depends(get_current_principal)) -> Dict[str, Any]:
    state = mcp_server.load_state()
    log = mcp_server.load_session_log()
    projects = state.get("project_states", {})
    active_projects = [p for p in projects.values() if p.get("status") == "active"]
    pressure = mcp_server.analyze_context_pressure(state)

    sessions = log.get("sessions", [])
    recent_sessions = sessions[-30:] if isinstance(sessions, list) else []
    activity = collaboration_store.get_activity(limit=20)
    for session in recent_sessions[-5:]:
        activity.append(
            {
                "id": f"session_{session.get('session', 'n/a')}",
                "event_type": "session_logged",
                "payload": {
                    "summary": session.get("summary", ""),
                    "project": session.get("project"),
                    "time": session.get("time"),
                },
                "created_at": f"{session.get('date', '')}T{session.get('time', '00:00:00')}",
            }
        )

    return {
        "generated_at": _utc_now().isoformat(),
        "stats": {
            "total_sessions": len(recent_sessions),
            "active_projects": len(active_projects),
            "recent_wins": len(state.get("recent_wins", [])),
            "avg_energy": 78 if recent_sessions else 0,
        },
        "projects": [
            {
                "key": key,
                "name": project.get("name", key),
                "description": project.get("description", ""),
                "completion": project.get("completion", 0),
                "urgency": pressure.get("project_urgency", {}).get(key, {}).get("urgency_level", "LOW"),
                "priority": project.get("priority", "medium"),
                "lastWorked": project.get("last_worked", "n/a"),
            }
            for key, project in projects.items()
            if project.get("status") != "archived"
        ],
        "activity": activity[-40:],
        "monitoring": mcp_server.MONITORING.snapshot(),
    }


@app.get(f"{API_PREFIX}/dashboard/projects")
async def dashboard_projects(_: Principal = Depends(get_current_principal)) -> Dict[str, Any]:
    state = mcp_server.load_state()
    projects = state.get("project_states", {})
    pressure = mcp_server.analyze_context_pressure(state)
    result = []
    for key, project in projects.items():
        if project.get("status") == "archived":
            continue
        result.append(
            {
                "key": key,
                "name": project.get("name", key),
                "description": project.get("description", ""),
                "completion": project.get("completion", 0),
                "urgency": pressure.get("project_urgency", {}).get(key, {}).get("urgency_level", "LOW"),
                "priority": project.get("priority", "medium"),
                "lastWorked": project.get("last_worked", "n/a"),
                "status": project.get("status", "active"),
            }
        )
    return {"projects": result, "count": len(result)}


@app.get(f"{API_PREFIX}/dashboard/activity")
async def dashboard_activity(limit: int = 100, _: Principal = Depends(get_current_principal)) -> Dict[str, Any]:
    activity = collaboration_store.get_activity(limit=limit)
    sessions = mcp_server.load_session_log().get("sessions", [])
    if isinstance(sessions, list):
        for session in sessions[-10:]:
            activity.append(
                {
                    "id": f"session_{session.get('session', 'n/a')}",
                    "event_type": "session_logged",
                    "payload": {"summary": session.get("summary", "")},
                    "created_at": f"{session.get('date', '')}T{session.get('time', '00:00:00')}",
                }
            )
    return {"activity": activity[-limit:], "count": len(activity[-limit:])}


@app.get(f"{API_PREFIX}/dashboard/context-pressure")
async def dashboard_context_pressure(_: Principal = Depends(get_current_principal)) -> Dict[str, Any]:
    state = mcp_server.load_state()
    return mcp_server.analyze_context_pressure(state)


@app.get(f"{API_PREFIX}/analytics/advanced")
async def advanced_analytics(_: Principal = Depends(get_current_principal)) -> Dict[str, Any]:
    state = mcp_server.load_state()
    session_log = mcp_server.load_session_log()
    return generate_advanced_analytics(state, session_log)


@app.get(f"{API_PREFIX}/analytics/recommendations")
async def analytics_recommendations(_: Principal = Depends(get_current_principal)) -> Dict[str, Any]:
    state = mcp_server.load_state()
    session_log = mcp_server.load_session_log()
    analytics = generate_advanced_analytics(state, session_log)
    return {
        "generated_at": analytics.get("generated_at"),
        "recommendations": analytics.get("ai_recommendations", []),
    }


@app.get(f"{API_PREFIX}/analytics/predictions")
async def analytics_predictions(_: Principal = Depends(get_current_principal)) -> Dict[str, Any]:
    state = mcp_server.load_state()
    session_log = mcp_server.load_session_log()
    analytics = generate_advanced_analytics(state, session_log)
    return {
        "generated_at": analytics.get("generated_at"),
        "completion_predictions": analytics.get("completion_predictions", []),
        "burnout": analytics.get("burnout", {}),
    }


api_app = app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "rest_api:api_app",
        host=os.environ.get("REL_API_HOST", "0.0.0.0"),
        port=int(os.environ.get("REL_API_PORT", "8080")),
        reload=False,
    )
