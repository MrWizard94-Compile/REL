from __future__ import annotations

import asyncio
import builtins
import json
import logging
import os
import runpy
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict

import pytest

import mcp_server


def _parse_payload(response: Any) -> Dict[str, Any]:
    assert isinstance(response, list)
    assert len(response) == 1
    return json.loads(response[0].text)


@pytest.fixture
def runtime_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Dict[str, Path]:
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

    monkeypatch.setattr(mcp_server, "AUTH_REQUIRED", False)
    monkeypatch.setattr(mcp_server, "AUTH_BEARER_TOKEN", None)
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", False)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", False)
    monkeypatch.setattr(mcp_server, "_brain", None)
    monkeypatch.setattr(mcp_server, "_neural_web", None)

    mcp_server.ensure_data_paths()

    return {"tmp": tmp_path, "core": core_path, "session": session_path}


def test_configure_logging_instances_and_data_path_warning(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("REL_LOG_FORMAT", "text")
    mcp_server.configure_logging()
    root = logging.getLogger()
    assert root.handlers
    assert type(root.handlers[0].formatter).__name__ == "Formatter"

    brain_sentinel = object()
    neural_sentinel = object()
    monkeypatch.setattr(mcp_server, "_brain", None)
    monkeypatch.setattr(mcp_server, "_neural_web", None)
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_brain", lambda _path: brain_sentinel)
    monkeypatch.setattr(mcp_server, "get_neural_web", lambda _path: neural_sentinel)
    assert mcp_server.get_brain_instance() is brain_sentinel
    assert mcp_server.get_neural_web_instance() is neural_sentinel

    class _BadPath:
        def mkdir(self, *args: Any, **kwargs: Any) -> None:
            _ = (args, kwargs)
            raise OSError("forced-mkdir-failure")

        def __str__(self) -> str:
            return "bad-path"

    monkeypatch.setattr(mcp_server, "REL_PATH", _BadPath())
    monkeypatch.setattr(mcp_server, "DATA_PATH", tmp_path / "data")
    monkeypatch.setattr(mcp_server, "BRAIN_PATH", tmp_path / "brain")
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_PATH", tmp_path / "neural")
    monkeypatch.setattr(mcp_server, "SNAPSHOTS_PATH", tmp_path / "snapshots")
    mcp_server.ensure_data_paths()


def test_load_state_and_session_log_missing_and_invalid_shape(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    missing_core = tmp_path / "missing_core.json"
    missing_log = tmp_path / "missing_log.json"
    monkeypatch.setattr(mcp_server, "CORE_STATE_PATH", missing_core)
    monkeypatch.setattr(mcp_server, "SESSION_LOG_PATH", missing_log)
    assert mcp_server.load_state() == {}
    assert mcp_server.load_session_log() == {"sessions": []}

    invalid_shape_log = tmp_path / "invalid_shape_log.json"
    invalid_shape_log.write_text(json.dumps({"not_sessions": True}), encoding="utf-8")
    monkeypatch.setattr(mcp_server, "SESSION_LOG_PATH", invalid_shape_log)
    assert mcp_server.load_session_log() == {"sessions": []}


def test_atomic_write_error_cleanup_and_zero_retry_atomic_update(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    target = tmp_path / "atomic.json"

    def _raise_replace(*args: Any, **kwargs: Any) -> None:
        _ = (args, kwargs)
        raise OSError("replace failed")

    def _raise_unlink(*args: Any, **kwargs: Any) -> None:
        _ = (args, kwargs)
        raise OSError("unlink failed")

    monkeypatch.setattr(os, "replace", _raise_replace)
    monkeypatch.setattr(os, "unlink", _raise_unlink)
    with pytest.raises(OSError):
        mcp_server.atomic_write_json(target, {"x": 1})

    with pytest.raises(mcp_server.VersionConflictError):
        mcp_server.atomic_update(
            tmp_path / "never.json",
            tmp_path / "never.lock",
            lambda cur: cur,
            max_retries=0,
        )


def test_file_lock_unix_paths_and_timeout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _FcntlWithUnlockError:
        LOCK_EX = 1
        LOCK_NB = 2
        LOCK_UN = 8

        def __init__(self) -> None:
            self.acquire_attempts = 0
            self.unlock_called = False

        def flock(self, _fileno: int, flags: int) -> None:
            if flags == (self.LOCK_EX | self.LOCK_NB):
                self.acquire_attempts += 1
                if self.acquire_attempts == 1:
                    raise OSError("busy")
                return None
            if flags == self.LOCK_UN:
                self.unlock_called = True
                raise OSError("unlock-fail")

    fake_fcntl = _FcntlWithUnlockError()
    monkeypatch.setattr(mcp_server.sys, "platform", "linux")
    monkeypatch.setattr(mcp_server, "fcntl", fake_fcntl, raising=False)
    with mcp_server.file_lock(tmp_path / "unix.lock", timeout=0.3):
        pass
    assert fake_fcntl.acquire_attempts >= 2
    assert fake_fcntl.unlock_called is True

    class _AlwaysBusyFcntl:
        LOCK_EX = 1
        LOCK_NB = 2
        LOCK_UN = 8

        def flock(self, _fileno: int, flags: int) -> None:
            if flags == (self.LOCK_EX | self.LOCK_NB):
                raise OSError("always busy")

    monkeypatch.setattr(mcp_server, "fcntl", _AlwaysBusyFcntl(), raising=False)
    with pytest.raises(TimeoutError):
        with mcp_server.file_lock(tmp_path / "timeout.lock", timeout=0.0):
            pass


def test_cognitive_branch_coverage_targets() -> None:
    assert mcp_server.get_staleness_multiplier(
        {"status": "complete", "completion": 1, "last_worked": "2026-01-01"}
    ) == 0.0

    medium_state = {
        "project_states": {
            "high_only": {
                "name": "High Only",
                "description": "medium pressure target",
                "status": "active",
                "priority": "high",
                "completion": 50,
                "last_worked": (mcp_server.datetime.now().date() - mcp_server.timedelta(days=5)).strftime(
                    "%Y-%m-%d"
                ),
            }
        }
    }
    pressure = mcp_server.analyze_context_pressure(medium_state)
    assert pressure["overall_pressure"]["level"] == "MEDIUM"

    assert mcp_server.calculate_momentum([{"summary": "x"}], days=-1) == "stalled"
    assert mcp_server.detect_arc_type([{"summary": "exploring new architecture"}]) == "exploration"
    assert mcp_server.detect_arc_type([{"summary": "back to this work and resuming"}]) == "recovery"
    assert mcp_server.detect_work_state([{"summary": "building a new tool"}], {}) == "creation"
    assert mcp_server.detect_work_state([{"summary": "learning advanced patterns"}], {}) == "learning"
    assert mcp_server.detect_work_state([{"summary": "planning sprint tasks"}], {}) == "planning"

    trend = mcp_server.get_affective_trends_analysis({}, {"sessions": [{"achievements": []}] * 5})
    assert trend["productivity_trend"] == "increasing"


def test_custom_sequence_branches_for_momentum_and_energy() -> None:
    class _MomentumSessions:
        def __len__(self) -> int:
            return 8

        def __iter__(self) -> Any:
            return iter([{"summary": "work", "achievements": []}] * 8)

        def __getitem__(self, item: Any) -> Any:
            if isinstance(item, slice):
                if item.start == -7 and item.stop is None:
                    return [{"summary": "work", "achievements": []}] * 20
                if item.start == -5 and item.stop is None:
                    return [{"summary": "work", "achievements": []}] * 5
                return [{"summary": "work", "achievements": []}] * 3
            return {"summary": "work", "achievements": []}

        def __bool__(self) -> bool:
            return True

    momentum_sessions = _MomentumSessions()
    assert mcp_server.detect_arc_type(momentum_sessions) == "building_momentum"
    arc = mcp_server.get_story_arc_analysis(
        {"project_states": {"p1": {"status": "active"}}, "recent_wins": []},
        {"sessions": momentum_sessions},
    )
    assert arc["momentum"] == "accelerating"

    class _EmptyRecentSessions:
        def __len__(self) -> int:
            return 8

        def __iter__(self) -> Any:
            return iter([{"achievements": ["x"]}] * 8)

        def __getitem__(self, item: Any) -> Any:
            if isinstance(item, slice):
                return []
            return {"achievements": ["x"]}

        def __bool__(self) -> bool:
            return True

    assert mcp_server.infer_energy_level(_EmptyRecentSessions()) == "low"

    class _DecreasingSessions:
        def __len__(self) -> int:
            return 4

        def __iter__(self) -> Any:
            return iter([{"summary": "steady", "achievements": []}] * 4)

        def __getitem__(self, item: Any) -> Any:
            if isinstance(item, slice):
                if item.start is None and item.stop == 2:
                    return [{"summary": "steady", "achievements": []}] * 5
                if item.start == 2 and item.stop is None:
                    return [{"summary": "steady", "achievements": []}]
                return [{"summary": "steady", "achievements": []}] * 3
            return {"summary": "steady", "achievements": []}

        def __bool__(self) -> bool:
            return True

    dec = mcp_server.get_affective_trends_analysis({}, {"sessions": _DecreasingSessions()})
    assert dec["productivity_trend"] == "decreasing"


@pytest.mark.asyncio
async def test_list_tools_validate_and_log_session_subpaths(
    runtime_env: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tools = await mcp_server.list_tools()
    assert len(tools) >= 45

    runtime_env["session"].write_text("{bad-json", encoding="utf-8")
    validate = _parse_payload(await mcp_server.call_tool("validate", {}))
    assert validate["json_ok"]["sessionLog"] is False
    runtime_env["session"].write_text(json.dumps({"sessions": []}), encoding="utf-8")

    class _BrokenBrain:
        def ingest_text(self, *_args: Any, **_kwargs: Any) -> int:
            raise RuntimeError("ingest failed")

    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: None)
    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: _BrokenBrain())

    logged = _parse_payload(await mcp_server.call_tool("log_session", {"summary": "branch session"}))
    assert logged["success"] is True

    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: None)
    logged_again = _parse_payload(await mcp_server.call_tool("log_session", {"summary": "branch session two"}))
    assert logged_again["success"] is True


@pytest.mark.asyncio
async def test_end_session_log_progress_search_and_context_fallbacks(
    runtime_env: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _ = _parse_payload(await mcp_server.call_tool("create_project", {"key": "p1", "name": "P1"}))
    _ = _parse_payload(await mcp_server.call_tool("log_session", {"summary": "active session"}))
    ended = _parse_payload(await mcp_server.call_tool("end_session", {}))
    assert ended["success"] is True

    p1_progress = _parse_payload(await mcp_server.call_tool("log_progress", {"project": "p1", "update": "u1"}))
    assert p1_progress["success"] is True
    p1_progress_2 = _parse_payload(await mcp_server.call_tool("log_progress", {"project": "p1", "update": "u2"}))
    assert p1_progress_2["success"] is True
    missing_progress = _parse_payload(
        await mcp_server.call_tool("log_progress", {"project": "missing", "update": "u3"})
    )
    assert missing_progress["error"] == "Project not found"

    state = mcp_server.load_state()
    state["project_states"]["broken"] = "not-a-dict"
    mcp_server.save_state(state)
    broken_progress = _parse_payload(await mcp_server.call_tool("log_progress", {"project": "broken", "update": "u4"}))
    assert broken_progress["error"] == "Invalid project record"

    class _BrokenStatFile:
        name = "branch-file.txt"

        def is_file(self) -> bool:
            return True

        def stat(self) -> Any:
            raise OSError("no-stat")

        def __str__(self) -> str:
            return "branch-file.txt"

    class _BrokenStatRoot:
        def rglob(self, _pattern: str) -> Any:
            return [_BrokenStatFile()]

    monkeypatch.setattr(mcp_server, "REL_PATH", _BrokenStatRoot())
    search = _parse_payload(await mcp_server.call_tool("search_files", {"query": "branch"}))
    assert search["files"][0]["name"] == "branch-file.txt"

    state_with_set = {
        "system_state": {},
        "current_context": {},
        "project_states": {},
        "recent_wins": [{"win": "branch", "meta": {1, 2}}],
        "active_ideas": [],
        "flags": {},
    }
    monkeypatch.setattr(mcp_server, "load_state", lambda: state_with_set)
    monkeypatch.setattr(mcp_server, "load_session_log", lambda: {"sessions": [{"summary": "branch"}]})
    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", False)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", False)
    ctx = _parse_payload(await mcp_server.call_tool("load_context", {"query": "branch", "max_tokens": 100}))
    assert "error" in ctx


@pytest.mark.asyncio
async def test_context_recommendation_analytics_snapshot_graph_sync_and_smart_load(
    runtime_env: Dict[str, Path],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _EmptyBrain:
        def search(self, _query: str, _limit: int) -> list[dict[str, Any]]:
            return []

    class _EmptyNeural:
        def get_related_concepts(self, _query: str, _limit: int) -> list[dict[str, Any]]:
            return []

    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: _EmptyBrain())
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: _EmptyNeural())

    context = _parse_payload(await mcp_server.call_tool("load_context", {"query": "alpha", "max_tokens": 2000}))
    assert "context" in context

    class _BadStrengthNeural:
        def get_related_concepts(self, _query: str, _limit: int) -> list[dict[str, Any]]:
            return [{"concept": "alpha", "weight": "not-a-number"}]

    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: _BadStrengthNeural())
    recs = _parse_payload(await mcp_server.call_tool("get_recommendations", {"query": "alpha"}))
    learning = [item for item in recs["recommendations"] if item.get("type") == "learning"]
    assert learning
    assert "strength: 0.00" in learning[0]["items"][0]

    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: None)
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: None)
    analytics = _parse_payload(await mcp_server.call_tool("get_analytics", {}))
    assert "brain" not in analytics
    assert "neural_web" not in analytics

    state = mcp_server.load_state()
    state["project_states"] = {
        "active_proj": {
            "name": "Active",
            "description": "active project",
            "status": "active",
            "priority": "high",
            "completion": 60,
            "last_worked": "2026-02-20",
        },
        "archived_proj": {
            "name": "Archived",
            "description": "archived project",
            "status": "archived",
            "priority": "low",
            "completion": 100,
            "last_worked": "2026-01-01",
        },
    }
    state["active_ideas"] = ["ship this branch coverage"]
    state["recent_wins"] = [{"win": "coverage branch done", "impact": "high"}]
    mcp_server.save_state(state)
    mcp_server.save_session_log(
        {
            "sessions": [
                {
                    "session": 1,
                    "date": "2026-02-20",
                    "time": "10:00:00",
                    "summary": "worked without project",
                    "achievements": [],
                    "project": None,
                    "status": "ended",
                }
            ]
        }
    )

    mcp_server.SNAPSHOTS_PATH.mkdir(parents=True, exist_ok=True)
    existing_snapshot = mcp_server.SNAPSHOTS_PATH / "collision.json"
    existing_snapshot.write_text("{}", encoding="utf-8")
    snapshot = _parse_payload(await mcp_server.call_tool("create_snapshot", {"name": "collision"}))
    assert snapshot["path"] != str(existing_snapshot)

    monkeypatch.setattr(mcp_server, "NEURAL_WEB_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_neural_web_instance", lambda: None)
    graph = _parse_payload(await mcp_server.call_tool("get_knowledge_graph", {}))
    node_types = {node.get("type") for node in graph["nodes"]}
    assert "idea" in node_types
    assert "win" in node_types

    monkeypatch.setenv("REL_OBSIDIAN_VAULT_PATH", str(runtime_env["tmp"] / "vault"))
    synced = _parse_payload(await mcp_server.call_tool("sync_obsidian", {}))
    assert synced["success"] is True
    assert synced["projects_exported"] == 1
    project_note = Path(synced["vault_path"]) / "Projects" / "active_proj.md"
    assert project_note.exists()

    monkeypatch.setattr(mcp_server, "BRAIN_AVAILABLE", True)
    monkeypatch.setattr(mcp_server, "get_brain_instance", lambda: None)
    loaded = _parse_payload(await mcp_server.call_tool("smart_load", {"query": "active"}))
    assert loaded["loaded"] is True
    assert "ingested_to_brain" not in loaded


def test_runpath_main_import_fallback_branches(monkeypatch: pytest.MonkeyPatch) -> None:
    called: Dict[str, bool] = {"run_called": False}

    def _fake_run(coro: Any) -> None:
        called["run_called"] = True
        coro.close()

    fake_fcntl = SimpleNamespace(
        LOCK_EX=1,
        LOCK_NB=2,
        LOCK_UN=8,
        flock=lambda *_args, **_kwargs: None,
    )

    original_import = builtins.__import__

    def _guarded_import(
        name: str,
        globals_dict: Any = None,
        locals_dict: Any = None,
        fromlist: Any = (),
        level: int = 0,
    ) -> Any:
        if name in {"brain_typed", "brain", "neural_web_typed", "neural_web"}:
            raise ImportError(f"forced import failure for {name}")
        return original_import(name, globals_dict, locals_dict, fromlist, level)

    original_mkdir = Path.mkdir

    def _failing_mkdir(self: Path, *args: Any, **kwargs: Any) -> None:
        _ = (args, kwargs)
        raise OSError("forced mkdir failure")

    monkeypatch.setattr(asyncio, "run", _fake_run)
    monkeypatch.setattr(sys, "platform", "linux")
    monkeypatch.setitem(sys.modules, "fcntl", fake_fcntl)
    monkeypatch.setattr(builtins, "__import__", _guarded_import)
    monkeypatch.setattr(Path, "mkdir", _failing_mkdir)

    namespace = runpy.run_path(str(Path(mcp_server.__file__)), run_name="__main__")
    assert namespace["BRAIN_AVAILABLE"] is False
    assert namespace["NEURAL_WEB_AVAILABLE"] is False
    assert called["run_called"] is True

    monkeypatch.setattr(Path, "mkdir", original_mkdir)
