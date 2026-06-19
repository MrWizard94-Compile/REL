from __future__ import annotations

import os
from typing import Dict

import pytest
from fastapi.testclient import TestClient

import rest_api


def _auth_headers(client: TestClient) -> Dict[str, str]:
    username = os.environ.get("REL_ADMIN_USERNAME", rest_api.DEFAULT_ADMIN_USERNAME)
    password = os.environ.get("REL_ADMIN_PASSWORD", rest_api.DEFAULT_ADMIN_PASSWORD)
    response = client.post(
        "/api/v1/auth/token",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    if response.status_code != 200:
        pytest.skip("Default admin credentials are not available in this environment.")
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_health_endpoint_available() -> None:
    client = TestClient(rest_api.app)
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["tool_count"] >= 45


def test_tool_routes_are_registered_for_each_tool() -> None:
    tool_routes = []
    for route in rest_api.app.routes:
        path = getattr(route, "path", "")
        if path.startswith("/api/v1/tools/") and "{tool_name}" not in path:
            tool_routes.append(path)
    assert len(tool_routes) >= 45


def test_tools_listing_and_invoke_stats() -> None:
    client = TestClient(rest_api.app)
    headers = _auth_headers(client)

    list_response = client.get("/api/v1/tools", headers=headers)
    assert list_response.status_code == 200
    tools = list_response.json()["tools"]
    assert "get_stats" in tools
    assert len(tools) >= 45

    invoke_response = client.post(
        "/api/v1/tools/get_stats",
        json={"arguments": {}},
        headers=headers,
    )
    assert invoke_response.status_code == 200
    payload = invoke_response.json()
    assert payload["tool"] == "get_stats"
    assert "result" in payload


def test_plugin_listing_endpoint() -> None:
    client = TestClient(rest_api.app)
    headers = _auth_headers(client)

    response = client.get("/api/v1/plugins", headers=headers)
    assert response.status_code == 200
    payload = response.json()
    assert "plugins" in payload
