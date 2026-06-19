"""Unit tests for MCP executor-safe tool policy (H1)."""

from __future__ import annotations

import json

import pytest

import mcp_server


@pytest.fixture(autouse=True)
def _restore_mcp_policy(monkeypatch: pytest.MonkeyPatch) -> None:
    """Reset module-level policy flags after each test."""
    monkeypatch.setattr(mcp_server, "MCP_EXECUTOR_SAFE", True)
    monkeypatch.setattr(mcp_server, "MCP_DENIED_TOOLS", frozenset(mcp_server.DEFAULT_MCP_DENIED_TOOLS))


@pytest.mark.asyncio
async def test_list_tools_hides_denied_tools_in_executor_safe_mode() -> None:
    tools = await mcp_server.list_tools()
    names = {tool.name for tool in tools}

    assert "get_state_summary" in names
    assert "load_context" in names
    assert "neural_learn" in names
    assert "PowerShell" not in names
    assert "fs_read_file" not in names
    assert "Screenshot" not in names
    assert len(names) == 88 - len(mcp_server.DEFAULT_MCP_DENIED_TOOLS)


@pytest.mark.asyncio
async def test_call_tool_blocks_denied_tools_in_executor_safe_mode() -> None:
    result = await mcp_server.call_tool("PowerShell", {"command": "Get-Process"})
    payload = json.loads(result[0].text)

    assert payload["code"] == 403
    assert "PowerShell" in payload["error"]
    assert "REL_MCP_EXECUTOR_SAFE=false" in payload["error"]


@pytest.mark.asyncio
async def test_call_tool_allows_bridge_tools_in_executor_safe_mode() -> None:
    result = await mcp_server.call_tool("get_state_summary", {})
    payload = json.loads(result[0].text)

    assert "error" not in payload or payload.get("code") not in {403, 401}
    assert "system_state" in payload or "project_summary" in payload


@pytest.mark.asyncio
async def test_executor_safe_false_exposes_all_tools(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mcp_server, "MCP_EXECUTOR_SAFE", False)

    tools = await mcp_server.list_tools()
    names = {tool.name for tool in tools}
    assert len(names) == 88
    assert "PowerShell" in names
    assert "fs_read_file" in names


@pytest.mark.asyncio
async def test_executor_safe_false_allows_denied_tool_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mcp_server, "MCP_EXECUTOR_SAFE", False)

    result = await mcp_server.call_tool("PowerShell", {"command": "echo test"})
    text = result[0].text

    assert "executor-safe mode" not in text
    assert '"code": 403' not in text


def test_load_mcp_executor_safe_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("REL_MCP_EXECUTOR_SAFE", raising=False)
    assert mcp_server._load_mcp_executor_safe() is True

    monkeypatch.setenv("REL_MCP_EXECUTOR_SAFE", "false")
    assert mcp_server._load_mcp_executor_safe() is False

    monkeypatch.setenv("REL_MCP_EXECUTOR_SAFE", "1")
    assert mcp_server._load_mcp_executor_safe() is True


def test_load_mcp_denied_tools_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("REL_MCP_DENIED_TOOLS", "PowerShell, fs_read_file")
    assert mcp_server._load_mcp_denied_tools() == frozenset({"PowerShell", "fs_read_file"})

    monkeypatch.delenv("REL_MCP_DENIED_TOOLS", raising=False)
    assert mcp_server._load_mcp_denied_tools() == frozenset(mcp_server.DEFAULT_MCP_DENIED_TOOLS)


def test_default_denied_tools_cover_bridge_and_desktop_risks() -> None:
    denied = set(mcp_server.DEFAULT_MCP_DENIED_TOOLS)
    bridge = set(mcp_server.DEFAULT_MCP_BRIDGE_TOOLS)

    assert bridge.isdisjoint(denied)
    assert "PowerShell" in denied
    assert "fs_write_file" in denied
    assert "Screenshot" in denied
    assert "WinFileSystem" in denied