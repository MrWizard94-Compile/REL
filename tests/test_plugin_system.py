from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import plugin_system as ps


def _write_plugin(
    plugin_dir: Path,
    *,
    name: str,
    version: str = "1.0.0",
    entrypoint: str = "main.py",
    enabled: bool = True,
    dependencies: list[str] | None = None,
    timeout: int = 5,
    main_code: str | None = None,
) -> None:
    plugin_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "name": name,
        "version": version,
        "description": f"{name} plugin",
        "api_version": "1.0",
        "entrypoint": entrypoint,
        "enabled": enabled,
        "dependencies": dependencies or [],
        "sandbox_timeout_seconds": timeout,
    }
    (plugin_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    if main_code is None:
        main_code = (
            "def run(payload, context=None):\n"
            "    return {'ok': True, 'plugin': 'base', 'payload': payload.get('request', {})}\n"
        )
    (plugin_dir / entrypoint).write_text(main_code, encoding="utf-8")


def test_discover_list_get_reload_and_public_record(tmp_path: Path) -> None:
    root = tmp_path / "plugins"
    manager = ps.PluginManager(root)
    _write_plugin(manager.installed_root / "p1", name="p1")

    discovered = manager.discover_plugins()
    assert "p1" in discovered
    assert manager.get_plugin("p1") is not None

    listed = manager.list_plugins()
    assert len(listed) == 1
    assert listed[0]["name"] == "p1"
    assert listed[0]["status"] == "ready"
    assert discovered["p1"].plugin_name == "p1"

    reloaded = manager.reload_plugins()
    assert "p1" in reloaded


def test_manifest_loading_defaults_and_invalid_paths(tmp_path: Path) -> None:
    manager = ps.PluginManager(tmp_path / "plugins")

    no_manifest_dir = manager.installed_root / "no_manifest"
    no_manifest_dir.mkdir(parents=True, exist_ok=True)
    assert manager._load_manifest(no_manifest_dir) is None

    bad_manifest_dir = manager.installed_root / "bad_manifest"
    bad_manifest_dir.mkdir(parents=True, exist_ok=True)
    (bad_manifest_dir / "manifest.json").write_text("{bad json", encoding="utf-8")
    assert manager._load_manifest(bad_manifest_dir) is None

    minimal_dir = manager.installed_root / "minimal"
    minimal_dir.mkdir(parents=True, exist_ok=True)
    (minimal_dir / "manifest.json").write_text(json.dumps({}), encoding="utf-8")
    manifest = manager._load_manifest(minimal_dir)
    assert manifest is not None
    assert manifest.name == "minimal"
    assert manifest.version == "0.1.0"
    assert manifest.entrypoint == "main.py"
    assert manifest.sandbox_timeout_seconds >= 1

    invalid_timeout_dir = manager.installed_root / "invalid_timeout"
    invalid_timeout_dir.mkdir(parents=True, exist_ok=True)
    (invalid_timeout_dir / "manifest.json").write_text(
        json.dumps({"name": "invalid_timeout", "sandbox_timeout_seconds": "NaN", "enabled": "false"}),
        encoding="utf-8",
    )
    invalid_manifest = manager._load_manifest(invalid_timeout_dir)
    assert invalid_manifest is not None
    assert invalid_manifest.sandbox_timeout_seconds == 15
    assert invalid_manifest.enabled is False

    whitespace_entrypoint_dir = manager.installed_root / "whitespace_entrypoint"
    whitespace_entrypoint_dir.mkdir(parents=True, exist_ok=True)
    (whitespace_entrypoint_dir / "manifest.json").write_text(
        json.dumps({"name": "whitespace_entrypoint", "entrypoint": "   ", "enabled": 0}),
        encoding="utf-8",
    )
    whitespace_manifest = manager._load_manifest(whitespace_entrypoint_dir)
    assert whitespace_manifest is not None
    assert whitespace_manifest.entrypoint == "main.py"
    assert whitespace_manifest.enabled is False

    absolute_entrypoint_dir = manager.installed_root / "absolute_entrypoint"
    absolute_entrypoint_dir.mkdir(parents=True, exist_ok=True)
    absolute_entrypoint_path = str((tmp_path / "evil.py").resolve())
    (absolute_entrypoint_dir / "manifest.json").write_text(
        json.dumps({"name": "absolute_entrypoint", "entrypoint": absolute_entrypoint_path}),
        encoding="utf-8",
    )
    assert manager._load_manifest(absolute_entrypoint_dir) is None


def test_discover_skips_non_dirs_and_missing_manifest(tmp_path: Path) -> None:
    manager = ps.PluginManager(tmp_path / "plugins")
    # Non-directory item
    (manager.installed_root / "readme.txt").write_text("x", encoding="utf-8")
    # Directory without manifest
    (manager.installed_root / "empty_dir").mkdir(parents=True, exist_ok=True)

    discovered = manager.discover_plugins()
    assert discovered == {}

    # Cover base-not-exists branch by removing one discovery root.
    manager.marketplace_root.rmdir()
    discovered_again = manager.discover_plugins()
    assert discovered_again == {}


def test_set_enabled_success_and_failure(tmp_path: Path) -> None:
    manager = ps.PluginManager(tmp_path / "plugins")
    plugin_dir = manager.installed_root / "toggle"
    _write_plugin(plugin_dir, name="toggle")
    manager.discover_plugins()

    assert manager.set_enabled("toggle", False) is True
    plugin = manager.get_plugin("toggle")
    assert plugin is not None
    assert plugin.status == "disabled"
    assert plugin.manifest.enabled is False

    assert manager.set_enabled("toggle", True) is True
    plugin = manager.get_plugin("toggle")
    assert plugin is not None
    assert plugin.status == "ready"
    assert plugin.manifest.enabled is True

    assert manager.set_enabled("missing", True) is False

    (plugin_dir / "manifest.json").write_text("{bad json", encoding="utf-8")
    assert manager.set_enabled("toggle", False) is False


def test_resolve_dependencies_and_disabled_states(tmp_path: Path) -> None:
    manager = ps.PluginManager(tmp_path / "plugins")
    _write_plugin(manager.installed_root / "dep_base", name="dep_base")
    _write_plugin(
        manager.installed_root / "dep_missing",
        name="dep_missing",
        dependencies=["nope"],
    )
    _write_plugin(
        manager.installed_root / "dep_disabled",
        name="dep_disabled",
        enabled=False,
    )
    discovered = manager.discover_plugins()

    assert discovered["dep_base"].status == "ready"
    assert discovered["dep_missing"].status == "dependency_error"
    assert "Missing dependencies" in (discovered["dep_missing"].last_error or "")
    assert discovered["dep_disabled"].status == "disabled"


class _DummyConn:
    def __init__(self, *, response: dict[str, Any] | None = None, should_poll: bool = True, raise_eof: bool = False):
        self.response = response or {}
        self.should_poll = should_poll
        self.raise_eof = raise_eof
        self.closed = False
        self.sent: list[dict[str, Any]] = []

    def poll(self, _: float) -> bool:
        return self.should_poll

    def recv(self) -> dict[str, Any]:
        if self.raise_eof:
            raise EOFError
        return self.response

    def send(self, payload: dict[str, Any]) -> None:
        self.sent.append(payload)

    def close(self) -> None:
        self.closed = True


class _FakeProcess:
    def __init__(self, *, alive: bool = False):
        self._alive = alive
        self.started = False
        self.terminated = False

    def start(self) -> None:
        self.started = True

    def join(self, timeout: float | None = None) -> None:
        _ = timeout

    def is_alive(self) -> bool:
        return self._alive

    def terminate(self) -> None:
        self.terminated = True
        self._alive = False


def _patch_mp(
    monkeypatch: Any,
    parent_conn: _DummyConn,
    *,
    process_alive: bool = False,
) -> None:
    monkeypatch.setattr(ps.mp, "Pipe", lambda duplex=False: (parent_conn, _DummyConn()))  # noqa: ARG005

    def _proc_factory(*_: Any, **__: Any) -> _FakeProcess:
        return _FakeProcess(alive=process_alive)

    monkeypatch.setattr(ps.mp, "Process", _proc_factory)


def test_plugin_worker_variants(tmp_path: Path, monkeypatch: Any) -> None:
    # Success
    success_plugin = tmp_path / "success.py"
    success_plugin.write_text("def run(payload, context=None):\n    return {'ok': True}\n", encoding="utf-8")
    success_conn = _DummyConn()
    ps._plugin_worker(str(success_plugin), {"x": 1}, success_conn)
    assert success_conn.sent[-1]["ok"] is True

    # No callable run
    no_run_plugin = tmp_path / "no_run.py"
    no_run_plugin.write_text("VALUE = 1\n", encoding="utf-8")
    no_run_conn = _DummyConn()
    ps._plugin_worker(str(no_run_plugin), {"x": 1}, no_run_conn)
    assert "callable run" in no_run_conn.sent[-1]["error"]

    # Non-serializable result
    bad_return_plugin = tmp_path / "bad_return.py"
    bad_return_plugin.write_text(
        "class X:\n    pass\n\ndef run(payload, context=None):\n    return X()\n",
        encoding="utf-8",
    )
    bad_conn = _DummyConn()
    ps._plugin_worker(str(bad_return_plugin), {"x": 1}, bad_conn)
    assert "non-JSON-serializable" in bad_conn.sent[-1]["error"]

    # Exception in run
    raise_plugin = tmp_path / "raise_plugin.py"
    raise_plugin.write_text("def run(payload, context=None):\n    raise RuntimeError('boom')\n", encoding="utf-8")
    raise_conn = _DummyConn()
    ps._plugin_worker(str(raise_plugin), {"x": 1}, raise_conn)
    assert "boom" in raise_conn.sent[-1]["error"]

    # spec loader unavailable
    monkeypatch.setattr(ps.importlib.util, "spec_from_file_location", lambda *_args, **_kwargs: None)
    spec_conn = _DummyConn()
    ps._plugin_worker(str(success_plugin), {"x": 1}, spec_conn)
    assert "Could not load plugin module" in spec_conn.sent[-1]["error"]


def test_execute_plugin_success_and_missing_cases(tmp_path: Path, monkeypatch: Any) -> None:
    manager = ps.PluginManager(tmp_path / "plugins")
    _write_plugin(
        manager.installed_root / "good",
        name="good",
        main_code=(
            "def run(payload, context=None):\n"
            "    return {'plugin': 'good', 'subject': payload.get('principal', {}).get('subject')}\n"
        ),
    )
    manager.discover_plugins()

    parent_conn = _DummyConn(response={"ok": True, "result": {"plugin": "good"}}, should_poll=True)
    _patch_mp(monkeypatch, parent_conn, process_alive=False)

    ok, result = manager.execute_plugin("good", {"principal": {"subject": "u1"}})
    assert ok is True
    assert result["result"]["plugin"] == "good"

    record = manager.get_plugin("good")
    assert record is not None
    assert record.last_run_at is not None

    missing_ok, missing = manager.execute_plugin("nope", {})
    assert missing_ok is False
    assert "not found" in missing["error"]


def test_execute_plugin_disabled_dependency_missing_entrypoint(tmp_path: Path) -> None:
    manager = ps.PluginManager(tmp_path / "plugins")
    _write_plugin(manager.installed_root / "disabled", name="disabled", enabled=False)
    _write_plugin(
        manager.installed_root / "dep_err",
        name="dep_err",
        dependencies=["not_installed"],
    )
    _write_plugin(
        manager.installed_root / "no_entry",
        name="no_entry",
        entrypoint="runner.py",
    )
    _write_plugin(
        manager.installed_root / "path_escape",
        name="path_escape",
        entrypoint="../outside.py",
    )
    (manager.installed_root / "no_entry" / "runner.py").unlink()
    manager.discover_plugins()

    ok_disabled, payload_disabled = manager.execute_plugin("disabled", {})
    assert ok_disabled is False
    assert "disabled" in payload_disabled["error"].lower()

    ok_dep, payload_dep = manager.execute_plugin("dep_err", {})
    assert ok_dep is False
    assert "dependency" in payload_dep["error"].lower() or "missing dependencies" in payload_dep["error"].lower()

    ok_entry, payload_entry = manager.execute_plugin("no_entry", {})
    assert ok_entry is False
    assert "Entrypoint not found" in payload_entry["error"]

    ok_escape, payload_escape = manager.execute_plugin("path_escape", {})
    assert ok_escape is False
    assert "inside plugin directory" in payload_escape["error"]


def test_execute_plugin_timeout_and_error_variants(tmp_path: Path, monkeypatch: Any) -> None:
    manager = ps.PluginManager(tmp_path / "plugins")
    _write_plugin(
        manager.installed_root / "sleepy",
        name="sleepy",
        timeout=1,
        main_code=(
            "import time\n"
            "def run(payload, context=None):\n"
            "    time.sleep(2)\n"
            "    return {'done': True}\n"
        ),
    )
    _write_plugin(
        manager.installed_root / "no_run",
        name="no_run",
        main_code="VALUE = 42\n",
    )
    _write_plugin(
        manager.installed_root / "bad_return",
        name="bad_return",
        main_code=(
            "class X:\n"
            "    pass\n"
            "def run(payload, context=None):\n"
            "    return X()\n"
        ),
    )
    _write_plugin(
        manager.installed_root / "raising",
        name="raising",
        main_code=(
            "def run(payload, context=None):\n"
            "    raise RuntimeError('boom')\n"
        ),
    )
    manager.discover_plugins()

    timeout_conn = _DummyConn(response={"ok": True, "result": {"done": True}}, should_poll=True)
    _patch_mp(monkeypatch, timeout_conn, process_alive=True)
    timeout_ok, timeout_payload = manager.execute_plugin("sleepy", {})
    assert timeout_ok is False
    assert "timed out" in timeout_payload["error"].lower()

    eof_conn = _DummyConn(should_poll=True, raise_eof=True)
    _patch_mp(monkeypatch, eof_conn, process_alive=False)
    bad_ok, bad_payload = manager.execute_plugin("bad_return", {})
    assert bad_ok is False
    assert "ended unexpectedly" in bad_payload["error"].lower()

    no_result_conn = _DummyConn(should_poll=False)
    _patch_mp(monkeypatch, no_result_conn, process_alive=False)
    raise_ok, raise_payload = manager.execute_plugin("raising", {})
    assert raise_ok is False
    assert "no result" in raise_payload["error"].lower()

    # Poll + explicit error payload
    error_conn = _DummyConn(response={"ok": False, "error": "worker-fail"}, should_poll=True)
    _patch_mp(monkeypatch, error_conn, process_alive=False)
    no_run_ok, no_run_payload = manager.execute_plugin("no_run", {})
    assert no_run_ok is False
    assert "worker-fail" in no_run_payload["error"]
