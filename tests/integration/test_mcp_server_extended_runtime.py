from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

import pytest

import mcp_server


def _parse_payload(response: Any) -> Dict[str, Any]:
    assert isinstance(response, list)
    assert len(response) == 1
    return json.loads(response[0].text)


@pytest.fixture
def isolated_runtime(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Dict[str, Path]:
    data_path = tmp_path / "data"
    data_path.mkdir(parents=True, exist_ok=True)

    core_state = {
        "system_state": {"status": "TEST"},
        "current_context": {"active_project": None},
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

    monkeypatch.setattr(mcp_server, "AUTH_REQUIRED", False)
    monkeypatch.setattr(mcp_server, "AUTH_BEARER_TOKEN", None)
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", False)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", False)
    monkeypatch.setattr(mcp_server, "_brain", None)
    monkeypatch.setattr(mcp_server, "_neural_web", None)

    mcp_server.ensure_data_paths()
    return {"tmp": tmp_path, "data": data_path, "core": core_path, "session": session_path}


def test_private_auth_and_validation_helpers(monkeypatch: pytest.MonkeyPatch) -> None:
    stripped = mcp_server._strip_auth_fields(
        {"auth_token": "x", "_auth_token": "y", "access_token": "z", "bearer_token": "w", "keep": 1}
    )
    assert stripped == {"keep": 1}
    assert mcp_server._strip_auth_fields(None) == {}

    monkeypatch.setattr(mcp_server, "AUTH_REQUIRED", True)
    monkeypatch.setattr(mcp_server, "AUTH_BEARER_TOKEN", None)
    assert "not configured" in (mcp_server._validate_oauth2_token({}) or "")

    monkeypatch.setattr(mcp_server, "AUTH_BEARER_TOKEN", "token-1")
    assert "Missing bearer token" in (mcp_server._validate_oauth2_token({}) or "")
    assert "Invalid bearer token" in (mcp_server._validate_oauth2_token({"auth_token": "bad"}) or "")
    assert mcp_server._validate_oauth2_token({"auth_token": "token-1"}) is None

    monkeypatch.setattr(mcp_server, "AUTH_REQUIRED", False)
    assert mcp_server._validate_oauth2_token({}) is None

    valid_payload = mcp_server._validate_tool_arguments("create_project", {"key": "abc", "name": "ABC"})
    assert valid_payload["key"] == "abc"

    with pytest.raises(ValueError):
        mcp_server._validate_tool_arguments("create_project", {"key": "bad key", "name": "ABC"})


def test_load_state_and_log_invalid_json_paths(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    core = tmp_path / "CoreState.json"
    session = tmp_path / "SessionLog.json"
    core.write_text("{bad-json", encoding="utf-8")
    session.write_text("{bad-json", encoding="utf-8")

    monkeypatch.setattr(mcp_server, "CORE_STATE_PATH", core)
    monkeypatch.setattr(mcp_server, "SESSION_LOG_PATH", session)

    assert mcp_server.load_state() == {}
    assert mcp_server.load_session_log() == {"sessions": []}


@pytest.mark.asyncio
async def test_project_and_session_error_paths(isolated_runtime: Dict[str, Path]) -> None:
    missing_project = _parse_payload(await mcp_server.call_tool("get_project", {"project": "missing"}))
    assert "error" in missing_project

    update_missing = _parse_payload(
        await mcp_server.call_tool("update_project", {"project": "missing", "updates": {"completion": 10}})
    )
    assert update_missing["error"] == "Project not found"

    archive_missing = _parse_payload(await mcp_server.call_tool("archive_project", {"project": "missing"}))
    assert archive_missing["error"] == "Project not found"

    stats_missing = _parse_payload(await mcp_server.call_tool("get_project_stats", {"project": "missing"}))
    assert stats_missing["error"] == "Project not found"

    active_none = _parse_payload(await mcp_server.call_tool("get_active_project", {}))
    assert active_none["error"] == "No active project"
    set_active_missing = _parse_payload(await mcp_server.call_tool("set_active_project", {"project": "missing"}))
    assert set_active_missing["error"] == "Project not found"

    current_none = _parse_payload(await mcp_server.call_tool("get_current_session", {}))
    assert current_none["error"] == "No sessions yet"

    end_none = _parse_payload(await mcp_server.call_tool("end_session", {"summary": "done"}))
    assert end_none["error"] == "No active session to end"


@pytest.mark.asyncio
async def test_search_files_error_and_context_truncation(
    isolated_runtime: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _BrokenPath:
        def rglob(self, _: str) -> Any:
            raise RuntimeError("rglob failed")

    monkeypatch.setattr(mcp_server, "REL_PATH", _BrokenPath())
    search_error = _parse_payload(await mcp_server.call_tool("search_files", {"query": "x"}))
    assert "error" in search_error

    # Restore proper path for context test.
    monkeypatch.setattr(mcp_server, "REL_PATH", isolated_runtime["tmp"])
    state = mcp_server.load_state()
    state["project_states"]["alpha"] = {
        "name": "Alpha project",
        "description": "alpha alpha alpha",
        "status": "active",
        "priority": "high",
        "completion": 50,
        "last_worked": "2026-02-20",
    }
    mcp_server.save_state(state)
    log = mcp_server.load_session_log()
    log["sessions"] = [
        {
            "session": 1,
            "date": "2026-02-20",
            "time": "10:00:00",
            "summary": "alpha " * 300,
            "achievements": [],
            "project": "alpha",
            "status": "active",
        }
    ]
    mcp_server.save_session_log(log)

    context = _parse_payload(await mcp_server.call_tool("load_context", {"query": "alpha", "max_tokens": 100}))
    assert context["truncated"] is True


class _FakeBrain:
    def __init__(self) -> None:
        self.last_ingest_state: Dict[str, Any] | None = None
        self.last_ingest_log: Dict[str, Any] | None = None

    def initialize(self) -> None:
        return None

    def get_stats(self) -> Dict[str, Any]:
        return {"documents": 3}

    def ingest_text(self, *_: Any, **__: Any) -> int:
        return 1

    def ingest_from_state_and_log(self, *_: Any, **__: Any) -> int:
        if _:
            self.last_ingest_state = _[0] if isinstance(_[0], dict) else None
            self.last_ingest_log = _[1] if len(_) > 1 and isinstance(_[1], dict) else None
        return 2

    def search(self, query: str, limit: int) -> list[Dict[str, Any]]:
        return [{"query": query, "score": 0.9}] * limit


class _FakeNeural:
    def learn_from_text(self, _: str) -> None:
        return None

    def save(self) -> None:
        return None

    def get_stats(self) -> Dict[str, Any]:
        return {"concepts": 5}

    def get_related_concepts(self, concept: str, limit: int) -> list[Dict[str, Any]]:
        return [{"concept": concept, "weight": 0.8}] * max(limit, 1)

    def get_strongest_patterns(self, limit: int) -> list[Dict[str, Any]]:
        return [
            {"source": "api", "target": "auth", "weight": 0.9, "strength": 0.8},
            {"source": "", "target": "skip", "weight": 0.1, "strength": 0.1},
        ][:limit]

    def apply_decay(self, days_threshold: int = 7, decay_amount: float = 0.01) -> None:
        _ = (days_threshold, decay_amount)
        return None


@pytest.mark.asyncio
async def test_brain_neural_success_paths(
    isolated_runtime: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_brain = _FakeBrain()
    fake_neural = _FakeNeural()
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: fake_brain)
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: fake_neural)

    await mcp_server.call_tool("create_project", {"key": "alpha", "name": "Alpha"})
    await mcp_server.call_tool("set_active_project", {"project": "alpha"})

    logged = _parse_payload(await mcp_server.call_tool("log_session", {"summary": "worked on alpha"}))
    assert logged["success"] is True

    semantic = _parse_payload(await mcp_server.call_tool("semantic_search", {"query": "alpha", "limit": 2}))
    assert semantic["count"] == 2

    learned = _parse_payload(await mcp_server.call_tool("neural_learn", {"text": "alpha auth integration"}))
    assert learned["success"] is True

    related = _parse_payload(await mcp_server.call_tool("neural_get_related", {"concept": "alpha", "limit": 2}))
    assert related["count"] >= 1

    patterns = _parse_payload(await mcp_server.call_tool("neural_get_patterns", {"limit": 2}))
    assert patterns["count"] >= 1

    decayed = _parse_payload(await mcp_server.call_tool("neural_apply_decay", {"days_threshold": 2}))
    assert decayed["success"] is True

    analytics = _parse_payload(await mcp_server.call_tool("get_analytics", {}))
    assert analytics["brain"]["documents"] == 3
    assert analytics["neural_web"]["concepts"] == 5

    graph = _parse_payload(await mcp_server.call_tool("get_knowledge_graph", {}))
    assert graph["stats"]["total_nodes"] >= 1
    assert graph["stats"]["total_edges"] >= 1

    smart = _parse_payload(await mcp_server.call_tool("smart_load", {"query": "alpha"}))
    assert smart["loaded"] is True
    assert smart["ingested_to_brain"] == 2
    assert smart["ingestion_scope"] == "query_matched"
    assert fake_brain.last_ingest_state is not None
    assert fake_brain.last_ingest_log is not None
    assert set(fake_brain.last_ingest_state.get("project_states", {}).keys()) == {"alpha"}
    assert len(fake_brain.last_ingest_log.get("sessions", [])) >= 1


@pytest.mark.asyncio
async def test_brain_neural_error_paths(
    isolated_runtime: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _ErrorBrain(_FakeBrain):
        def initialize(self) -> None:
            raise RuntimeError("brain-init-fail")

        def search(self, query: str, limit: int) -> list[Dict[str, Any]]:
            raise RuntimeError("brain-search-fail")

        def ingest_from_state_and_log(self, *_: Any, **__: Any) -> int:
            raise RuntimeError("brain-ingest-fail")

    class _ErrorNeural(_FakeNeural):
        def get_stats(self) -> Dict[str, Any]:
            raise RuntimeError("neural-stats-fail")

        def get_strongest_patterns(self, limit: int) -> list[Dict[str, Any]]:
            raise RuntimeError("neural-pattern-fail")

        def get_related_concepts(self, concept: str, limit: int) -> list[Dict[str, Any]]:
            raise RuntimeError("neural-related-fail")

        def apply_decay(self, days_threshold: int = 7, decay_amount: float = 0.01) -> None:
            _ = (days_threshold, decay_amount)
            raise RuntimeError("neural-decay-fail")

    error_brain = _ErrorBrain()
    error_neural = _ErrorNeural()
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: error_brain)
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: error_neural)

    analytics = _parse_payload(await mcp_server.call_tool("get_analytics", {}))
    assert "error" in analytics["brain"]
    assert "error" in analytics["neural_web"]

    semantic_error = _parse_payload(await mcp_server.call_tool("semantic_search", {"query": "x"}))
    assert "error" in semantic_error

    graph_error = _parse_payload(await mcp_server.call_tool("get_knowledge_graph", {}))
    assert "error" in graph_error

    smart_error = _parse_payload(await mcp_server.call_tool("smart_load", {"query": "x"}))
    assert "brain_error" in smart_error

    recs = _parse_payload(await mcp_server.call_tool("get_recommendations", {"query": "alpha"}))
    assert "recommendations" in recs

    decay_error = _parse_payload(await mcp_server.call_tool("neural_apply_decay", {"days_threshold": 1}))
    assert decay_error["success"] is False


@pytest.mark.asyncio
async def test_semantic_and_neural_not_initialized_paths(
    isolated_runtime: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: None)
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: None)

    semantic = _parse_payload(await mcp_server.call_tool("semantic_search", {"query": "q"}))
    assert "Failed to initialize brain" in semantic["error"]

    neural_learn = _parse_payload(await mcp_server.call_tool("neural_learn", {"text": "x"}))
    assert "Failed to initialize neural web" in neural_learn["error"]

    neural_related = _parse_payload(await mcp_server.call_tool("neural_get_related", {"concept": "x"}))
    assert "Failed to initialize neural web" in neural_related["error"]

    neural_patterns = _parse_payload(await mcp_server.call_tool("neural_get_patterns", {}))
    assert "Failed to initialize neural web" in neural_patterns["error"]

    neural_decay = _parse_payload(await mcp_server.call_tool("neural_apply_decay", {}))
    assert "Failed to initialize neural web" in neural_decay["error"]


@pytest.mark.asyncio
async def test_validate_and_project_success_branches(isolated_runtime: Dict[str, Path]) -> None:
    # Invalid JSON validation branch
    isolated_runtime["core"].write_text("{bad-json", encoding="utf-8")
    validate_bad = _parse_payload(await mcp_server.call_tool("validate", {}))
    assert validate_bad["valid"] is False

    # Restore valid state and exercise success branches.
    isolated_runtime["core"].write_text(
        json.dumps(
            {
                "system_state": {"status": "OK"},
                "current_context": {"active_project": None},
                "project_states": {},
                "recent_wins": [],
                "active_ideas": [],
                "flags": {},
            }
        ),
        encoding="utf-8",
    )
    _ = _parse_payload(await mcp_server.call_tool("create_project", {"key": "p1", "name": "P1"}))
    list_filtered = _parse_payload(await mcp_server.call_tool("list_projects", {"filter": "active"}))
    assert "p1" in list_filtered

    updated = _parse_payload(
        await mcp_server.call_tool("update_project", {"project": "p1", "updates": {"completion": 80}})
    )
    assert updated["success"] is True

    _ = _parse_payload(await mcp_server.call_tool("set_active_project", {"project": "p1"}))
    active = _parse_payload(await mcp_server.call_tool("get_active_project", {}))
    assert active["name"] == "P1"

    archived = _parse_payload(await mcp_server.call_tool("archive_project", {"project": "p1"}))
    assert archived["success"] is True


@pytest.mark.asyncio
async def test_recommendations_preview_and_neural_exception_subpaths(
    isolated_runtime: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Build state with urgency/stalled/near-done and wins for recommendation branches.
    state = mcp_server.load_state()
    state["project_states"] = {
        "near_done": {
            "name": "Near Done",
            "description": "alpha work",
            "status": "active",
            "priority": "critical",
            "completion": 90,
            "last_worked": "2026-01-01",
        },
        "stalled": {
            "name": "Stalled Project",
            "description": "alpha backlog",
            "status": "active",
            "priority": "high",
            "completion": 20,
            "last_worked": "2026-01-01",
        },
    }
    state["recent_wins"] = [{"win": "alpha milestone", "impact": "high"}]
    mcp_server.save_state(state)
    mcp_server.save_session_log(
        {
            "sessions": [
                {
                    "session": "one",  # trigger fallback numbering branch
                    "date": "2026-02-20",
                    "time": "09:00:00",
                    "summary": "alpha related session",
                    "achievements": [],
                    "project": "near_done",
                    "status": "active",
                },
                {
                    "session": 2,
                    "date": "2026-02-20",
                    "time": "09:30:00",
                    "summary": "alpha second session",
                    "achievements": [],
                    "project": "stalled",
                    "status": "active",
                },
            ]
        }
    )

    class _RecsNeural:
        def get_related_concepts(self, *_: Any, **__: Any) -> list[dict[str, Any]]:
            return [{"concept": "alpha", "weight": 0.9}]

    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: _RecsNeural())
    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: _FakeBrain())

    # Cover log_session numbering fallback and brain/neural skip/success branches.
    logged = _parse_payload(await mcp_server.call_tool("log_session", {"summary": "alpha new"}))
    assert logged["success"] is True

    preview = _parse_payload(await mcp_server.call_tool("get_loading_preview", {"query": "alpha"}))
    assert preview["total_sources"] >= 1

    recs = _parse_payload(await mcp_server.call_tool("get_recommendations", {"query": "alpha"}))
    assert recs["total"] >= 1


@pytest.mark.asyncio
async def test_tool_specific_exception_and_outer_exception_handler(
    isolated_runtime: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _BoomNeural:
        def learn_from_text(self, _: str) -> None:
            raise RuntimeError("learn boom")

        def save(self) -> None:
            return None

        def get_related_concepts(self, *_: Any, **__: Any) -> list[dict[str, Any]]:
            raise RuntimeError("related boom")

        def get_strongest_patterns(self, *_: Any, **__: Any) -> list[dict[str, Any]]:
            raise RuntimeError("patterns boom")

    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: _BoomNeural())

    learn = _parse_payload(await mcp_server.call_tool("neural_learn", {"text": "x"}))
    assert learn["success"] is False
    related = _parse_payload(await mcp_server.call_tool("neural_get_related", {"concept": "x"}))
    assert "error" in related
    patterns = _parse_payload(await mcp_server.call_tool("neural_get_patterns", {"limit": 2}))
    assert "error" in patterns

    # Trigger outer exception handler.
    monkeypatch.setattr(mcp_server, "load_state", lambda: None)
    errored = _parse_payload(await mcp_server.call_tool("get_stats", {}))
    assert "error" in errored


@pytest.mark.asyncio
async def test_main_entrypoint_with_mocked_stdio(monkeypatch: pytest.MonkeyPatch) -> None:
    class _DummyStdio:
        async def __aenter__(self) -> tuple[str, str]:
            return ("read", "write")

        async def __aexit__(self, exc_type, exc, tb) -> bool:  # type: ignore[no-untyped-def]
            _ = (exc_type, exc, tb)
            return False

    calls: Dict[str, Any] = {}

    async def _fake_run(read_stream: str, write_stream: str, options: Any) -> None:
        calls["read"] = read_stream
        calls["write"] = write_stream
        calls["options"] = options

    monkeypatch.setattr(mcp_server, "stdio_server", lambda: _DummyStdio())
    monkeypatch.setattr(mcp_server.app, "run", _fake_run)

    await mcp_server.main()
    assert calls["read"] == "read"
    assert calls["write"] == "write"


@pytest.mark.asyncio
async def test_main_entrypoint_with_unavailable_brain_and_neural(monkeypatch: pytest.MonkeyPatch) -> None:
    class _DummyStdio:
        async def __aenter__(self) -> tuple[str, str]:
            return ("read2", "write2")

        async def __aexit__(self, exc_type, exc, tb) -> bool:  # type: ignore[no-untyped-def]
            _ = (exc_type, exc, tb)
            return False

    async def _fake_run(read_stream: str, write_stream: str, options: Any) -> None:
        _ = (read_stream, write_stream, options)
        return None

    monkeypatch.setattr(mcp_server, "stdio_server", lambda: _DummyStdio())
    monkeypatch.setattr(mcp_server.app, "run", _fake_run)
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", False)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", False)
    await mcp_server.main()


@pytest.mark.asyncio
async def test_load_context_preview_and_recommendation_exception_paths(
    isolated_runtime: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    state = mcp_server.load_state()
    state["project_states"] = {
        "alpha": {
            "name": "Alpha",
            "description": "Alpha desc",
            "status": "active",
            "priority": "high",
            "completion": 75,
            "last_worked": "2026-02-01",
        }
    }
    state["recent_wins"] = [{"win": "Alpha victory", "impact": "high"}]
    state["active_ideas"] = ["idea one"]
    mcp_server.save_state(state)
    mcp_server.save_session_log(
        {
            "sessions": [
                {
                    "session": 1,
                    "date": "2026-02-20",
                    "time": "08:00:00",
                    "summary": "Alpha summary",
                    "achievements": [],
                    "project": "alpha",
                    "status": "active",
                }
            ]
        }
    )

    class _ErrBrain:
        def search(self, *_: Any, **__: Any) -> list[dict[str, Any]]:
            raise RuntimeError("brain context fail")

    class _ErrNeural:
        def get_related_concepts(self, *_: Any, **__: Any) -> list[dict[str, Any]]:
            raise RuntimeError("neural context fail")

    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: _ErrBrain())
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: _ErrNeural())

    load_context = _parse_payload(await mcp_server.call_tool("load_context", {"query": "alpha", "max_tokens": 200}))
    assert "context" in load_context

    # Force overall load_context exception branch.
    monkeypatch.setattr(mcp_server, "load_session_log", lambda: None)
    load_context_error = _parse_payload(await mcp_server.call_tool("load_context", {"query": "alpha", "max_tokens": 200}))
    assert "error" in load_context_error
    monkeypatch.setattr(mcp_server, "load_session_log", lambda: {"sessions": []})

    # Force get_loading_preview exception branch.
    monkeypatch.setattr(mcp_server, "load_state", lambda: None)
    preview_error = _parse_payload(await mcp_server.call_tool("get_loading_preview", {"query": "alpha"}))
    assert "error" in preview_error
    monkeypatch.setattr(mcp_server, "load_state", lambda: state)

    # Force recommendations exception branch.
    monkeypatch.setattr(mcp_server, "analyze_context_pressure", lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("boom")))
    rec_error = _parse_payload(await mcp_server.call_tool("get_recommendations", {"query": "alpha"}))
    assert "error" in rec_error
