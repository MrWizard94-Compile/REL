from __future__ import annotations

import copy
import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

import rest_api


def _write_plugin(plugin_dir: Path, name: str, code: str) -> None:
    plugin_dir.mkdir(parents=True, exist_ok=True)
    (plugin_dir / "manifest.json").write_text(
        json.dumps(
            {
                "name": name,
                "version": "1.0.0",
                "description": "test plugin",
                "entrypoint": "main.py",
                "enabled": True,
                "dependencies": [],
                "sandbox_timeout_seconds": 5,
            }
        ),
        encoding="utf-8",
    )
    (plugin_dir / "main.py").write_text(code, encoding="utf-8")


@pytest.fixture
def api_client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("REL_ADMIN_USERNAME", "admin")
    monkeypatch.setenv("REL_ADMIN_PASSWORD", "test-admin-password")

    user_store = rest_api.UserStore(tmp_path / "users.json")
    api_key_store = rest_api.APIKeyStore(tmp_path / "api_keys.json")
    collaboration_store = rest_api.CollaborationStore(tmp_path / "collab.json")
    plugin_manager = rest_api.PluginManager(tmp_path / "plugins")

    _write_plugin(
        plugin_manager.installed_root / "ok_plugin",
        "ok_plugin",
        "def run(payload, context=None):\n    return {'ok': True, 'echo': payload.get('request', {})}\n",
    )
    _write_plugin(
        plugin_manager.installed_root / "bad_plugin",
        "bad_plugin",
        "def run(payload, context=None):\n    raise RuntimeError('plugin-fail')\n",
    )
    plugin_manager.discover_plugins()

    monkeypatch.setattr(rest_api, "user_store", user_store)
    monkeypatch.setattr(rest_api, "api_key_store", api_key_store)
    monkeypatch.setattr(rest_api, "collaboration_store", collaboration_store)
    monkeypatch.setattr(rest_api, "plugin_manager", plugin_manager)
    monkeypatch.setattr(rest_api, "notification_hub", rest_api.NotificationHub())
    monkeypatch.setattr(rest_api, "rate_limiter", rest_api.SlidingWindowRateLimiter(200, 60))
    monkeypatch.setattr(rest_api, "AUTH_REQUIRED", True)

    monkeypatch.setattr(rest_api, "TOOL_NAMES", ["get_stats", "get_state", "fail_tool"])

    async def fake_call_tool(name: str, arguments: dict[str, Any]) -> list[Any]:
        if name == "fail_tool":
            return [SimpleNamespace(text='{"error":"failed"}')]
        return [SimpleNamespace(text=json.dumps({"name": name, "arguments": arguments, "ok": True}))]

    monkeypatch.setattr(rest_api.mcp_server, "call_tool", fake_call_tool)
    monkeypatch.setattr(rest_api.mcp_server, "AUTH_REQUIRED", True)
    monkeypatch.setattr(rest_api.mcp_server, "AUTH_BEARER_TOKEN", "mcp-server-token")

    state = {
        "project_states": {
            "alpha": {
                "name": "Alpha",
                "description": "Primary project",
                "status": "active",
                "completion": 55,
                "priority": "high",
                "last_worked": "2026-02-18",
            },
            "archived_x": {
                "name": "Archived",
                "description": "Hidden",
                "status": "archived",
                "completion": 100,
                "priority": "low",
                "last_worked": "2026-01-01",
            },
        },
        "recent_wins": [{"win": "Shipped API", "impact": "high"}],
    }
    session_log = {
        "sessions": [
            {
                "session": 1,
                "date": "2026-02-19",
                "time": "09:00:00",
                "summary": "Session one",
                "project": "alpha",
                "status": "ended",
            },
            {
                "session": 2,
                "date": "2026-02-20",
                "time": "10:00:00",
                "summary": "Session two",
                "project": "alpha",
                "status": "active",
            },
        ]
    }

    monkeypatch.setattr(rest_api.mcp_server, "load_state", lambda: copy.deepcopy(state))
    monkeypatch.setattr(rest_api.mcp_server, "load_session_log", lambda: copy.deepcopy(session_log))
    monkeypatch.setattr(
        rest_api.mcp_server,
        "analyze_context_pressure",
        lambda _: {
            "project_urgency": {"alpha": {"urgency_level": "HIGH"}},
            "recommended_focus": [{"project": "alpha", "urgency": "HIGH"}],
        },
    )
    monkeypatch.setattr(
        rest_api.mcp_server,
        "MONITORING",
        SimpleNamespace(snapshot=lambda: {"total_calls": 1, "total_errors": 0}),
    )

    return TestClient(rest_api.app)


def _admin_headers(client: TestClient) -> dict[str, str]:
    username = os.environ.get("REL_ADMIN_USERNAME", "admin")
    password = os.environ.get("REL_ADMIN_PASSWORD", "test-admin-password")
    token_res = client.post(
        "/api/v1/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert token_res.status_code == 200
    token = token_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_auth_and_user_management_paths(api_client: TestClient) -> None:
    bad_login = api_client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "bad"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert bad_login.status_code == 401

    headers = _admin_headers(api_client)
    me = api_client.get("/api/v1/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.json()["role"] == "admin"

    create_user = api_client.post(
        "/api/v1/users",
        json={"username": "member_a", "password": "memberpass", "role": "member"},
        headers=headers,
    )
    assert create_user.status_code == 200
    created_id = create_user.json()["id"]

    dup_user = api_client.post(
        "/api/v1/users",
        json={"username": "member_a", "password": "memberpass", "role": "member"},
        headers=headers,
    )
    assert dup_user.status_code == 409

    list_users = api_client.get("/api/v1/users", headers=headers)
    assert list_users.status_code == 200
    assert any(u["id"] == created_id for u in list_users.json()["users"])


def test_api_key_and_tools_paths(api_client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    headers = _admin_headers(api_client)

    create_key = api_client.post("/api/v1/api-keys", json={"name": "svc1", "role": "service"}, headers=headers)
    assert create_key.status_code == 200
    api_key = create_key.json()["api_key"]
    key_id = create_key.json()["record"]["id"]

    list_keys = api_client.get("/api/v1/api-keys", headers=headers)
    assert list_keys.status_code == 200
    assert list_keys.json()["keys"]

    # API key authentication path.
    tools_with_key = api_client.get("/api/v1/tools", headers={"X-API-Key": api_key})
    assert tools_with_key.status_code == 200
    assert "get_stats" in tools_with_key.json()["tools"]

    invoke_specific = api_client.post("/api/v1/tools/get_stats", json={"arguments": {}}, headers=headers)
    assert invoke_specific.status_code == 200
    assert invoke_specific.json()["success"] is True

    invoke_generic_error = api_client.post("/api/v1/tools/fail_tool", json={"arguments": {}}, headers=headers)
    assert invoke_generic_error.status_code == 200
    assert invoke_generic_error.json()["success"] is False

    unknown_tool = api_client.post("/api/v1/tools/unknown", json={"arguments": {}}, headers=headers)
    assert unknown_tool.status_code == 404

    revoke_ok = api_client.delete(f"/api/v1/api-keys/{key_id}", headers=headers)
    assert revoke_ok.status_code == 200

    revoke_missing = api_client.delete("/api/v1/api-keys/key_missing", headers=headers)
    assert revoke_missing.status_code == 404

    # Rate limit branch.
    monkeypatch.setattr(rest_api, "rate_limiter", rest_api.SlidingWindowRateLimiter(1, 60))
    first = api_client.get("/api/v1/tools", headers=headers)
    second = api_client.get("/api/v1/tools", headers=headers)
    assert first.status_code == 200
    assert second.status_code == 429


def test_collaboration_preferences_activity_and_plugins(api_client: TestClient) -> None:
    headers = _admin_headers(api_client)
    created_user = api_client.post(
        "/api/v1/users",
        json={"username": "member_b", "password": "memberpass", "role": "member"},
        headers=headers,
    )
    assert created_user.status_code == 200
    member_id = created_user.json()["id"]

    share = api_client.post(
        "/api/v1/projects/alpha/share",
        json={"user_id": member_id, "role": "member"},
        headers=headers,
    )
    assert share.status_code == 200
    missing_project_members = api_client.get("/api/v1/projects/missing/members", headers=headers)
    assert missing_project_members.status_code == 404

    members = api_client.get("/api/v1/projects/alpha/members", headers=headers)
    assert members.status_code == 200
    assert members.json()["members"]

    comment = api_client.post(
        "/api/v1/projects/alpha/comments",
        json={"comment": "Looks good"},
        headers=headers,
    )
    assert comment.status_code == 200

    comments = api_client.get("/api/v1/projects/alpha/comments", headers=headers)
    assert comments.status_code == 200
    assert comments.json()["comments"]

    activity = api_client.get("/api/v1/activity?limit=20", headers=headers)
    assert activity.status_code == 200
    assert activity.json()["count"] >= 1

    prefs = api_client.post(
        f"/api/v1/users/{member_id}/notification-preferences",
        json={"websocket": True, "email": True, "slack": False, "digest_hours": 24, "custom_triggers": ["x"]},
        headers=headers,
    )
    assert prefs.status_code == 200

    get_prefs = api_client.get(f"/api/v1/users/{member_id}/notification-preferences", headers=headers)
    assert get_prefs.status_code == 200
    assert get_prefs.json()["preferences"]["email"] is True

    # Member cannot set another user's preferences.
    member_login = api_client.post(
        "/api/v1/auth/token",
        data={"username": "member_b", "password": "memberpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert member_login.status_code == 200
    member_headers = {"Authorization": f"Bearer {member_login.json()['access_token']}"}
    member_visible = api_client.get("/api/v1/projects/alpha/members", headers=member_headers)
    assert member_visible.status_code == 200
    member_comment = api_client.post(
        "/api/v1/projects/alpha/comments",
        json={"comment": "member update"},
        headers=member_headers,
    )
    assert member_comment.status_code == 200

    forbidden_set = api_client.post(
        "/api/v1/users/user_other/notification-preferences",
        json={"websocket": True, "email": False, "slack": False, "digest_hours": 24, "custom_triggers": []},
        headers=member_headers,
    )
    assert forbidden_set.status_code == 403

    forbidden_get = api_client.get("/api/v1/users/user_other/notification-preferences", headers=member_headers)
    assert forbidden_get.status_code == 403

    member_other = api_client.post(
        "/api/v1/users",
        json={"username": "member_c", "password": "memberpass", "role": "member"},
        headers=headers,
    )
    assert member_other.status_code == 200
    member_other_login = api_client.post(
        "/api/v1/auth/token",
        data={"username": "member_c", "password": "memberpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert member_other_login.status_code == 200
    member_other_headers = {"Authorization": f"Bearer {member_other_login.json()['access_token']}"}
    member_other_members = api_client.get("/api/v1/projects/alpha/members", headers=member_other_headers)
    assert member_other_members.status_code == 403
    member_other_comments = api_client.get("/api/v1/projects/alpha/comments", headers=member_other_headers)
    assert member_other_comments.status_code == 403
    member_other_share = api_client.post(
        "/api/v1/projects/alpha/share",
        json={"user_id": member_id, "role": "member"},
        headers=member_other_headers,
    )
    assert member_other_share.status_code == 403

    plugins = api_client.get("/api/v1/plugins", headers=headers)
    assert plugins.status_code == 200
    assert plugins.json()["plugins"]

    reload_plugins = api_client.post("/api/v1/plugins/reload", headers=headers)
    assert reload_plugins.status_code == 200

    enable_missing = api_client.post("/api/v1/plugins/missing/enable?enabled=true", headers=headers)
    assert enable_missing.status_code == 404

    enable_ok = api_client.post("/api/v1/plugins/ok_plugin/enable?enabled=true", headers=headers)
    assert enable_ok.status_code == 200

    execute_ok = api_client.post(
        "/api/v1/plugins/ok_plugin/execute",
        json={"payload": {"x": 1}},
        headers=headers,
    )
    assert execute_ok.status_code == 200
    assert execute_ok.json()["output"]["ok"] is True

    execute_bad = api_client.post(
        "/api/v1/plugins/bad_plugin/execute",
        json={"payload": {}},
        headers=headers,
    )
    assert execute_bad.status_code == 400
    execute_forbidden_member = api_client.post(
        "/api/v1/plugins/ok_plugin/execute",
        json={"payload": {"x": 2}},
        headers=member_headers,
    )
    assert execute_forbidden_member.status_code == 403

    notifications = api_client.get("/api/v1/notifications/recent?limit=20", headers=headers)
    assert notifications.status_code == 200


def test_dashboard_and_analytics_endpoints(api_client: TestClient) -> None:
    headers = _admin_headers(api_client)

    overview = api_client.get("/api/v1/dashboard/overview", headers=headers)
    assert overview.status_code == 200
    assert "stats" in overview.json()
    assert overview.json()["projects"]

    projects = api_client.get("/api/v1/dashboard/projects", headers=headers)
    assert projects.status_code == 200
    assert projects.json()["count"] >= 1

    activity = api_client.get("/api/v1/dashboard/activity?limit=10", headers=headers)
    assert activity.status_code == 200

    pressure = api_client.get("/api/v1/dashboard/context-pressure", headers=headers)
    assert pressure.status_code == 200
    assert "project_urgency" in pressure.json()

    advanced = api_client.get("/api/v1/analytics/advanced", headers=headers)
    assert advanced.status_code == 200
    assert "completion_predictions" in advanced.json()

    recs = api_client.get("/api/v1/analytics/recommendations", headers=headers)
    assert recs.status_code == 200
    assert "recommendations" in recs.json()

    preds = api_client.get("/api/v1/analytics/predictions", headers=headers)
    assert preds.status_code == 200
    assert "burnout" in preds.json()


def test_websocket_notification_paths(api_client: TestClient) -> None:
    with pytest.raises(WebSocketDisconnect):
        with api_client.websocket_connect("/ws/notifications"):
            pass

    with pytest.raises(WebSocketDisconnect):
        with api_client.websocket_connect("/ws/notifications?token=not-a-valid-token"):
            pass

    headers = _admin_headers(api_client)
    token = headers["Authorization"].split(" ", 1)[1]

    with api_client.websocket_connect(
        "/ws/notifications",
        subprotocols=["rel-notify", f"bearer.{token}"],
    ) as websocket:
        message = websocket.receive_json()
        assert message["event"] == "connected"
        websocket.send_text("ping")

    with pytest.raises(WebSocketDisconnect):
        with api_client.websocket_connect(f"/ws/notifications?token={token}"):
            pass

    with pytest.raises(WebSocketDisconnect):
        with api_client.websocket_connect(
            "/ws/notifications?user_id=someone_else",
            subprotocols=["rel-notify", f"bearer.{token}"],
        ):
            pass


def test_login_endpoint_rate_limited(api_client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(rest_api, "login_rate_limiter", rest_api.SlidingWindowRateLimiter(1, 60))
    username = os.environ.get("REL_ADMIN_USERNAME", "admin")

    first = api_client.post(
        "/api/v1/auth/token",
        data={"username": username, "password": "wrong-pass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    second = api_client.post(
        "/api/v1/auth/token",
        data={"username": username, "password": "wrong-pass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert first.status_code in {401, 429}
    assert second.status_code == 429
