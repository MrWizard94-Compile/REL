"""
Plugin system for REL.

Features:
- Plugin discovery and manifest loading
- Version/dependency metadata checks
- Enable/disable and hot-reload support
- Sandboxed execution in a separate process with timeout
"""

from __future__ import annotations

import importlib.util
import json
import multiprocessing as mp
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class PluginManifest:
    """Plugin manifest metadata."""

    name: str
    version: str
    description: str = ""
    api_version: str = "1.0"
    entrypoint: str = "main.py"
    dependencies: List[str] = field(default_factory=list)
    enabled: bool = True
    sandbox_timeout_seconds: int = 15


@dataclass
class PluginRecord:
    """Discovered plugin and runtime metadata."""

    manifest: PluginManifest
    plugin_dir: Path
    discovered_at: float
    status: str = "ready"
    last_error: Optional[str] = None
    last_run_at: Optional[float] = None

    @property
    def plugin_name(self) -> str:
        return self.manifest.name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.manifest.name,
            "version": self.manifest.version,
            "description": self.manifest.description,
            "api_version": self.manifest.api_version,
            "entrypoint": self.manifest.entrypoint,
            "dependencies": list(self.manifest.dependencies),
            "enabled": self.manifest.enabled,
            "sandbox_timeout_seconds": self.manifest.sandbox_timeout_seconds,
            "status": self.status,
            "last_error": self.last_error,
            "last_run_at": self.last_run_at,
            "path": str(self.plugin_dir),
        }


def _plugin_worker(entrypoint: str, payload: Dict[str, Any], conn: Any) -> None:
    """Execute plugin code in an isolated process."""
    try:
        spec = importlib.util.spec_from_file_location("rel_plugin_module", entrypoint)
        if spec is None or spec.loader is None:
            conn.send({"ok": False, "error": f"Could not load plugin module from {entrypoint}"})
            return
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        run_fn = getattr(module, "run", None)
        if not callable(run_fn):
            conn.send({"ok": False, "error": "Plugin entrypoint must define callable run(payload, context=None)."})
            return

        result = run_fn(payload, context={"sandboxed": True, "runtime": "rel"})
        if not isinstance(result, (dict, list, str, int, float, bool, type(None))):
            conn.send({"ok": False, "error": "Plugin returned a non-JSON-serializable type."})
            return

        conn.send({"ok": True, "result": result})
    except Exception as exc:  # pragma: no cover - process boundary
        conn.send({"ok": False, "error": str(exc)})
    finally:
        conn.close()


class PluginManager:
    """Discover and execute REL plugins."""

    def __init__(self, plugin_root: Path) -> None:
        self.plugin_root = plugin_root
        self.marketplace_root = self.plugin_root / "marketplace"
        self.installed_root = self.plugin_root / "installed"
        # Re-entrant lock avoids deadlock when dependency resolution is invoked
        # from a code-path that already holds the manager lock.
        self._lock = threading.RLock()
        self._plugins: Dict[str, PluginRecord] = {}

        self.plugin_root.mkdir(parents=True, exist_ok=True)
        self.marketplace_root.mkdir(parents=True, exist_ok=True)
        self.installed_root.mkdir(parents=True, exist_ok=True)

    def discover_plugins(self) -> Dict[str, PluginRecord]:
        """Discover plugins under installed and marketplace roots."""
        discovered: Dict[str, PluginRecord] = {}
        for base in (self.installed_root, self.marketplace_root):
            if not base.exists():
                continue
            for item in base.iterdir():
                if not item.is_dir():
                    continue
                manifest = self._load_manifest(item)
                if manifest is None:
                    continue
                discovered[manifest.name] = PluginRecord(
                    manifest=manifest,
                    plugin_dir=item,
                    discovered_at=time.time(),
                )
        with self._lock:
            self._plugins = discovered
            self._resolve_dependencies()
            return dict(self._plugins)

    def reload_plugins(self) -> Dict[str, PluginRecord]:
        """Hot-reload all plugins from disk."""
        return self.discover_plugins()

    def list_plugins(self) -> List[Dict[str, Any]]:
        with self._lock:
            records = list(self._plugins.values())
        return [record.to_dict() for record in records]

    def get_plugin(self, plugin_name: str) -> Optional[PluginRecord]:
        with self._lock:
            return self._plugins.get(plugin_name)

    def set_enabled(self, plugin_name: str, enabled: bool) -> bool:
        record = self.get_plugin(plugin_name)
        if record is None:
            return False
        manifest_path = record.plugin_dir / "manifest.json"
        try:
            raw = json.loads(manifest_path.read_text(encoding="utf-8"))
            raw["enabled"] = enabled
            manifest_path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
        except Exception:
            return False
        with self._lock:
            record.manifest.enabled = enabled
            record.status = "ready" if enabled else "disabled"
            record.last_error = None
        return True

    def execute_plugin(self, plugin_name: str, payload: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]:
        """Execute plugin in a separate process with timeout."""
        record = self.get_plugin(plugin_name)
        if record is None:
            return False, {"error": f"Plugin not found: {plugin_name}"}
        if not record.manifest.enabled:
            return False, {"error": f"Plugin disabled: {plugin_name}"}
        if record.status == "dependency_error":
            return False, {"error": record.last_error or "Dependency error"}

        entrypoint = (record.plugin_dir / record.manifest.entrypoint).resolve()
        plugin_root = record.plugin_dir.resolve()
        if entrypoint != plugin_root and plugin_root not in entrypoint.parents:
            with self._lock:
                record.status = "error"
                record.last_error = "Entrypoint must resolve inside plugin directory."
            return False, {"error": record.last_error}
        if not entrypoint.exists():
            with self._lock:
                record.status = "error"
                record.last_error = f"Entrypoint not found: {entrypoint}"
            return False, {"error": record.last_error}

        parent_conn, child_conn = mp.Pipe(duplex=False)
        proc = mp.Process(target=_plugin_worker, args=(str(entrypoint), payload, child_conn))
        proc.start()
        proc.join(timeout=max(record.manifest.sandbox_timeout_seconds, 1))

        if proc.is_alive():
            proc.terminate()
            proc.join(timeout=1)
            with self._lock:
                record.status = "timeout"
                record.last_error = "Plugin timed out."
            return False, {"error": "Plugin timed out."}

        response: Dict[str, Any] = {"ok": False, "error": "Plugin returned no result."}
        if parent_conn.poll(0.1):
            try:
                response = parent_conn.recv()
            except EOFError:
                response = {"ok": False, "error": "Plugin process ended unexpectedly."}
        parent_conn.close()

        with self._lock:
            record.last_run_at = time.time()
            if response.get("ok"):
                record.status = "ready"
                record.last_error = None
                return True, {"result": response.get("result")}
            record.status = "error"
            record.last_error = str(response.get("error", "Plugin execution failed."))
            return False, {"error": record.last_error}

    def _load_manifest(self, plugin_dir: Path) -> Optional[PluginManifest]:
        manifest_path = plugin_dir / "manifest.json"
        if not manifest_path.exists():
            return None

        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            return None

        name = str(data.get("name") or plugin_dir.name)
        version = str(data.get("version") or "0.1.0")
        description = str(data.get("description") or "")
        api_version = str(data.get("api_version") or "1.0")
        entrypoint = str(data.get("entrypoint") or "main.py").strip()
        if not entrypoint:
            entrypoint = "main.py"
        entrypoint_path = Path(entrypoint)
        if entrypoint_path.is_absolute():
            return None

        dependencies = [
            str(dep).strip()
            for dep in data.get("dependencies", [])
            if str(dep).strip()
        ]
        enabled_raw = data.get("enabled", True)
        if isinstance(enabled_raw, bool):
            enabled = enabled_raw
        elif isinstance(enabled_raw, str):
            enabled = enabled_raw.strip().lower() in {"1", "true", "yes", "on"}
        else:
            enabled = bool(enabled_raw)

        timeout_raw = data.get("sandbox_timeout_seconds", 15)
        try:
            timeout = int(timeout_raw)
        except (TypeError, ValueError):
            timeout = 15
        return PluginManifest(
            name=name,
            version=version,
            description=description,
            api_version=api_version,
            entrypoint=entrypoint,
            dependencies=dependencies,
            enabled=enabled,
            sandbox_timeout_seconds=max(timeout, 1),
        )

    def _resolve_dependencies(self) -> None:
        with self._lock:
            names = set(self._plugins.keys())
            for record in self._plugins.values():
                missing = [dep for dep in record.manifest.dependencies if dep not in names]
                if missing:
                    record.status = "dependency_error"
                    record.last_error = f"Missing dependencies: {', '.join(missing)}"
                elif not record.manifest.enabled:
                    record.status = "disabled"
                    record.last_error = None
                else:
                    record.status = "ready"
                    record.last_error = None
