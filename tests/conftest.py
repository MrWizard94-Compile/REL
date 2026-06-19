"""Shared test fixtures for REL tests"""

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator

import pytest


@pytest.fixture
def temp_rel_dir() -> Generator[Path, None, None]:
    """Create temporary REL directory for testing

    Yields:
        Path: Temporary directory path

    The directory is automatically cleaned up after the test.
    """
    temp_dir = Path(tempfile.mkdtemp())
    data_dir = temp_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Create empty state files
    core_state: Dict[str, Any] = {
        "system_state": {"status": "TEST_MODE", "session_count": 0},
        "current_context": {"current_focus": "Testing", "active_project": None},
        "project_states": {},
        "recent_wins": [],
        "active_ideas": [],
        "flags": {},
    }

    session_log: Dict[str, Any] = {"sessions": []}

    (data_dir / "CoreState.json").write_text(json.dumps(core_state, indent=2))
    (data_dir / "SessionLog.json").write_text(json.dumps(session_log, indent=2))

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_state() -> Dict[str, Any]:
    """Sample CoreState for testing

    Returns:
        Dict: Sample state dictionary
    """
    return {
        "system_state": {"status": "ACTIVE", "session_count": 5},
        "current_context": {
            "current_focus": "Building neural web",
            "active_project": "neural_web",
        },
        "project_states": {
            "neural_web": {
                "name": "Neural Web Learning System",
                "description": "Implement neural learning",
                "status": "active",
                "priority": "high",
                "completion": 75,
                "created": "2026-02-10",
                "last_worked": "2026-02-17",
            },
            "rel_development": {
                "name": "REL Development",
                "description": "Core REL system",
                "status": "complete",
                "priority": "critical",
                "completion": 100,
                "created": "2026-02-01",
                "last_worked": "2026-02-16",
            },
        },
        "recent_wins": [
            {
                "date": "2026-02-17",
                "win": "Completed neural web integration",
                "impact": "high",
            },
            {
                "date": "2026-02-16",
                "win": "Rebuilt REL system after corruption",
                "impact": "high",
            },
        ],
        "active_ideas": [
            "Add semantic search to neural web",
            "Implement auto-learning from sessions",
            "Create cognitive modules",
        ],
        "flags": {
            "foundation_complete": True,
            "all_tools_implemented": True,
            "ready_for_cognitive_modules": True,
        },
    }


@pytest.fixture
def sample_session_log() -> Dict[str, Any]:
    """Sample SessionLog for testing

    Returns:
        Dict: Sample session log dictionary
    """
    return {
        "sessions": [
            {
                "session": 1,
                "date": "2026-02-15",
                "time": "10:30:00",
                "summary": "Started building neural web module",
                "achievements": [
                    "Created Neuron class",
                    "Created Synapse class",
                    "Implemented connection strengthening",
                ],
                "project": "neural_web",
                "status": "ended",
            },
            {
                "session": 2,
                "date": "2026-02-16",
                "time": "14:00:00",
                "summary": "Completed neural web integration",
                "achievements": [
                    "Added auto-learning from sessions",
                    "Integrated with MCP server",
                    "Added 4 neural learning tools",
                ],
                "project": "neural_web",
                "status": "ended",
            },
            {
                "session": 3,
                "date": "2026-02-17",
                "time": "09:00:00",
                "summary": "Testing and refinement",
                "achievements": ["Added pattern detection", "Tested concept extraction"],
                "project": "neural_web",
                "status": "active",
            },
        ]
    }


@pytest.fixture
def brain_path(temp_rel_dir: Path) -> Path:
    """Create brain directory path

    Args:
        temp_rel_dir: Temporary REL directory fixture

    Returns:
        Path: Brain directory path
    """
    brain_dir = temp_rel_dir / "data" / "brain"
    brain_dir.mkdir(parents=True, exist_ok=True)
    return brain_dir


@pytest.fixture
def neural_web_path(temp_rel_dir: Path) -> Path:
    """Create neural web directory path

    Args:
        temp_rel_dir: Temporary REL directory fixture

    Returns:
        Path: Neural web directory path
    """
    neural_dir = temp_rel_dir / "data" / "neural_web"
    neural_dir.mkdir(parents=True, exist_ok=True)
    return neural_dir
