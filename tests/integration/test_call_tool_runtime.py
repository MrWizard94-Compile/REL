"""Runtime integration tests for mcp_server.call_tool."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
import mcp_server


@pytest.fixture
def runtime_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Dict[str, Path]:
    """Patch mcp_server globals to use temporary state files."""
    data_path = tmp_path / "data"
    data_path.mkdir(parents=True, exist_ok=True)

    core_state = {
        "system_state": {"status": "TEST", "session_count": 0},
        "current_context": {"active_project": None, "current_focus": "Testing"},
        "project_states": {},
        "recent_wins": [],
        "active_ideas": [],
        "flags": {},
    }
    session_log = {"sessions": []}

    core_path = data_path / "CoreState.json"
    session_path = data_path / "SessionLog.json"
    core_path.write_text(json.dumps(core_state), encoding="utf-8")
    session_path.write_text(json.dumps(session_log), encoding="utf-8")

    monkeypatch.setattr(mcp_server, "REL_PATH", tmp_path)
    monkeypatch.setattr(mcp_server, "DATA_PATH", data_path)
    monkeypatch.setattr(mcp_server, "BRAIN_PATH", data_path / "brain")
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_PATH", data_path / "neural_web")
    monkeypatch.setattr(mcp_server, "CORE_STATE_PATH", core_path)
    monkeypatch.setattr(mcp_server, "SESSION_LOG_PATH", session_path)
    monkeypatch.setattr(mcp_server, "SNAPSHOTS_PATH", data_path / "snapshots")
    monkeypatch.setattr(mcp_server, "DEFAULT_OBSIDIAN_EXPORT_PATH", tmp_path / "obsidian_export")

    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", False)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", False)
    monkeypatch.setattr(mcp_server, "_brain", None)
    monkeypatch.setattr(mcp_server, "_neural_web", None)

    # Ensure auth is disabled by default for runtime tool-path tests.
    monkeypatch.setattr(mcp_server, "AUTH_REQUIRED", False)
    monkeypatch.setattr(mcp_server, "AUTH_BEARER_TOKEN", None)

    mcp_server.ensure_data_paths()

    return {
        "rel": tmp_path,
        "data": data_path,
        "core": core_path,
        "session": session_path,
    }


def parse_text_response(response: Any) -> Dict[str, Any]:
    """Parse the first MCP TextContent JSON payload."""
    assert isinstance(response, list)
    assert len(response) == 1
    return json.loads(response[0].text)


@pytest.mark.asyncio
async def test_core_project_and_session_runtime_paths(runtime_env: Dict[str, Path]) -> None:
    create = await mcp_server.call_tool(
        "create_project",
        {"key": "runtime_project", "name": "Runtime Project", "description": "coverage"},
    )
    create_payload = parse_text_response(create)
    assert create_payload["success"] is True

    duplicate = parse_text_response(
        await mcp_server.call_tool(
            "create_project",
            {"key": "runtime_project", "name": "Runtime Project", "description": "coverage"},
        )
    )
    assert "already exists" in duplicate["error"].lower()

    project_data = parse_text_response(
        await mcp_server.call_tool("get_project", {"project": "runtime_project"})
    )
    assert project_data["name"] == "Runtime Project"

    active = parse_text_response(
        await mcp_server.call_tool("set_active_project", {"project": "runtime_project"})
    )
    assert active["active_project"] == "runtime_project"

    session = parse_text_response(
        await mcp_server.call_tool(
            "log_session",
            {"summary": "Implemented runtime flow", "achievements": ["tool call", "state update"]},
        )
    )
    assert session["success"] is True

    history = parse_text_response(await mcp_server.call_tool("get_session_history", {"count": 1}))
    assert len(history) == 1
    assert history[0]["summary"] == "Implemented runtime flow"

    current = parse_text_response(await mcp_server.call_tool("get_current_session", {}))
    assert current["status"] == "active"

    ended = parse_text_response(
        await mcp_server.call_tool("end_session", {"summary": "Ended runtime session"})
    )
    assert ended["success"] is True

    search = parse_text_response(
        await mcp_server.call_tool("search_sessions", {"query": "runtime"})
    )
    assert len(search) >= 1

    stats = parse_text_response(await mcp_server.call_tool("get_project_stats", {"project": "runtime_project"}))
    assert stats["project"] == "runtime_project"


@pytest.mark.asyncio
async def test_core_state_progress_and_cognitive_runtime_paths(runtime_env: Dict[str, Path]) -> None:
    _ = parse_text_response(
        await mcp_server.call_tool(
            "create_project",
            {"key": "runtime_project", "name": "Runtime Project", "description": "for progress logs"},
        )
    )

    updated = parse_text_response(
        await mcp_server.call_tool("update_state", {"updates": {"flags": {"runtime_flag": True}}})
    )
    assert updated["success"] is True

    _ = parse_text_response(await mcp_server.call_tool("log_win", {"win": "Runtime win", "impact": "high"}))
    _ = parse_text_response(await mcp_server.call_tool("capture_idea", {"idea": "Runtime idea"}))
    _ = parse_text_response(await mcp_server.call_tool("update_focus", {"focus": "Runtime focus"}))
    progress = parse_text_response(
        await mcp_server.call_tool(
            "log_progress",
            {"project": "runtime_project", "update": "Updated runtime progress"},
        )
    )
    assert progress["success"] is True
    assert progress["project"] == "runtime_project"
    assert "progress_entry" in progress

    state = parse_text_response(await mcp_server.call_tool("get_state", {}))
    assert state["flags"]["runtime_flag"] is True
    assert len(state["project_states"]["runtime_project"]["progress_log"]) == 1

    summary = parse_text_response(await mcp_server.call_tool("get_state_summary", {}))
    assert "system_state" in summary

    all_flags = parse_text_response(await mcp_server.call_tool("get_all_flags", {}))
    assert all_flags["runtime_flag"] is True

    _ = parse_text_response(await mcp_server.call_tool("get_insights", {}))
    _ = parse_text_response(await mcp_server.call_tool("predict_cold_projects", {}))
    conflict = parse_text_response(
        await mcp_server.call_tool(
            "check_for_conflict",
            {"statement": "We won't use runtime auth anymore"},
        )
    )
    assert "conflicts_found" in conflict

    _ = parse_text_response(await mcp_server.call_tool("get_story_arc", {}))
    _ = parse_text_response(await mcp_server.call_tool("get_affective_trends", {}))
    patterns = parse_text_response(await mcp_server.call_tool("get_patterns", {}))
    assert "message" in patterns

    productivity = parse_text_response(
        await mcp_server.call_tool("analyze_productivity", {"days": 7})
    )
    assert productivity["days_analyzed"] == 7

    actions = parse_text_response(await mcp_server.call_tool("get_suggested_actions", {}))
    assert isinstance(actions, list)

    validate_payload = parse_text_response(await mcp_server.call_tool("validate", {}))
    assert validate_payload["valid"] is True

    stats = parse_text_response(await mcp_server.call_tool("get_stats", {}))
    assert stats["total_wins"] >= 1


@pytest.mark.asyncio
async def test_context_and_advanced_runtime_paths(runtime_env: Dict[str, Path]) -> None:
    notes = runtime_env["rel"] / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    (notes / "runtime-note.txt").write_text("runtime query reference", encoding="utf-8")

    search_files = parse_text_response(
        await mcp_server.call_tool("search_files", {"query": "runtime"})
    )
    assert search_files["total_found"] >= 1

    context = parse_text_response(
        await mcp_server.call_tool("load_context", {"query": "runtime", "max_tokens": 2000})
    )
    assert context["query"] == "runtime"

    preview = parse_text_response(
        await mcp_server.call_tool("get_loading_preview", {"query": "runtime"})
    )
    assert "preview" in preview

    recs = parse_text_response(
        await mcp_server.call_tool("get_recommendations", {"query": "runtime"})
    )
    assert "recommendations" in recs

    analytics = parse_text_response(await mcp_server.call_tool("get_analytics", {}))
    assert "monitoring" in analytics

    snapshot = parse_text_response(
        await mcp_server.call_tool("create_snapshot", {"name": "runtime_snapshot"})
    )
    assert snapshot["success"] is True
    assert Path(snapshot["path"]).exists()

    graph = parse_text_response(await mcp_server.call_tool("get_knowledge_graph", {}))
    assert "nodes" in graph
    assert "edges" in graph

    synced = parse_text_response(await mcp_server.call_tool("sync_obsidian", {}))
    assert synced["success"] is True
    assert synced["files_written"] >= 2
    assert Path(synced["vault_path"]).exists()
    assert (Path(synced["vault_path"]) / "REL_State.md").exists()

    loaded = parse_text_response(await mcp_server.call_tool("smart_load", {"query": "runtime"}))
    assert loaded["loaded"] is True
    assert loaded["query"] == "runtime"
    assert "matches" in loaded


@pytest.mark.asyncio
async def test_brain_and_neural_unavailable_paths(runtime_env: Dict[str, Path]) -> None:
    semantic = parse_text_response(
        await mcp_server.call_tool("semantic_search", {"query": "runtime", "limit": 3})
    )
    assert "error" in semantic

    learn = parse_text_response(
        await mcp_server.call_tool("neural_learn", {"text": "runtime text"})
    )
    assert learn["success"] is False

    related = parse_text_response(
        await mcp_server.call_tool("neural_get_related", {"concept": "runtime", "limit": 5})
    )
    assert "error" in related

    patterns = parse_text_response(await mcp_server.call_tool("neural_get_patterns", {"limit": 5}))
    assert "error" in patterns

    decay = parse_text_response(await mcp_server.call_tool("neural_apply_decay", {"days_threshold": 3}))
    assert decay["success"] is False


@pytest.mark.asyncio
async def test_validation_errors_are_returned(runtime_env: Dict[str, Path]) -> None:
    invalid_project = parse_text_response(
        await mcp_server.call_tool("create_project", {"key": "Invalid Key", "name": "Bad"})
    )
    assert invalid_project["code"] == 422
    assert "Validation failed" in invalid_project["error"]

    invalid_search = parse_text_response(
        await mcp_server.call_tool("search_sessions", {"query": "   "})
    )
    assert invalid_search["code"] == 422


@pytest.mark.asyncio
async def test_auth_required_paths(runtime_env: Dict[str, Path], monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(mcp_server, "AUTH_REQUIRED", True)
    monkeypatch.setattr(mcp_server, "AUTH_BEARER_TOKEN", "secret-token")

    missing = parse_text_response(await mcp_server.call_tool("get_state", {}))
    assert missing["code"] == 401

    wrong = parse_text_response(
        await mcp_server.call_tool("get_state", {"auth_token": "wrong-token"})
    )
    assert wrong["code"] == 401

    ok = parse_text_response(
        await mcp_server.call_tool("get_state", {"auth_token": "secret-token"})
    )
    assert "system_state" in ok


@pytest.mark.asyncio
async def test_unknown_tool_returns_error(runtime_env: Dict[str, Path]) -> None:
    unknown = parse_text_response(await mcp_server.call_tool("unknown_tool", {}))
    assert "Unknown tool" in unknown["error"]
