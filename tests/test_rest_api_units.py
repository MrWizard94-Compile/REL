from __future__ import annotations

import copy
import importlib.util
import json
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any
import time

import pytest
from fastapi import HTTPException
from starlette.requests import Request

import rest_api


def test_json_helpers_round_trip_and_fallback(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    payload = {"a": 1}
    rest_api._json_write(path, payload)
    assert rest_api._json_read(path, {}) == payload

    bad_path = tmp_path / "bad.json"
    bad_path.write_text("{not-json", encoding="utf-8")
    assert rest_api._json_read(bad_path, {"fallback": True}) == {"fallback": True}
    assert rest_api._json_read(tmp_path / "missing.json", {"x": 1}) == {"x": 1}


def test_hash_and_password_and_token_helpers() -> None:
    assert rest_api._hash_value("abc") == rest_api._hash_value("abc")
    assert rest_api._password_hash("pw", "salt") == rest_api._password_hash("pw", "salt")

    token = rest_api._encode_token({"sub": "u1", "exp": int(rest_api._utc_now().timestamp()) + 60})
    decoded = rest_api._decode_token(token)
    assert decoded is not None
    assert decoded["sub"] == "u1"

    assert rest_api._decode_token("bad-token") is None
    assert rest_api._decode_token("abc.def") is None
    expired = rest_api._encode_token({"sub": "u2", "exp": int(rest_api._utc_now().timestamp()) - 1})
    assert rest_api._decode_token(expired) is None
    missing_exp = rest_api._encode_token({"sub": "u3"})
    assert rest_api._decode_token(missing_exp) is None
    assert rest_api._decode_token(rest_api._encode_token({"sub": "u4", "exp": "x"})) is None
    assert rest_api._decode_token(rest_api._encode_token({"sub": "u5", "exp": int(rest_api._utc_now().timestamp()) + 60, "obj": []})) is not None

    # Signature-valid but decode-invalid body branch.
    body = "!!!"
    sig = rest_api.hmac.new(rest_api.OAUTH2_SECRET, body.encode("utf-8"), rest_api.hashlib.sha256).hexdigest()
    assert rest_api._decode_token(f"{body}.{sig}") is None

    # Signature-valid and decoded payload not dict branch.
    payload_raw = rest_api.base64.urlsafe_b64encode(json.dumps([1, 2, 3]).encode("utf-8")).decode("utf-8").rstrip("=")
    payload_sig = rest_api.hmac.new(
        rest_api.OAUTH2_SECRET, payload_raw.encode("utf-8"), rest_api.hashlib.sha256
    ).hexdigest()
    assert rest_api._decode_token(f"{payload_raw}.{payload_sig}") is None


def test_rest_api_source_load_uses_explicit_env_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REL_OAUTH2_SECRET", "explicit-secret-value")
    monkeypatch.setenv("REL_ADMIN_PASSWORD", "explicit-admin-password")

    spec = importlib.util.spec_from_file_location("rest_api_env_probe", Path(rest_api.__file__))
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.OAUTH2_SECRET == b"explicit-secret-value"
    assert module.DEFAULT_ADMIN_PASSWORD == "explicit-admin-password"


def test_rest_api_main_guard_invokes_uvicorn(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: dict[str, Any] = {}

    class _FakeUvicorn:
        @staticmethod
        def run(*args: Any, **kwargs: Any) -> None:
            calls["args"] = args
            calls["kwargs"] = kwargs

    monkeypatch.setitem(sys.modules, "uvicorn", _FakeUvicorn)
    monkeypatch.setenv("REL_API_HOST", "127.0.0.1")
    monkeypatch.setenv("REL_API_PORT", "9191")

    runpy.run_path(str(Path(rest_api.__file__)), run_name="__main__")

    assert calls["args"][0] == "rest_api:api_app"
    assert calls["kwargs"]["host"] == "127.0.0.1"
    assert calls["kwargs"]["port"] == 9191


def test_user_store_create_auth_list_get(tmp_path: Path) -> None:
    store = rest_api.UserStore(tmp_path / "users.json")
    users = store.list_users()
    assert any(u["role"] == "admin" for u in users)

    created = store.create_user("member1", "memberpass", role="member")
    assert created["username"] == "member1"
    assert store.get_user(created["id"]) is not None

    auth_ok = store.authenticate("member1", "memberpass")
    assert auth_ok is not None
    assert auth_ok["role"] == "member"
    assert store.authenticate("member1", "wrong") is None
    assert store.authenticate("missing", "x") is None
    assert store.get_user("missing") is None

    # inactive user branch
    data = json.loads((tmp_path / "users.json").read_text(encoding="utf-8"))
    for value in data["users"].values():
        if value["username"] == "member1":
            value["active"] = False
    (tmp_path / "users.json").write_text(json.dumps(data), encoding="utf-8")
    assert store.authenticate("member1", "memberpass") is None

    with pytest.raises(ValueError):
        store.create_user("member1", "memberpass", role="member")


def test_api_key_store_create_auth_revoke(tmp_path: Path) -> None:
    store = rest_api.APIKeyStore(tmp_path / "keys.json")
    created = store.create_key("svc", "service", "admin")
    raw_key = created["api_key"]
    rec = created["record"]
    assert rec["name"] == "svc"
    assert rec["revoked"] is False

    auth = store.authenticate(raw_key)
    assert auth is not None
    assert auth["id"] == rec["id"]

    listed = store.list_keys()
    assert len(listed) == 1
    assert listed[0]["last_used_at"] is not None

    assert store.revoke(rec["id"]) is True
    assert store.authenticate(raw_key) is None
    assert store.authenticate("") is None
    assert store.list_keys() == []
    assert store.list_keys(include_revoked=True)[0]["revoked"] is True
    assert store.revoke("missing") is False


def test_rate_limiter_consumption_and_retry() -> None:
    limiter = rest_api.SlidingWindowRateLimiter(limit=1, window_seconds=60)
    allowed1, remaining1, _ = limiter.consume("id1")
    assert allowed1 is True
    assert remaining1 == 0

    allowed2, _, retry = limiter.consume("id1")
    assert allowed2 is False
    assert retry >= 1

    short = rest_api.SlidingWindowRateLimiter(limit=1, window_seconds=1)
    assert short.consume("id2")[0] is True
    time.sleep(1.1)
    assert short.consume("id2")[0] is True


def test_collaboration_store_paths(tmp_path: Path) -> None:
    store = rest_api.CollaborationStore(tmp_path / "collab.json")
    share = store.share_project("proj", "u1", "member", "admin")
    assert share["user_id"] == "u1"

    members = store.get_project_members("proj")
    assert len(members) == 1

    comment = store.add_comment("proj", "u1", "hello")
    assert comment["project"] == "proj"

    comments = store.get_comments("proj")
    assert len(comments) == 1
    prefs = store.set_notification_preferences("u1", {"websocket": True})
    assert prefs["websocket"] is True
    assert store.get_notification_preferences("u1")["websocket"] is True
    assert store.get_notification_preferences("missing") == {}

    activity = store.get_activity(limit=10)
    assert len(activity) >= 2

    # Non-list activity branch.
    (tmp_path / "collab.json").write_text(
        json.dumps({"project_members": {}, "comments": {}, "activity": "x", "notification_preferences": {}}),
        encoding="utf-8",
    )
    assert store.get_activity(limit=5) == []


class _DummySocket:
    def __init__(self, fail_send: bool = False) -> None:
        self.fail_send = fail_send
        self.accepted = False
        self.messages: list[dict[str, Any]] = []

    async def accept(self, subprotocol: str | None = None) -> None:
        _ = subprotocol
        self.accepted = True

    async def send_json(self, payload: dict[str, Any]) -> None:
        if self.fail_send:
            raise RuntimeError("send failed")
        self.messages.append(payload)


@pytest.mark.asyncio
async def test_notification_hub_connect_publish_disconnect_recent() -> None:
    hub = rest_api.NotificationHub()
    ws_good = _DummySocket()
    ws_bad = _DummySocket(fail_send=True)

    await hub.connect("u1", ws_good)  # type: ignore[arg-type]
    await hub.connect("u1", ws_bad)  # type: ignore[arg-type]
    assert ws_good.accepted is True

    await hub.publish("evt", {"value": 1}, ["u1"])
    assert ws_good.messages
    # bad socket is removed after send failure
    assert len(hub._connections.get("u1", set())) == 1

    recent = hub.recent(limit=5)
    assert len(recent) == 1

    hub.disconnect("u1", ws_good)  # type: ignore[arg-type]
    assert "u1" not in hub._connections
    hub.disconnect("missing", ws_good)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_publish_event_logs_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _raise(*_: Any, **__: Any) -> None:
        raise RuntimeError("fail")

    monkeypatch.setattr(rest_api.notification_hub, "publish", _raise)
    await rest_api._publish_event("x", {"a": 1})


def test_identity_for_rate_limit_paths() -> None:
    req_api = Request({"type": "http", "headers": [(b"x-api-key", b"k1")], "client": ("1.2.3.4", 1234)})
    assert rest_api._identity_for_rate_limit(req_api).startswith("api_key:")

    req_bearer = Request(
        {"type": "http", "headers": [(b"authorization", b"Bearer abc")], "client": ("1.2.3.4", 1234)}
    )
    assert rest_api._identity_for_rate_limit(req_bearer).startswith("bearer:")

    req_ip = Request({"type": "http", "headers": [], "client": ("1.2.3.4", 1234)})
    assert rest_api._identity_for_rate_limit(req_ip).startswith("ip:")


def test_extract_websocket_auth_token_paths() -> None:
    ws_protocol = SimpleNamespace(
        headers={"sec-websocket-protocol": "rel-notify, bearer.protocoltoken"},
        query_params={},
    )
    token, subprotocol = rest_api._extract_websocket_auth_token(ws_protocol)  # type: ignore[arg-type]
    assert token == "protocoltoken"
    assert subprotocol == "rel-notify"

    ws_header = SimpleNamespace(
        headers={"authorization": "Bearer headertoken"},
        query_params={},
    )
    token2, subprotocol2 = rest_api._extract_websocket_auth_token(ws_header)  # type: ignore[arg-type]
    assert token2 == "headertoken"
    assert subprotocol2 is None

    ws_query = SimpleNamespace(
        headers={},
        query_params={"token": "querytoken"},
    )
    token3, subprotocol3 = rest_api._extract_websocket_auth_token(ws_query)  # type: ignore[arg-type]
    assert token3 is None
    assert subprotocol3 is None


@pytest.mark.asyncio
async def test_get_current_principal_and_roles(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    # API key auth path.
    key_store = rest_api.APIKeyStore(tmp_path / "keys.json")
    created = key_store.create_key("svc", "service", "admin")
    monkeypatch.setattr(rest_api, "api_key_store", key_store)
    principal_key = await rest_api.get_current_principal(token=None, api_key=created["api_key"])
    assert principal_key.auth_type == "api_key"

    with pytest.raises(HTTPException):
        await rest_api.get_current_principal(token=None, api_key="bad-key")

    # OAuth2 token path.
    token = rest_api._encode_token(
        {
            "sub": "user_1",
            "username": "u1",
            "role": "admin",
            "exp": int(rest_api._utc_now().timestamp()) + 60,
        }
    )
    principal_token = await rest_api.get_current_principal(token=token, api_key=None)
    assert principal_token.auth_type == "oauth2"
    assert principal_token.role == "admin"

    with pytest.raises(HTTPException):
        await rest_api.get_current_principal(token="bad.token", api_key=None)

    monkeypatch.setattr(rest_api, "AUTH_REQUIRED", False)
    anon = await rest_api.get_current_principal(token=None, api_key=None)
    assert anon.subject == "anonymous"
    monkeypatch.setattr(rest_api, "AUTH_REQUIRED", True)
    with pytest.raises(HTTPException):
        await rest_api.get_current_principal(token=None, api_key=None)

    dep = rest_api.require_roles(["admin"])
    ok = await dep(principal=rest_api.Principal(subject="u1", role="admin", auth_type="oauth2"))
    assert ok.role == "admin"
    with pytest.raises(HTTPException):
        await dep(principal=rest_api.Principal(subject="u2", role="member", auth_type="oauth2"))


def test_tool_response_to_payload_and_discover_names(monkeypatch: pytest.MonkeyPatch) -> None:
    item_json = SimpleNamespace(text='{"a":1}')
    item_text = SimpleNamespace(text="plain")
    item_other = SimpleNamespace(text=123)
    parsed = rest_api._tool_response_to_payload([item_json, item_text, item_other])
    assert parsed[0]["a"] == 1
    assert parsed[1] == "plain"
    assert parsed[2] == 123
    assert rest_api._tool_response_to_payload([item_json]) == {"a": 1}

    names = rest_api._discover_tool_names()
    assert "get_state" in names

    original_file = rest_api.mcp_server.__file__
    monkeypatch.setattr(rest_api.mcp_server, "__file__", str(Path("Z:/missing/notfound.py")))
    assert rest_api._discover_tool_names() == []
    monkeypatch.setattr(rest_api.mcp_server, "__file__", original_file)


@pytest.mark.asyncio
async def test_invoke_tool_paths(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rest_api, "TOOL_NAMES", ["ok_tool", "err_tool"])

    async def fake_call(name: str, payload: dict[str, Any]) -> list[Any]:
        if name == "err_tool":
            return [SimpleNamespace(text='{"error":"bad"}')]
        return [SimpleNamespace(text=json.dumps({"name": name, "payload": payload}))]

    monkeypatch.setattr(rest_api.mcp_server, "call_tool", fake_call)
    monkeypatch.setattr(rest_api.mcp_server, "AUTH_REQUIRED", True)
    monkeypatch.setattr(rest_api.mcp_server, "AUTH_BEARER_TOKEN", "server-token")

    ok = await rest_api._invoke_tool("ok_tool", {"x": 1})
    assert ok.success is True
    assert ok.result["payload"]["auth_token"] == "server-token"

    err = await rest_api._invoke_tool("err_tool", {})
    assert err.success is False

    with pytest.raises(HTTPException):
        await rest_api._invoke_tool("missing", {})

    monkeypatch.setattr(rest_api.mcp_server, "AUTH_REQUIRED", False)
    monkeypatch.setattr(rest_api.mcp_server, "AUTH_BEARER_TOKEN", None)


@pytest.mark.asyncio
async def test_tool_endpoint_closure_and_dashboard_activity_non_list_sessions(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _fake_invoke(tool_name: str, arguments: dict[str, Any]) -> rest_api.ToolInvocationResponse:
        return rest_api.ToolInvocationResponse(
            tool=tool_name,
            success=True,
            result={"arguments": arguments},
            invoked_at=rest_api._utc_now().isoformat(),
        )

    monkeypatch.setattr(rest_api, "_invoke_tool", _fake_invoke)
    endpoint = rest_api._tool_endpoint("get_stats")
    response = await endpoint(
        request=rest_api.ToolInvocationRequest(arguments={"x": 1}),
        principal=rest_api.Principal(subject="u1", role="admin", auth_type="oauth2"),
    )
    assert response.tool == "get_stats"

    monkeypatch.setattr(rest_api.mcp_server, "load_session_log", lambda: {"sessions": "bad"})
    out = await rest_api.dashboard_activity(
        limit=5,
        _=rest_api.Principal(subject="u1", role="admin", auth_type="oauth2"),
    )
    assert out["count"] == len(out["activity"])


@pytest.mark.asyncio
async def test_app_lifespan_and_websocket_generic_exception_branch(monkeypatch: pytest.MonkeyPatch) -> None:
    called = {"discover": False}
    monkeypatch.setattr(rest_api.plugin_manager, "discover_plugins", lambda: called.__setitem__("discover", True))
    async with rest_api.app_lifespan(rest_api.app):
        pass
    assert called["discover"] is True

    class _Ws:
        def __init__(self) -> None:
            self.query_params = {"token": rest_api._encode_token({"sub": "u1", "exp": int(rest_api._utc_now().timestamp()) + 60})}
            self.headers = {}
            self.closed_codes: list[int] = []

        async def close(self, code: int) -> None:
            self.closed_codes.append(code)

        async def accept(self, subprotocol: str | None = None) -> None:
            _ = subprotocol
            return None

        async def send_json(self, _: dict[str, Any]) -> None:
            return None

        async def receive_text(self) -> str:
            raise RuntimeError("boom")

    ws = _Ws()
    await rest_api.websocket_notifications(ws)  # type: ignore[arg-type]
