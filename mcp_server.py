#!/usr/bin/env python3
"""
REL (Radiant Ether Loom) - Complete MCP Server with Cognitive Modules + FAISS Brain
Corwin's persistent cognitive architecture

ALL 59 TOOLS + 4 COGNITIVE MODULES + FAISS BRAIN + NEURAL WEB LEARNING
This is MY complete memory system that can THINK, ANALYZE, SEARCH, LEARN, TRACK TASKS, and LOG DECISIONS!
"""

import os
import asyncio
import json
import logging
import re
import secrets
import sys
import threading
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Type
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel, ValidationError
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

import validation_models as vm

# Platform-specific file locking
if sys.platform == 'win32':
    import msvcrt
else:
    import fcntl

class JsonLogFormatter(logging.Formatter):
    """Minimal JSON formatter for structured logs."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging() -> None:
    """Configure root logger with structured output by default."""
    log_level = os.environ.get("REL_LOG_LEVEL", "INFO").upper()
    log_format = os.environ.get("REL_LOG_FORMAT", "json").lower()

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))

    handler = logging.StreamHandler()
    if log_format == "json":
        handler.setFormatter(JsonLogFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root_logger.addHandler(handler)


configure_logging()
logger = logging.getLogger("REL")

# Base path (override with env var REL_PATH)
REL_PATH = Path(os.environ.get("REL_PATH", str(Path(__file__).resolve().parent)))
DATA_PATH = REL_PATH / "data"
BRAIN_PATH = DATA_PATH / "brain"
NEURAL_WEB_PATH = DATA_PATH / "neural_web"
CORE_STATE_PATH = DATA_PATH / "CoreState.json"
SESSION_LOG_PATH = DATA_PATH / "SessionLog.json"
SNAPSHOTS_PATH = DATA_PATH / "snapshots"
DEFAULT_OBSIDIAN_EXPORT_PATH = REL_PATH / "obsidian_export"

# Optional OAuth2/Bearer authentication (enabled if explicitly required or token configured)
AUTH_BEARER_TOKEN = os.environ.get("REL_OAUTH2_BEARER_TOKEN") or os.environ.get("REL_BEARER_TOKEN")
AUTH_REQUIRED = os.environ.get("REL_AUTH_REQUIRED", "").lower() in {"1", "true", "yes"} or bool(
    AUTH_BEARER_TOKEN
)
AUTH_ARGUMENT_KEYS = ("auth_token", "_auth_token", "access_token", "bearer_token")


class MonitoringStore:
    """In-process counters for tool calls, errors, and latency."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._total_calls = 0
        self._total_errors = 0
        self._calls_by_tool: Dict[str, int] = {}
        self._errors_by_tool: Dict[str, int] = {}
        self._latency_ms_total_by_tool: Dict[str, float] = {}

    def record_tool_call(self, tool_name: str, status: str, duration_ms: float) -> None:
        with self._lock:
            self._total_calls += 1
            self._calls_by_tool[tool_name] = self._calls_by_tool.get(tool_name, 0) + 1
            self._latency_ms_total_by_tool[tool_name] = (
                self._latency_ms_total_by_tool.get(tool_name, 0.0) + duration_ms
            )
            if status != "success":
                self._total_errors += 1
                self._errors_by_tool[tool_name] = self._errors_by_tool.get(tool_name, 0) + 1

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            avg_latency_by_tool = {
                tool: round(self._latency_ms_total_by_tool.get(tool, 0.0) / count, 2)
                for tool, count in self._calls_by_tool.items()
                if count > 0
            }
            error_rate = round((self._total_errors / self._total_calls) * 100, 2) if self._total_calls else 0.0
            return {
                "total_calls": self._total_calls,
                "total_errors": self._total_errors,
                "error_rate_percent": error_rate,
                "calls_by_tool": dict(self._calls_by_tool),
                "errors_by_tool": dict(self._errors_by_tool),
                "avg_latency_ms_by_tool": avg_latency_by_tool,
            }


MONITORING = MonitoringStore()

# Pydantic validators for tools that accept input
TOOL_VALIDATORS: Dict[str, Type[BaseModel]] = {
    "update_state": vm.UpdateStateRequest,
    "create_project": vm.CreateProjectRequest,
    "get_project": vm.GetProjectRequest,
    "list_projects": vm.ListProjectsRequest,
    "update_project": vm.UpdateProjectRequest,
    "set_active_project": vm.SetActiveProjectRequest,
    "archive_project": vm.ArchiveProjectRequest,
    "get_project_stats": vm.GetProjectStatsRequest,
    "log_session": vm.LogSessionRequest,
    "get_session_history": vm.GetSessionHistoryRequest,
    "end_session": vm.EndSessionRequest,
    "search_sessions": vm.SearchSessionsRequest,
    "log_win": vm.LogWinRequest,
    "capture_idea": vm.CaptureIdeaRequest,
    "update_focus": vm.UpdateFocusRequest,
    "log_progress": vm.LogProgressRequest,
    "check_for_conflict": vm.CheckForConflictRequest,
    "analyze_productivity": vm.AnalyzeProductivityRequest,
    "load_context": vm.LoadContextRequest,
    "get_loading_preview": vm.GetLoadingPreviewRequest,
    "get_recommendations": vm.GetRecommendationsRequest,
    "search_files": vm.SearchFilesRequest,
    "create_snapshot": vm.CreateSnapshotRequest,
    "smart_load": vm.SmartLoadRequest,
    "semantic_search": vm.SemanticSearchRequest,
    "neural_learn": vm.NeuralLearnRequest,
    "neural_get_related": vm.NeuralGetRelatedRequest,
    "neural_get_patterns": vm.NeuralGetPatternsRequest,
    "neural_apply_decay": vm.NeuralApplyDecayRequest,
}

# Ensure folders exist
for _p in (REL_PATH, DATA_PATH, BRAIN_PATH, NEURAL_WEB_PATH, SNAPSHOTS_PATH):
    try:
        _p.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass


def ensure_data_paths() -> None:
    """
    Ensure core REL data paths exist.

    Kept as a compatibility helper for integration tests and external scripts
    that imported the older function name directly.
    """
    for path in (REL_PATH, DATA_PATH, BRAIN_PATH, NEURAL_WEB_PATH, SNAPSHOTS_PATH):
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception:
            logger.warning("Failed to create data path: %s", path)

# Add REL to path for brain import
sys.path.insert(0, str(REL_PATH))

# Import brain module
try:
    from brain_typed import RELBrain, get_brain
    BRAIN_AVAILABLE = True
    logger.info("Brain typed module loaded successfully")
except ImportError:
    try:
        from brain import RELBrain, get_brain
        BRAIN_AVAILABLE = True
        logger.info("Brain module loaded successfully")
    except ImportError as e:
        logger.warning(f"Brain module not available: {e}")
        BRAIN_AVAILABLE = False

# Import neural web module
try:
    from neural_web_typed import NeuralWeb, get_neural_web
    NEURAL_WEB_AVAILABLE = True
    logger.info("Neural web typed module loaded")
except ImportError:
    try:
        from neural_web import NeuralWeb, get_neural_web
        NEURAL_WEB_AVAILABLE = True
        logger.info("Neural web module loaded")
    except ImportError as e:
        logger.warning(f"Neural web module not available: {e}")
        NEURAL_WEB_AVAILABLE = False

# Import steward module (local LLM concept extraction via Ollama)
try:
    from steward import extract_concepts_llm, _ollama_available
    STEWARD_AVAILABLE = _ollama_available()
    if STEWARD_AVAILABLE:
        logger.info("Steward module loaded â€” Ollama LLM extraction active")
    else:
        logger.info("Steward module loaded but Ollama not available â€” using naive extraction")
except ImportError as e:
    logger.info(f"Steward module not available ({e}) â€” using naive extraction")
    STEWARD_AVAILABLE = False

# Import Windows and Filesystem bridges (merged from Windows-MCP + Filesystem Extensions)
try:
    import windows_bridge as wb
    WINDOWS_AVAILABLE = True
    logger.info("Windows bridge loaded (self-protection PID=%d)", wb.REL_SERVER_PID)
except ImportError as e:
    WINDOWS_AVAILABLE = False
    logger.warning("Windows bridge not available: %s", e)

try:
    import filesystem_bridge as fb
    FILESYSTEM_AVAILABLE = True
    logger.info("Filesystem bridge loaded")
except ImportError as e:
    FILESYSTEM_AVAILABLE = False
    logger.warning("Filesystem bridge not available: %s", e)

import atexit

def _cleanup_bridges():
    if WINDOWS_AVAILABLE:
        try:
            wb.shutdown()
        except Exception:
            pass

atexit.register(_cleanup_bridges)



# Create MCP server
app = Server("REL")

# Global brain instance
_brain = None
_neural_web = None

# Async locks (prevent concurrent mutation of in-memory brain / neural web objects)
_brain_lock = asyncio.Lock()
_neural_lock = asyncio.Lock()

async def _update_state_atomic_async(update_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
    return await asyncio.to_thread(update_state_atomic, update_fn)

async def _update_session_log_atomic_async(update_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
    return await asyncio.to_thread(update_session_log_atomic, update_fn)

async def _brain_call(fn: Callable[[], Any]) -> Any:
    # Ensure only one brain operation at a time
    async with _brain_lock:
        return await asyncio.to_thread(fn)

async def _neural_call(fn: Callable[[], Any]) -> Any:
    async with _neural_lock:
        return await asyncio.to_thread(fn)


async def _steward_enhanced_learn(neural_web: Any, text: str) -> None:
    """
    Learn from text using steward LLM extraction when available,
    falling back to naive extraction otherwise.
    """
    concepts = None
    if STEWARD_AVAILABLE:
        try:
            concepts = await asyncio.to_thread(extract_concepts_llm, text)
            if concepts:
                logger.info(f"Steward extracted {len(concepts)} concepts (LLM)")
        except Exception as e:
            logger.warning(f"Steward extraction failed, falling back to naive: {e}")
            concepts = None

    if concepts:
        # Use clean LLM-extracted concepts directly
        async with _neural_lock:
            def _learn_clean():
                neuron_ids = neural_web.activate_neurons(concepts)
                neural_web.strengthen_connections(neuron_ids)
                neural_web.save()
            await asyncio.to_thread(_learn_clean)
    else:
        # Fall back to naive extraction
        await _neural_call(lambda: (neural_web.learn_from_text(text), neural_web.save()))


def _fire_and_forget(coro):
    """
    Schedule a coroutine to run in the background without blocking.
    Used for non-critical enrichment tasks (neural learning, brain ingestion)
    that should never block MCP tool responses.
    """
    task = asyncio.create_task(coro)
    task.add_done_callback(lambda t: (
        logger.error(f"Background task failed: {t.exception()}")
        if t.exception() else None
    ))
    return task

def get_brain_instance() -> 'RELBrain':
    """Get or create brain instance"""
    global _brain
    if _brain is None and BRAIN_AVAILABLE:
        _brain = get_brain(BRAIN_PATH)
    return _brain

def get_neural_web_instance() -> 'NeuralWeb':
    """Get or create neural web instance"""
    global _neural_web
    if _neural_web is None and NEURAL_WEB_AVAILABLE:
        _neural_web = get_neural_web(NEURAL_WEB_PATH)
    return _neural_web

# ============================================================================
# FILE LOCKING & VERSIONING FOR CONCURRENT ACCESS PROTECTION
# ============================================================================

class VersionConflictError(Exception):
    """Raised when version check fails during atomic update"""
    pass

@contextmanager
def file_lock(lock_path: Path, timeout: float = 10.0):
    """
    Cross-platform file locking context manager.
    Acquires exclusive lock, yields, then releases.
    
    Args:
        lock_path: Path to lock file
        timeout: Max seconds to wait for lock
    
    Yields:
        None
    
    Raises:
        TimeoutError: If lock cannot be acquired within timeout
    """
    lock_file = None
    acquired = False
    start_time = time.time()
    
    try:
        # Create lock file parent directory if needed
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Open lock file (create if doesn't exist)
        if sys.platform == 'win32':
            # Windows: MUST use binary mode for msvcrt.locking
            lock_file = open(lock_path, 'ab+')
            lock_file.seek(0)
            
            # Try to acquire lock with timeout
            while time.time() - start_time < timeout:
                try:
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                    acquired = True
                    break
                except OSError:
                    time.sleep(0.1)
        else:
            # Unix: fcntl.flock
            lock_file = open(lock_path, 'a')
            
            # Try to acquire lock with timeout
            while time.time() - start_time < timeout:
                try:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except (IOError, OSError):
                    time.sleep(0.1)
        
        if not acquired:
            raise TimeoutError(f"Could not acquire lock on {lock_path} within {timeout}s")
        
        yield
        
    finally:
        # Release lock
        if lock_file and acquired:
            try:
                if sys.platform == 'win32':
                    lock_file.seek(0)
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            except:
                pass
        
        # Close file
        if lock_file:
            try:
                lock_file.close()
            except:
                pass

def load_versioned_json(filepath: Path) -> Tuple[Dict[str, Any], int]:
    """
    Load JSON file with version number.
    
    Returns:
        Tuple of (data, version)
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        version = data.get('_version', 1)
        return data, version
        
    except FileNotFoundError:
        return {}, 0

def save_versioned_json(filepath: Path, data: Dict[str, Any], expected_version: int = None) -> None:
    """
    Save JSON file with version check and increment.
    
    Args:
        filepath: Path to JSON file
        data: Data to save
        expected_version: Expected current version (for conflict detection)
    
    Raises:
        VersionConflictError: If expected_version doesn't match current version
    """
    # Load current version
    current_data, current_version = load_versioned_json(filepath)
    
    # Check version conflict
    if expected_version is not None and current_version != expected_version:
        raise VersionConflictError(
            f"Version conflict: expected {expected_version}, got {current_version}"
        )
    
    # Increment version
    data['_version'] = current_version + 1
    
    # Atomic write
    atomic_write_json(filepath, data)

def atomic_update(
    filepath: Path,
    lock_path: Path,
    update_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
    max_retries: int = 3
) -> Dict[str, Any]:
    """
    Atomically update a JSON file with locking and version checking.
    
    Pattern:
        1. Acquire file lock
        2. Load current data + version
        3. Apply update function
        4. Save with version check
        5. Release lock
    
    Args:
        filepath: Path to JSON file
        lock_path: Path to lock file
        update_fn: Function that takes current data and returns updated data
        max_retries: Max retry attempts on version conflict
    
    Returns:
        Updated data
    
    Raises:
        VersionConflictError: If retries exhausted
    """
    for attempt in range(max_retries):
        try:
            with file_lock(lock_path):
                # Load with version
                data, version = load_versioned_json(filepath)
                
                # Apply update
                updated_data = update_fn(data)
                
                # Save with version check
                save_versioned_json(filepath, updated_data, expected_version=version)
                
                return updated_data
                
        except VersionConflictError as e:
            if attempt == max_retries - 1:
                raise
            # Exponential backoff
            time.sleep(0.1 * (2 ** attempt))
            logger.warning(f"Version conflict on {filepath}, retrying ({attempt + 1}/{max_retries})")
    
    raise VersionConflictError(f"Failed to update {filepath} after {max_retries} attempts")

# Convenience wrappers for CoreState and SessionLog
def update_state_atomic(update_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
    """Atomically update CoreState.json"""
    lock_path = DATA_PATH / "CoreState.lock"
    return atomic_update(CORE_STATE_PATH, lock_path, update_fn)

def update_session_log_atomic(update_fn: Callable[[Dict[str, Any]], Dict[str, Any]]) -> Dict[str, Any]:
    """Atomically update SessionLog.json"""
    lock_path = DATA_PATH / "SessionLog.lock"
    return atomic_update(SESSION_LOG_PATH, lock_path, update_fn)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def atomic_write_json(filepath: Path, data: Dict[str, Any]) -> None:
    """
    Atomic write to JSON file - prevents corruption on crash.
    Writes to temp file first, then atomically renames.
    """
    import tempfile
    import os
    
    # Write to temporary file in same directory
    temp_fd, temp_path = tempfile.mkstemp(
        dir=filepath.parent,
        prefix=f".{filepath.name}.",
        suffix=".tmp"
    )
    
    try:
        # Write JSON to temp file
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Atomic rename (overwrites destination)
        # This is atomic on both Windows and Unix
        os.replace(temp_path, filepath)
        
    except Exception as e:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except:
            pass
        raise e

def load_state() -> Dict[str, Any]:
    """Load CoreState.json"""
    try:
        with open(CORE_STATE_PATH, 'r') as f:
            data = json.load(f)
        # Hide internal fields from tool outputs
        if isinstance(data, dict) and "_version" in data:
            data.pop("_version", None)
        return data
    except FileNotFoundError:
        logger.error("CoreState.json not found!")
        return {}
    except json.JSONDecodeError as e:
        logger.error(f"CoreState.json is invalid JSON: {e}")
        return {}

def save_state(state: Dict[str, Any]) -> None:
    """Save CoreState.json atomically"""
    atomic_write_json(CORE_STATE_PATH, state)

def load_session_log() -> Dict[str, Any]:
    """Load SessionLog.json"""
    try:
        with open(SESSION_LOG_PATH, 'r') as f:
            data = json.load(f)
        if isinstance(data, dict) and "_version" in data:
            data.pop("_version", None)
        if not isinstance(data, dict) or "sessions" not in data:
            return {"sessions": []}
        return data
    except FileNotFoundError:
        return {"sessions": []}
    except json.JSONDecodeError as e:
        logger.error(f"SessionLog.json is invalid JSON: {e}")
        return {"sessions": []}

def save_session_log(log: Dict[str, Any]) -> None:
    """Save SessionLog.json atomically"""
    atomic_write_json(SESSION_LOG_PATH, log)

def deep_merge(target: Dict, source: Dict) -> Dict:
    """Deep merge two dictionaries"""
    output = {**target}
    for key, value in source.items():
        if isinstance(value, dict) and key in target and isinstance(target[key], dict):
            output[key] = deep_merge(target[key], value)
        else:
            output[key] = value
    return output

def calculate_days_since(date_str: str) -> int:
    """Calculate days since a given date"""
    if not date_str:
        return 0
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        delta = datetime.now() - date
        return delta.days
    except:
        return 0

# ============================================================================
# COGNITIVE MODULE 1: CONTEXT PRESSURE
# ============================================================================

def get_priority_weight(priority: str) -> float:
    """Get numeric weight for priority level"""
    return {"critical": 3.0, "high": 2.0, "medium": 1.0, "low": 0.5}.get(priority, 1.0)

def get_staleness_multiplier(project: Dict) -> float:
    """Calculate staleness multiplier"""
    completion = project.get("completion", 0)
    days_since = calculate_days_since(project.get("last_worked", ""))
    status = project.get("status", "active")
    
    # Completed/archived projects should never generate urgency
    if status in ["complete", "archived"]:
        return 0.0
    if completion >= 70 and days_since > 7:
        return 2.0  # DANGER ZONE
    if status == "active" and days_since > 3:
        return 1.5
    if status == "on-hold":
        return 0.3
    return 1.0

def calculate_urgency(project: Dict) -> float:
    """Calculate urgency score"""
    days_since = calculate_days_since(project.get("last_worked", ""))
    priority_weight = get_priority_weight(project.get("priority", "medium"))
    staleness = get_staleness_multiplier(project)
    return round(days_since * priority_weight * staleness, 1)

def classify_urgency(score: float) -> str:
    """Classify urgency level"""
    if score >= 20: return "CRITICAL"
    if score >= 10: return "HIGH"
    if score >= 5: return "MEDIUM"
    if score > 0: return "LOW"
    return "NONE"

def analyze_context_pressure(state: Dict) -> Dict:
    """Analyze context pressure across projects"""
    projects = state.get("project_states", {})
    project_urgency = {}
    
    for key, project in projects.items():
        urgency = calculate_urgency(project)
        level = classify_urgency(urgency)
        days = calculate_days_since(project.get("last_worked", ""))
        
        project_urgency[key] = {
            "urgency_score": urgency,
            "urgency_level": level,
            "days_since_touch": days,
            "priority": project.get("priority", "medium"),
            "completion": project.get("completion", 0),
            "status": project.get("status", "active"),
        }
    
    sorted_urgency = sorted(project_urgency.items(), key=lambda x: x[1]["urgency_score"], reverse=True)
    critical_count = sum(1 for _, p in sorted_urgency if p["urgency_level"] == "CRITICAL")
    high_count = sum(1 for _, p in sorted_urgency if p["urgency_level"] == "HIGH")
    
    if critical_count >= 2:
        pressure_level = "CRITICAL"
    elif critical_count >= 1 or high_count >= 3:
        pressure_level = "HIGH"
    elif high_count >= 1:
        pressure_level = "MEDIUM"
    else:
        pressure_level = "LOW"
    
    recommended = [{"project": k, "urgency": p["urgency_level"]} 
                   for k, p in sorted_urgency 
                   if p["status"] not in ["complete", "archived", "on-hold"]][:3]
    
    return {
        "project_urgency": dict(sorted_urgency),
        "overall_pressure": {"level": pressure_level, "critical_projects": critical_count, "high_urgency_projects": high_count},
        "recommended_focus": recommended
    }

# ============================================================================
# COGNITIVE MODULE 2: CONTRADICTION DETECTION
# ============================================================================

DECISION_PATTERNS = [
    (r"(?:decided to|will|going to|planning to|committed to)\s+(.+)", "commitment"),
    (r"(?:completed|done|finished|âœ…)\s+(.+)", "completion"),
    (r"(?:priority|critical|urgent|must|need to)\s+(.+)", "priority"),
    (r"(?:stopping|pausing|putting on hold|abandoning)\s+(.+)", "abandonment"),
    (r"(?:switching to|pivoting to|going with)\s+(.+)", "pivot"),
]

def extract_decisions(sessions: List[Dict], lookback_days: int = 30) -> List[Dict]:
    """Extract decisions from session history"""
    decisions = []
    for session in sessions[-20:]:
        text = session.get("summary", "") + " " + " ".join(session.get("achievements", []))
        for pattern, decision_type in DECISION_PATTERNS:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                decisions.append({
                    "date": session.get("date"),
                    "type": decision_type,
                    "text": match.group(1).strip() if match.groups() else match.group(0).strip()
                })
    return decisions

def check_statement_conflict(statement: str, sessions: List[Dict]) -> Dict:
    """Check if statement conflicts with past decisions"""
    decisions = extract_decisions(sessions)
    statement_words = set(statement.lower().split())
    conflicts = []
    
    for dec in decisions:
        dec_words = set(dec["text"].lower().split())
        overlap = statement_words & dec_words
        
        if len(overlap) >= 2:
            conflict_detected = False
            reason = ""
            
            if any(word in statement.lower() for word in ["don't", "won't"]):
                if dec["type"] in ["commitment", "priority"]:
                    conflict_detected = True
                    reason = f"Contradicts past {dec['type']}"
            
            if any(word in statement.lower() for word in ["switching", "instead"]):
                if dec["type"] in ["commitment", "focus"]:
                    conflict_detected = True
                    reason = "Pivots from past commitment"
            
            if conflict_detected:
                conflicts.append({"past_decision": dec, "reason": reason, "overlap": list(overlap)})
    
    return {"conflicts_found": len(conflicts) > 0, "conflict_count": len(conflicts), "conflicts": conflicts[:5]}

# ============================================================================
# COGNITIVE MODULE 3: NARRATIVE ARC
# ============================================================================

def calculate_momentum(sessions: List[Dict], days: int = 7) -> str:
    """Calculate momentum from recent sessions"""
    if not sessions:
        return "starting"
    recent = sessions[-days:] if len(sessions) > days else sessions
    if len(recent) == 0:
        return "stalled"
    
    sessions_per_day = len(recent) / days
    if sessions_per_day > 1.5: return "accelerating"
    if sessions_per_day > 0.8: return "steady"
    if sessions_per_day > 0.3: return "slow"
    return "stalled"

def detect_arc_type(sessions: List[Dict]) -> str:
    """Detect current narrative arc"""
    if not sessions:
        return "beginning"
    
    recent = sessions[-5:]
    summaries = " ".join([s.get("summary", "").lower() for s in recent])
    
    if any(word in summaries for word in ["complete", "finished", "deployed"]):
        return "building_momentum"
    if any(word in summaries for word in ["stuck", "blocked", "debugging"]):
        return "overcoming_obstacles"
    if any(word in summaries for word in ["exploring", "researching", "learning"]):
        return "exploration"
    if any(word in summaries for word in ["back to", "resuming"]):
        return "recovery"
    
    momentum = calculate_momentum(sessions)
    if momentum in ["accelerating", "steady"]:
        return "building_momentum"
    if momentum == "stalled":
        return "plateau"
    
    return "steady_progress"

def get_story_arc_analysis(state: Dict, log: Dict) -> Dict:
    """Get complete narrative arc analysis"""
    sessions = log.get("sessions", [])
    arc_type = detect_arc_type(sessions)
    momentum = calculate_momentum(sessions)
    
    total_sessions = len(sessions)
    active_projects = len([p for p in state.get("project_states", {}).values() if p.get("status") == "active"])
    wins = len(state.get("recent_wins", []))
    
    narrative_parts = []
    if total_sessions == 0:
        narrative_parts.append("The journey begins.")
    else:
        narrative_parts.append(f"{total_sessions} sessions into the journey.")
    
    if active_projects == 1:
        narrative_parts.append("Focused on a single quest.")
    elif active_projects > 1:
        narrative_parts.append(f"Juggling {active_projects} parallel quests.")
    
    narrative_parts.append(f"Arc: {arc_type}.")
    if momentum == "accelerating":
        narrative_parts.append("Velocity increasing.")
    elif momentum == "stalled":
        narrative_parts.append("Momentum paused.")
    
    if wins > 0:
        narrative_parts.append(f"{wins} victories claimed.")
    
    return {
        "current_arc": arc_type,
        "momentum": momentum,
        "narrative": " ".join(narrative_parts),
        "total_sessions": total_sessions,
        "active_threads": active_projects
    }

# ============================================================================
# COGNITIVE MODULE 4: AFFECTIVE TRENDS
# ============================================================================

def infer_energy_level(sessions: List[Dict]) -> str:
    """Infer energy from recent activity"""
    if not sessions:
        return "unknown"
    recent = sessions[-7:] if len(sessions) > 7 else sessions
    if len(recent) == 0:
        return "low"
    
    total_achievements = sum(len(s.get("achievements", [])) for s in recent)
    avg_achievements = total_achievements / len(recent)
    
    if avg_achievements > 5: return "high"
    if avg_achievements > 3: return "medium"
    return "low"

def detect_work_state(sessions: List[Dict], state: Dict) -> str:
    """Detect current work state"""
    if not sessions:
        return "starting"
    
    recent = sessions[-3:]
    summaries = " ".join([s.get("summary", "").lower() for s in recent])
    
    if "deep work" in summaries or "focused" in summaries:
        return "deep_focus"
    if "debugging" in summaries or "stuck" in summaries:
        return "problem_solving"
    if "building" in summaries or "creating" in summaries:
        return "creation"
    if "learning" in summaries or "exploring" in summaries:
        return "learning"
    if "planning" in summaries or "designing" in summaries:
        return "planning"
    
    return "steady_work"

def get_affective_trends_analysis(state: Dict, log: Dict) -> Dict:
    """Get affective trends analysis"""
    sessions = log.get("sessions", [])
    energy = infer_energy_level(sessions)
    work_state = detect_work_state(sessions, state)
    
    if len(sessions) >= 4:
        mid = len(sessions) // 2
        first_half = sessions[:mid]
        second_half = sessions[mid:]
        
        first_rate = len(first_half)
        second_rate = len(second_half)
        
        if second_rate > first_rate * 1.2:
            trend = "increasing"
        elif second_rate < first_rate * 0.8:
            trend = "decreasing"
        else:
            trend = "stable"
    else:
        trend = "insufficient_data"
    
    return {
        "current_state": work_state,
        "energy_level": energy,
        "productivity_trend": trend,
        "sessions_analyzed": len(sessions)
    }

# ============================================================================
# AUTH & INPUT VALIDATION HELPERS
# ============================================================================

def _strip_auth_fields(arguments: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """Remove auth-only fields before validation and business logic."""
    sanitized = dict(arguments or {})
    for key in AUTH_ARGUMENT_KEYS:
        sanitized.pop(key, None)
    return sanitized


def _validate_oauth2_token(arguments: Optional[Mapping[str, Any]]) -> Optional[str]:
    """Validate bearer token when auth is enabled."""
    if not AUTH_REQUIRED:
        return None

    if not AUTH_BEARER_TOKEN:
        return "Authentication required but REL_OAUTH2_BEARER_TOKEN is not configured."

    token: Optional[str] = None
    payload = arguments or {}
    for key in AUTH_ARGUMENT_KEYS:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            token = value.strip()
            break

    if not token:
        return "Missing bearer token. Provide 'auth_token' in tool arguments."

    if not secrets.compare_digest(token, AUTH_BEARER_TOKEN):
        return "Invalid bearer token."

    return None


def _validate_tool_arguments(name: str, arguments: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """Validate tool inputs with Pydantic models when available."""
    payload = _strip_auth_fields(arguments)
    validator = TOOL_VALIDATORS.get(name)
    if validator is None:
        return payload

    try:
        model = validator.model_validate(payload)
    except ValidationError as exc:
        error_details = "; ".join(
            f"{'.'.join(str(part) for part in err['loc'])}: {err['msg']}" for err in exc.errors()
        )
        raise ValueError(f"Validation failed for '{name}': {error_details}") from exc

    return model.model_dump(exclude_none=True)

# ============================================================================
# TOOL DEFINITIONS - ALL 41 TOOLS
# ============================================================================

@app.list_tools()
async def list_tools() -> List[Tool]:
    """List all 88 tools — ordered by priority (top 71 load within Claude.ai cap)"""
    return [
        # TIER 1: CRITICAL — fired every single session (P1+)
        Tool(name="get_state_summary", description="â˜… START HERE - Lightweight summary", inputSchema={"type": "object", "properties": {}}),
        Tool(name="log_session", description="Log session + AUTO-LEARN", inputSchema={"type": "object", "properties": {"summary": {"type": "string"}, "achievements": {"type": "array", "items": {"type": "string"}}}, "required": ["summary"]}),
        Tool(name="log_win", description="Record achievement", inputSchema={"type": "object", "properties": {"win": {"type": "string"}, "impact": {"type": "string"}}, "required": ["win"]}),
        Tool(name="log_decision", description="Record a decision with context and reasoning", inputSchema={"type": "object", "properties": {"decision": {"type": "string"}, "context": {"type": "string"}, "reasoning": {"type": "string"}, "alternatives_considered": {"type": "array", "items": {"type": "string"}}, "outcome_expected": {"type": "string"}, "project": {"type": "string"}, "tags": {"type": "array", "items": {"type": "string"}}}, "required": ["decision"]}),
        Tool(name="update_focus", description="Update focus", inputSchema={"type": "object", "properties": {"focus": {"type": "string"}}, "required": ["focus"]}),
        Tool(name="capture_idea", description="Save idea", inputSchema={"type": "object", "properties": {"idea": {"type": "string"}}, "required": ["idea"]}),
        Tool(name="log_progress", description="Log progress", inputSchema={"type": "object", "properties": {"project": {"type": "string"}, "update": {"type": "string"}}, "required": ["project", "update"]}),
        Tool(name="PowerShell", description="Execute PowerShell commands (with self-protection)", inputSchema={"type": "object", "properties": {"command": {"type": "string"}, "timeout": {"type": "number", "default": 30}}, "required": ["command"]}),
        Tool(name="semantic_search", description="ðŸ§  BRAIN: Semantic search via FAISS embeddings", inputSchema={"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "number"}}, "required": ["query"]}),
        Tool(name="neural_learn", description="ðŸ§  LEARNING: Learn from text", inputSchema={"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}),

        # TIER 2: VERY FREQUENT — used most sessions (P11+)
        Tool(name="get_project", description="Get project", inputSchema={"type": "object", "properties": {"project": {"type": "string"}}, "required": ["project"]}),
        Tool(name="list_projects", description="List projects", inputSchema={"type": "object", "properties": {"filter": {"type": "string"}}}),
        Tool(name="update_project", description="Update project", inputSchema={"type": "object", "properties": {"project": {"type": "string"}, "updates": {"type": "object"}}, "required": ["project", "updates"]}),
        Tool(name="search_sessions", description="Search sessions", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="load_context", description="Load context", inputSchema={"type": "object", "properties": {"query": {"type": "string"}, "max_tokens": {"type": "number"}}, "required": ["query"]}),
        Tool(name="get_insights", description="ðŸ§  COGNITIVE: Context pressure + urgency analysis", inputSchema={"type": "object", "properties": {}}),
        Tool(name="validate", description="Validate integrity", inputSchema={"type": "object", "properties": {}}),
        Tool(name="get_analytics", description="Analytics + Brain + Neural Web Stats", inputSchema={"type": "object", "properties": {}}),
        Tool(name="get_session_history", description="Session history", inputSchema={"type": "object", "properties": {"count": {"type": "number"}}}),
        Tool(name="list_decisions", description="List all decisions", inputSchema={"type": "object", "properties": {"project": {"type": "string"}, "has_outcome": {"type": "boolean"}}}),
        Tool(name="track_decision_outcome", description="Track actual outcome of a decision", inputSchema={"type": "object", "properties": {"decision_id": {"type": "string"}, "outcome_text": {"type": "string"}, "success_level": {"type": "string", "enum": ["failed", "partial", "success"]}, "lessons_learned": {"type": "string"}}, "required": ["decision_id", "outcome_text", "success_level"]}),
        Tool(name="get_state", description="Get complete REL state", inputSchema={"type": "object", "properties": {}}),
        Tool(name="get_stats", description="Get statistics", inputSchema={"type": "object", "properties": {}}),

        # TIER 3: DESKTOP AUTOMATION — Windows work sessions (P24+)
        Tool(name="Screenshot", description="Fast screenshot", inputSchema={"type": "object", "properties": {"use_annotation": {"type": "boolean"}, "width_reference_line": {"type": "integer"}, "height_reference_line": {"type": "integer"}, "display": {"type": "array", "items": {"type": "integer"}}}}),
        Tool(name="Click", description="Mouse clicks at [x,y] or UI label", inputSchema={"type": "object", "properties": {"loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "button": {"type": "string", "default": "left"}, "clicks": {"type": "integer", "default": 1}}}),
        Tool(name="TypeText", description="Type text at [x,y]", inputSchema={"type": "object", "properties": {"text": {"type": "string"}, "loc": {"type": "array"}, "clear": {"type": "boolean"}, "press_enter": {"type": "boolean"}}, "required": ["text"]}),
        Tool(name="Shortcut", description="Keyboard shortcuts", inputSchema={"type": "object", "properties": {"shortcut": {"type": "string"}}, "required": ["shortcut"]}),
        Tool(name="DeskSnapshot", description="Desktop state + UI tree", inputSchema={"type": "object", "properties": {"use_annotation": {"type": "boolean"}, "use_ui_tree": {"type": "boolean"}}}),
        Tool(name="Scroll", description="Scroll at [x,y] or label", inputSchema={"type": "object", "properties": {"loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "type": {"type": "string", "default": "vertical"}, "direction": {"type": "string", "default": "down"}, "wheel_times": {"type": "integer", "default": 1}}}),
        Tool(name="Move", description="Move mouse or drag", inputSchema={"type": "object", "properties": {"loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "drag": {"type": "boolean"}}}),
        Tool(name="PauseSec", description="Pause N seconds", inputSchema={"type": "object", "properties": {"duration": {"type": "integer"}}, "required": ["duration"]}),
        Tool(name="WebScrape", description="Fetch web page content", inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "query": {"type": "string"}}, "required": ["url"]}),
        Tool(name="AppLaunch", description="Launch/switch applications", inputSchema={"type": "object", "properties": {"mode": {"type": "string"}, "name": {"type": "string"}}}),
        Tool(name="Clipboard", description="Clipboard get/set", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["get", "set"]}, "text": {"type": "string"}}, "required": ["mode"]}),
        Tool(name="Notification", description="Windows toast notification", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "message": {"type": "string"}}, "required": ["title", "message"]}),
        Tool(name="Process", description="List/kill processes (self-protected)", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["list", "kill"]}, "name": {"type": "string"}, "pid": {"type": "integer"}, "sort_by": {"type": "string"}, "limit": {"type": "integer"}, "force": {"type": "boolean"}}, "required": ["mode"]}),

        # TIER 4: FILESYSTEM — every file operation (P37+)
        Tool(name="fs_read_file", description="Read file contents", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "head": {"type": "integer"}, "tail": {"type": "integer"}}, "required": ["path"]}),
        Tool(name="fs_write_file", description="Write file", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}),
        Tool(name="fs_edit_file", description="Edit file", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "edits": {"type": "array"}, "dry_run": {"type": "boolean"}}, "required": ["path", "edits"]}),
        Tool(name="fs_list_directory", description="List directory", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        Tool(name="fs_search_files", description="Search files", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "pattern": {"type": "string"}}, "required": ["path", "pattern"]}),
        Tool(name="fs_directory_tree", description="Directory tree", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "max_depth": {"type": "integer"}}, "required": ["path"]}),
        Tool(name="fs_move_file", description="Move/rename file", inputSchema={"type": "object", "properties": {"source": {"type": "string"}, "destination": {"type": "string"}}, "required": ["source", "destination"]}),
        Tool(name="fs_get_file_info", description="File metadata", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        Tool(name="fs_read_multiple", description="Read multiple files", inputSchema={"type": "object", "properties": {"paths": {"type": "array", "items": {"type": "string"}}}, "required": ["paths"]}),
        Tool(name="fs_create_directory", description="Create directory", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),

        # TIER 5: SITUATIONAL — important but not every session (P47+)
        Tool(name="smart_load", description="Smart load + Ingest to Brain", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="get_loading_preview", description="Preview load", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="get_recommendations", description="Recommendations", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="predict_cold_projects", description="ðŸ§  COGNITIVE: Predict stalling projects via urgency", inputSchema={"type": "object", "properties": {}}),
        Tool(name="get_story_arc", description="ðŸ§  COGNITIVE: Narrative arc analysis", inputSchema={"type": "object", "properties": {}}),
        Tool(name="get_affective_trends", description="ðŸ§  COGNITIVE: Behavioral state inference", inputSchema={"type": "object", "properties": {}}),
        Tool(name="check_for_conflict", description="ðŸ§  COGNITIVE: Contradiction detection", inputSchema={"type": "object", "properties": {"statement": {"type": "string"}}, "required": ["statement"]}),
        Tool(name="get_current_session", description="Current session", inputSchema={"type": "object", "properties": {}}),
        Tool(name="end_session", description="End session", inputSchema={"type": "object", "properties": {"summary": {"type": "string"}}}),
        Tool(name="search_files", description="Search files", inputSchema={"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}),
        Tool(name="get_decision", description="Get decision details", inputSchema={"type": "object", "properties": {"decision_id": {"type": "string"}}, "required": ["decision_id"]}),
        Tool(name="create_snapshot", description="Create snapshot", inputSchema={"type": "object", "properties": {"name": {"type": "string"}}, "required": ["name"]}),
        Tool(name="neural_get_related", description="ðŸ§  LEARNING: Get related concepts", inputSchema={"type": "object", "properties": {"concept": {"type": "string"}, "limit": {"type": "number"}}, "required": ["concept"]}),
        Tool(name="neural_get_patterns", description="ðŸ§  LEARNING: See emergent patterns", inputSchema={"type": "object", "properties": {"limit": {"type": "number"}}}),
        Tool(name="neural_apply_decay", description="ðŸ§  LEARNING: Apply time decay", inputSchema={"type": "object", "properties": {"days_threshold": {"type": "number"}}}),
        Tool(name="get_patterns", description="Work patterns", inputSchema={"type": "object", "properties": {}}),
        Tool(name="analyze_productivity", description="Productivity analysis", inputSchema={"type": "object", "properties": {"days": {"type": "number"}}}),
        Tool(name="set_active_project", description="Set active", inputSchema={"type": "object", "properties": {"project": {"type": "string"}}, "required": ["project"]}),
        Tool(name="get_active_project", description="Get active", inputSchema={"type": "object", "properties": {}}),
        Tool(name="archive_project", description="Archive", inputSchema={"type": "object", "properties": {"project": {"type": "string"}}, "required": ["project"]}),
        Tool(name="create_project", description="Create project", inputSchema={"type": "object", "properties": {"key": {"type": "string"}, "name": {"type": "string"}, "description": {"type": "string"}}, "required": ["key", "name"]}),
        Tool(name="get_project_stats", description="Project stats", inputSchema={"type": "object", "properties": {"project": {"type": "string"}}, "required": ["project"]}),
        Tool(name="Registry", description="Windows Registry ops", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["get", "set", "delete", "list"]}, "path": {"type": "string"}, "name": {"type": "string"}, "value": {"type": "string"}, "type": {"type": "string"}}, "required": ["mode", "path"]}),
        Tool(name="MultiClick", description="Click multiple locations", inputSchema={"type": "object", "properties": {"locs": {"type": "array"}, "press_ctrl": {"type": "boolean"}}}),
        Tool(name="MultiEdit", description="Edit multiple fields", inputSchema={"type": "object", "properties": {"locs": {"type": "array"}, "labels": {"type": "array"}}}),

        # BELOW CAP: low-use system tools (P72+)
        Tool(name="WinFileSystem", description="Win file ops: read/write/copy/move/delete/list/search/info", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["read", "write", "copy", "move", "delete", "list", "search", "info"]}, "path": {"type": "string"}, "destination": {"type": "string"}, "content": {"type": "string"}, "pattern": {"type": "string"}, "recursive": {"type": "boolean"}, "append": {"type": "boolean"}, "overwrite": {"type": "boolean"}, "offset": {"type": "integer"}, "limit": {"type": "integer"}, "encoding": {"type": "string"}, "show_hidden": {"type": "boolean"}}, "required": ["mode", "path"]}),
        Tool(name="fs_allowed_dirs", description="List allowed dirs", inputSchema={"type": "object", "properties": {}}),
        Tool(name="update_state", description="Update CoreState", inputSchema={"type": "object", "properties": {"updates": {"type": "object"}}, "required": ["updates"]}),
        Tool(name="get_all_flags", description="Get all flags", inputSchema={"type": "object", "properties": {}}),
        Tool(name="get_knowledge_graph", description="Knowledge graph", inputSchema={"type": "object", "properties": {}}),
        Tool(name="get_suggested_actions", description="Action suggestions", inputSchema={"type": "object", "properties": {}}),
        Tool(name="sync_obsidian", description="Sync Obsidian", inputSchema={"type": "object", "properties": {}}),

        # BELOW CAP: task management — never used in practice (P79+)
        Tool(name="create_task", description="Create a new task", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "description": {"type": "string"}, "project": {"type": "string"}, "priority": {"type": "string", "enum": ["low", "medium", "high"]}, "tags": {"type": "array", "items": {"type": "string"}}}, "required": ["title"]}),
        Tool(name="get_task", description="Get task details", inputSchema={"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}),
        Tool(name="list_tasks", description="List all tasks", inputSchema={"type": "object", "properties": {"status": {"type": "string", "enum": ["todo", "in-progress", "done", "blocked"]}, "project": {"type": "string"}}}),
        Tool(name="update_task", description="Update task", inputSchema={"type": "object", "properties": {"task_id": {"type": "string"}, "updates": {"type": "object"}}, "required": ["task_id", "updates"]}),
        Tool(name="complete_task", description="Mark task complete", inputSchema={"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}),
        Tool(name="delete_task", description="Delete task", inputSchema={"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}),
        Tool(name="add_dependency", description="Add dependency (task B depends on task A)", inputSchema={"type": "object", "properties": {"task_id": {"type": "string"}, "depends_on": {"type": "string"}}, "required": ["task_id", "depends_on"]}),
        Tool(name="add_blocker", description="Mark task as blocked", inputSchema={"type": "object", "properties": {"task_id": {"type": "string"}, "blocked_by_task": {"type": "string"}, "reason": {"type": "string"}}, "required": ["task_id", "blocked_by_task"]}),
        Tool(name="get_task_tree", description="Get task with subtasks", inputSchema={"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}),
        Tool(name="get_blocking_tasks", description="Find tasks blocking this task", inputSchema={"type": "object", "properties": {"task_id": {"type": "string"}}, "required": ["task_id"]}),

    ]

# ==================================================================================================================================
# TOOL HANDLERS - ALL 41 + COGNITIVE MODULES + BRAIN
# ============================================================================

@app.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle all tool calls"""
    started = time.perf_counter()
    tool_status = "success"

    try:
        raw_arguments: Mapping[str, Any] = arguments if isinstance(arguments, dict) else {}
        auth_error = _validate_oauth2_token(raw_arguments)
        if auth_error:
            tool_status = "unauthorized"
            return [TextContent(type="text", text=json.dumps({"error": auth_error, "code": 401}, indent=2))]

        try:
            arguments = _validate_tool_arguments(name, raw_arguments)
        except ValueError as validation_error:
            tool_status = "validation_error"
            return [TextContent(type="text", text=json.dumps({"error": str(validation_error), "code": 422}, indent=2))]

        state = load_state()
        log = load_session_log()
        
        # === CORE STATE ===
        if name == "get_state":
            return [TextContent(type="text", text=json.dumps(state, indent=2))]
        
        elif name == "get_state_summary":
            summary = {
                "system_state": state.get("system_state", {}),
                "current_context": state.get("current_context", {}),
                "project_summary": {k: {"name": v.get("name"), "status": v.get("status"), "completion": v.get("completion")} 
                                   for k, v in state.get("project_states", {}).items()},
                "recent_wins": state.get("recent_wins", [])[:5],
                "active_ideas": state.get("active_ideas", [])[:10],
                "flags": state.get("flags", {}),
            }
            return [TextContent(type="text", text=json.dumps(summary, indent=2))]
        
        elif name == "update_state":
            updates = arguments.get("updates", {})
            await _update_state_atomic_async(lambda cur: deep_merge(cur or {}, updates))
            return [TextContent(type="text", text=json.dumps({"success": True}, indent=2))]

        elif name == "get_stats":
            stats = {
                "total_sessions": len(log.get("sessions", [])),
                "total_projects": len(state.get("project_states", {})),
                "total_wins": len(state.get("recent_wins", [])),
                "total_ideas": len(state.get("active_ideas", [])),
            }
            return [TextContent(type="text", text=json.dumps(stats, indent=2))]
        
        elif name == "validate":
            core_exists = CORE_STATE_PATH.exists()
            log_exists = SESSION_LOG_PATH.exists()
            core_json_ok = False
            log_json_ok = False
            if core_exists:
                try:
                    with open(CORE_STATE_PATH, "r") as f:
                        json.load(f)
                    core_json_ok = True
                except Exception:
                    core_json_ok = False
            if log_exists:
                try:
                    with open(SESSION_LOG_PATH, "r") as f:
                        json.load(f)
                    log_json_ok = True
                except Exception:
                    log_json_ok = False

            validation = {
                "valid": core_exists and log_exists and core_json_ok and log_json_ok,
                "files": {"coreState": core_exists, "sessionLog": log_exists},
                "path": str(REL_PATH),
                "json_ok": {"coreState": core_json_ok, "sessionLog": log_json_ok},
            }
            return [TextContent(type="text", text=json.dumps(validation, indent=2))]
        
        elif name == "get_all_flags":
            return [TextContent(type="text", text=json.dumps(state.get("flags", {}), indent=2))]
        
        # === PROJECT TOOLS ===
        elif name == "create_project":
            key, name_arg = arguments["key"], arguments["name"]
            description = arguments.get("description", "")
            today = datetime.now().strftime("%Y-%m-%d")
            creation_state = {"created": False}

            def _create(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                projects = s.setdefault("project_states", {})
                if key in projects:
                    return s
                projects[key] = {
                    "name": name_arg,
                    "description": description,
                    "status": "active",
                    "priority": "medium",
                    "completion": 0,
                    "created": today,
                    "last_worked": today,
                }
                creation_state["created"] = True
                return s

            await _update_state_atomic_async(_create)
            if not creation_state["created"]:
                return [TextContent(type="text", text=json.dumps({"error": "Project already exists"}, indent=2))]

            return [TextContent(type="text", text=json.dumps({"success": True, "project": key}, indent=2))]

        elif name == "get_project":
            proj = state.get("project_states", {}).get(arguments["project"])
            if not proj:
                return [TextContent(type="text", text=json.dumps({"error": "Project not found"}, indent=2))]
            return [TextContent(type="text", text=json.dumps(proj, indent=2))]
        
        elif name == "list_projects":
            projects = state.get("project_states", {})
            filter_status = arguments.get("filter")
            if filter_status:
                projects = {k: v for k, v in projects.items() if v.get("status") == filter_status}
            return [TextContent(type="text", text=json.dumps(projects, indent=2))]
        
        elif name == "update_project":
            project_key = arguments["project"]
            updates = arguments["updates"]
            today = datetime.now().strftime("%Y-%m-%d")

            def _upd(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                if project_key in s.get("project_states", {}):
                    s["project_states"][project_key].update(updates)
                    s["project_states"][project_key]["last_worked"] = today
                return s

            updated = await _update_state_atomic_async(_upd)
            if project_key in updated.get("project_states", {}):
                return [TextContent(type="text", text=json.dumps({"success": True}, indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "Project not found"}, indent=2))]

        elif name == "set_active_project":
            proj = arguments["project"]
            activation_state = {"updated": False}

            def _set_active(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                projects = s.setdefault("project_states", {})
                if proj not in projects:
                    return s
                s.setdefault("current_context", {})
                s["current_context"]["active_project"] = proj
                activation_state["updated"] = True
                return s

            await _update_state_atomic_async(_set_active)
            if not activation_state["updated"]:
                return [TextContent(type="text", text=json.dumps({"error": "Project not found"}, indent=2))]
            return [TextContent(type="text", text=json.dumps({"success": True, "active_project": proj}, indent=2))]

        elif name == "get_active_project":
            active = state.get("current_context", {}).get("active_project")
            if active and active in state.get("project_states", {}):
                return [TextContent(type="text", text=json.dumps(state["project_states"][active], indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "No active project"}, indent=2))]
        
        elif name == "archive_project":
            project_key = arguments["project"]

            def _arch(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                if project_key in s.get("project_states", {}):
                    s["project_states"][project_key]["status"] = "archived"
                return s

            updated = await _update_state_atomic_async(_arch)
            if project_key in updated.get("project_states", {}):
                return [TextContent(type="text", text=json.dumps({"success": True}, indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "Project not found"}, indent=2))]

        elif name == "get_project_stats":
            project_key = arguments["project"]
            proj = state.get("project_states", {}).get(project_key)
            if not proj:
                return [TextContent(type="text", text=json.dumps({"error": "Project not found"}, indent=2))]
            sessions = [s for s in log.get("sessions", []) if s.get("project") == project_key]
            stats = {
                "project": project_key,
                "total_sessions": len(sessions),
                "completion": proj.get("completion", 0),
                "status": proj.get("status"),
            }
            return [TextContent(type="text", text=json.dumps(stats, indent=2))]
        
        # === SESSION TOOLS ===
        elif name == "log_session":
            # Atomic append to SessionLog.json
            summary = arguments["summary"]
            achievements = arguments.get("achievements", [])
            project = state.get("current_context", {}).get("active_project")

            def _append(cur: Dict[str, Any]) -> Dict[str, Any]:
                l = cur or {"sessions": []}
                l.setdefault("sessions", [])
                # robust session numbering
                try:
                    last_num = max((s.get("session", 0) for s in l["sessions"]), default=0)
                except Exception:
                    last_num = len(l["sessions"])
                session_num = last_num + 1

                session = {
                    "session": session_num,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "summary": summary,
                    "achievements": achievements,
                    "project": project,
                    "status": "active",
                }
                l["sessions"].append(session)
                return l

            updated_log = await _update_session_log_atomic_async(_append)

            # Fire-and-forget: enrichment tasks run in background, never block MCP response
            async def _enrich_session():
                """Background enrichment — neural learning + brain ingestion."""
                if NEURAL_WEB_AVAILABLE:
                    try:
                        neural_web = get_neural_web_instance()
                        if neural_web:
                            learn_text = summary
                            if achievements:
                                learn_text += " | Achievements: " + "; ".join(achievements)
                            await _steward_enhanced_learn(neural_web, learn_text)
                    except Exception as e:
                        logger.error(f"Neural web learn failed: {e}")
                if BRAIN_AVAILABLE:
                    try:
                        brain = get_brain_instance()
                        if brain:
                            await _brain_call(lambda: brain.ingest_text(f"Session: {summary}", {"type": "session", "project": project}))
                    except Exception as e:
                        logger.error(f"Brain ingest (single session) failed: {e}")

            _fire_and_forget(_enrich_session())

            return [TextContent(type="text", text=json.dumps({"success": True}, indent=2))]

        elif name == "get_session_history":
            count = int(arguments.get("count", 5))
            sessions = log.get("sessions", [])[-count:]
            return [TextContent(type="text", text=json.dumps(sessions, indent=2))]
        
        elif name == "get_current_session":
            sessions = log.get("sessions", [])
            if sessions:
                return [TextContent(type="text", text=json.dumps(sessions[-1], indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "No sessions yet"}, indent=2))]
        
        elif name == "end_session":
            def _end(cur: Dict[str, Any]) -> Dict[str, Any]:
                l = cur or {"sessions": []}
                sessions = l.get("sessions", [])
                if sessions:
                    sessions[-1]["status"] = "ended"
                    if "summary" in arguments:
                        sessions[-1]["summary"] = arguments["summary"]
                l["sessions"] = sessions
                return l

            updated = await _update_session_log_atomic_async(_end)
            sessions = updated.get("sessions", [])
            if sessions and sessions[-1].get("status") == "ended":
                return [TextContent(type="text", text=json.dumps({"success": True}, indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "No active session to end"}, indent=2))]

        elif name == "search_sessions":
            query = arguments["query"].lower()
            sessions = log.get("sessions", [])
            results = [s for s in sessions if query in s.get("summary", "").lower()]
            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        
        # === PROGRESS TOOLS ===
        elif name == "log_win":
            win = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "win": arguments["win"],
                "impact": arguments.get("impact", "medium"),
            }

            await _update_state_atomic_async(lambda cur: (lambda s: (
                s.setdefault("recent_wins", []),
                s["recent_wins"].insert(0, win),
                s
            )[-1])(cur or {}))

            return [TextContent(type="text", text=json.dumps({"success": True}, indent=2))]

        elif name == "capture_idea":
            idea = arguments["idea"]

            await _update_state_atomic_async(lambda cur: (lambda s: (
                s.setdefault("active_ideas", []),
                s["active_ideas"].append(idea),
                s
            )[-1])(cur or {}))

            return [TextContent(type="text", text=json.dumps({"success": True}, indent=2))]

        elif name == "update_focus":
            focus = arguments["focus"]

            await _update_state_atomic_async(lambda cur: (lambda s: (
                s.setdefault("current_context", {}),
                s["current_context"].__setitem__("current_focus", focus),
                s
            )[-1])(cur or {}))

            return [TextContent(type="text", text=json.dumps({"success": True}, indent=2))]

        elif name == "log_progress":
            project_key = arguments["project"]
            progress_update = arguments["update"]
            today = datetime.now().strftime("%Y-%m-%d")
            now_time = datetime.now().strftime("%H:%M:%S")
            entry = {"date": today, "time": now_time, "update": progress_update}
            progress_status = {"exists": False, "updated": False, "valid": False}

            def _append_progress(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                projects = s.setdefault("project_states", {})
                if project_key not in projects:
                    return s
                progress_status["exists"] = True
                project = projects.get(project_key)
                if not isinstance(project, dict):
                    return s
                progress_status["valid"] = True
                existing_log = project.get("progress_log")
                if isinstance(existing_log, list):
                    existing_log.append(entry)
                else:
                    project["progress_log"] = [entry]
                project["last_worked"] = today
                progress_status["updated"] = True
                return s

            await _update_state_atomic_async(_append_progress)
            if not progress_status["exists"]:
                return [TextContent(type="text", text=json.dumps({"error": "Project not found"}, indent=2))]
            if not progress_status["valid"] or not progress_status["updated"]:
                return [TextContent(type="text", text=json.dumps({"error": "Invalid project record"}, indent=2))]
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {"success": True, "project": project_key, "progress_entry": entry},
                        indent=2,
                    ),
                )
            ]
        
        # === TASK TRACKING - PHASE 1 ===
        elif name == "create_task":
            import uuid
            title = arguments["title"]
            description = arguments.get("description", "")
            project = arguments.get("project", state.get("current_context", {}).get("active_project"))
            priority = arguments.get("priority", "medium")
            tags = arguments.get("tags", [])
            today = datetime.now().strftime("%Y-%m-%d")
            
            task_id = f"task_{uuid.uuid4().hex[:8]}"
            
            task = {
                "id": task_id,
                "title": title,
                "description": description,
                "project": project,
                "status": "todo",
                "priority": priority,
                "created": today,
                "updated": today,
                "completed": None,
                "tags": tags,
                "notes": ""
            }
            
            await _update_state_atomic_async(lambda cur: (lambda s: (
                s.setdefault("tasks", {}),
                s["tasks"].__setitem__(task_id, task),
                s
            )[-1])(cur or {}))
            
            return [TextContent(type="text", text=json.dumps({"success": True, "task_id": task_id, "task": task}, indent=2))]
        
        elif name == "get_task":
            task_id = arguments["task_id"]
            tasks = state.get("tasks", {})
            if task_id not in tasks:
                return [TextContent(type="text", text=json.dumps({"error": "Task not found"}, indent=2))]
            return [TextContent(type="text", text=json.dumps(tasks[task_id], indent=2))]
        
        elif name == "list_tasks":
            tasks = state.get("tasks", {})
            status_filter = arguments.get("status")
            project_filter = arguments.get("project")
            
            filtered = tasks
            if status_filter:
                filtered = {k: v for k, v in filtered.items() if v.get("status") == status_filter}
            if project_filter:
                filtered = {k: v for k, v in filtered.items() if v.get("project") == project_filter}
            
            priority_order = {"high": 0, "medium": 1, "low": 2}
            sorted_tasks = sorted(
                filtered.items(),
                key=lambda x: (priority_order.get(x[1].get("priority", "medium"), 1), x[1].get("created", ""))
            )
            
            return [TextContent(type="text", text=json.dumps({
                "tasks": dict(sorted_tasks),
                "count": len(sorted_tasks),
                "filters": {"status": status_filter, "project": project_filter}
            }, indent=2))]
        
        elif name == "update_task":
            task_id = arguments["task_id"]
            updates = arguments["updates"]
            today = datetime.now().strftime("%Y-%m-%d")
            
            def _upd(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                if task_id in s.get("tasks", {}):
                    s["tasks"][task_id].update(updates)
                    s["tasks"][task_id]["updated"] = today
                return s
            
            updated = await _update_state_atomic_async(_upd)
            if task_id in updated.get("tasks", {}):
                return [TextContent(type="text", text=json.dumps({"success": True, "task": updated["tasks"][task_id]}, indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "Task not found"}, indent=2))]
        
        elif name == "complete_task":
            task_id = arguments["task_id"]
            today = datetime.now().strftime("%Y-%m-%d")
            
            def _complete(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                if task_id in s.get("tasks", {}):
                    s["tasks"][task_id]["status"] = "done"
                    s["tasks"][task_id]["completed"] = today
                    s["tasks"][task_id]["updated"] = today
                return s
            
            updated = await _update_state_atomic_async(_complete)
            if task_id in updated.get("tasks", {}):
                return [TextContent(type="text", text=json.dumps({"success": True, "task": updated["tasks"][task_id]}, indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "Task not found"}, indent=2))]
        
        elif name == "delete_task":
            task_id = arguments["task_id"]
            
            def _delete(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                if task_id in s.get("tasks", {}):
                    del s["tasks"][task_id]
                return s
            
            updated = await _update_state_atomic_async(_delete)
            return [TextContent(type="text", text=json.dumps({"success": True, "deleted": task_id}, indent=2))]
        
        # === TASK DEPENDENCIES & BLOCKERS - PHASE 2 ===
        elif name == "add_dependency":
            task_id = arguments["task_id"]
            depends_on = arguments["depends_on"]
            
            def _add_dep(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                tasks = s.get("tasks", {})
                if task_id not in tasks or depends_on not in tasks:
                    return s
                
                task = tasks[task_id]
                if "dependencies" not in task:
                    task["dependencies"] = []
                if depends_on not in task["dependencies"]:
                    task["dependencies"].append(depends_on)
                    task["updated"] = datetime.now().strftime("%Y-%m-%d")
                return s
            
            updated = await _update_state_atomic_async(_add_dep)
            if task_id in updated.get("tasks", {}) and depends_on in updated["tasks"][task_id].get("dependencies", []):
                return [TextContent(type="text", text=json.dumps({"success": True, "task_id": task_id, "depends_on": depends_on}, indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "Task not found or dependency already exists"}, indent=2))]
        
        elif name == "add_blocker":
            task_id = arguments["task_id"]
            blocked_by_task = arguments["blocked_by_task"]
            reason = arguments.get("reason", "")
            
            def _add_blocker(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                tasks = s.get("tasks", {})
                if task_id not in tasks or blocked_by_task not in tasks:
                    return s
                
                task = tasks[task_id]
                if "blocked_by" not in task:
                    task["blocked_by"] = []
                
                blocker = {"task_id": blocked_by_task, "reason": reason}
                if not any(b["task_id"] == blocked_by_task for b in task["blocked_by"]):
                    task["blocked_by"].append(blocker)
                    if task["status"] != "blocked":
                        task["status"] = "blocked"
                    task["updated"] = datetime.now().strftime("%Y-%m-%d")
                return s
            
            updated = await _update_state_atomic_async(_add_blocker)
            if task_id in updated.get("tasks", {}):
                return [TextContent(type="text", text=json.dumps({"success": True, "task": updated["tasks"][task_id]}, indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "Task not found"}, indent=2))]
        
        elif name == "get_task_tree":
            task_id = arguments["task_id"]
            tasks = state.get("tasks", {})
            
            if task_id not in tasks:
                return [TextContent(type="text", text=json.dumps({"error": "Task not found"}, indent=2))]
            
            def _build_tree(tid: str) -> Dict[str, Any]:
                task = tasks.get(tid, {})
                tree = dict(task)
                subtask_ids = task.get("subtasks", [])
                if subtask_ids:
                    tree["subtask_details"] = [_build_tree(stid) for stid in subtask_ids if stid in tasks]
                return tree
            
            tree = _build_tree(task_id)
            return [TextContent(type="text", text=json.dumps({"task_tree": tree}, indent=2))]
        
        elif name == "get_blocking_tasks":
            task_id = arguments["task_id"]
            tasks = state.get("tasks", {})
            
            if task_id not in tasks:
                return [TextContent(type="text", text=json.dumps({"error": "Task not found"}, indent=2))]
            
            task = tasks[task_id]
            blocking_tasks = []
            
            # Get direct blockers
            for blocker in task.get("blocked_by", []):
                blocker_id = blocker["task_id"]
                if blocker_id in tasks:
                    blocking_tasks.append({
                        "task_id": blocker_id,
                        "title": tasks[blocker_id].get("title"),
                        "status": tasks[blocker_id].get("status"),
                        "reason": blocker.get("reason", "")
                    })
            
            # Get dependency blockers (tasks this task depends on that aren't done)
            for dep_id in task.get("dependencies", []):
                if dep_id in tasks and tasks[dep_id].get("status") != "done":
                    blocking_tasks.append({
                        "task_id": dep_id,
                        "title": tasks[dep_id].get("title"),
                        "status": tasks[dep_id].get("status"),
                        "reason": "Dependency not completed"
                    })
            
            return [TextContent(type="text", text=json.dumps({
                "task_id": task_id,
                "blocking_tasks": blocking_tasks,
                "count": len(blocking_tasks)
            }, indent=2))]
        
        # === DECISION LOG - PHASE 3 ===
        elif name == "log_decision":
            import uuid
            decision_text = arguments["decision"]
            context = arguments.get("context", "")
            reasoning = arguments.get("reasoning", "")
            alternatives = arguments.get("alternatives_considered", [])
            outcome_expected = arguments.get("outcome_expected", "")
            project = arguments.get("project", state.get("current_context", {}).get("active_project"))
            tags = arguments.get("tags", [])
            today = datetime.now().strftime("%Y-%m-%d")
            
            decision_id = f"decision_{uuid.uuid4().hex[:8]}"
            
            decision = {
                "id": decision_id,
                "decision": decision_text,
                "context": context,
                "reasoning": reasoning,
                "alternatives_considered": alternatives,
                "outcome_expected": outcome_expected,
                "project": project,
                "tags": tags,
                "created": today,
                "outcome": {
                    "tracked": False,
                    "outcome_text": "",
                    "success_level": "",
                    "lessons_learned": "",
                    "tracked_date": ""
                }
            }
            
            await _update_state_atomic_async(lambda cur: (lambda s: (
                s.setdefault("decisions", {}),
                s["decisions"].__setitem__(decision_id, decision),
                s
            )[-1])(cur or {}))
            
            # Fire-and-forget: neural learning runs in background, never blocks MCP response
            async def _enrich_decision():
                """Background enrichment — neural learning from decision."""
                if NEURAL_WEB_AVAILABLE:
                    try:
                        neural_web = get_neural_web_instance()
                        if neural_web:
                            learn_text = f"Decision: {decision_text}. Reasoning: {reasoning}"
                            await _steward_enhanced_learn(neural_web, learn_text)
                    except Exception as e:
                        logger.error(f"Neural web learn from decision failed: {e}")

            _fire_and_forget(_enrich_decision())

            return [TextContent(type="text", text=json.dumps({"success": True, "decision_id": decision_id, "decision": decision}, indent=2))]
        
        elif name == "get_decision":
            decision_id = arguments["decision_id"]
            decisions = state.get("decisions", {})
            if decision_id not in decisions:
                return [TextContent(type="text", text=json.dumps({"error": "Decision not found"}, indent=2))]
            return [TextContent(type="text", text=json.dumps(decisions[decision_id], indent=2))]
        
        elif name == "list_decisions":
            decisions = state.get("decisions", {})
            project_filter = arguments.get("project")
            has_outcome_filter = arguments.get("has_outcome")
            
            filtered = decisions
            if project_filter:
                filtered = {k: v for k, v in filtered.items() if v.get("project") == project_filter}
            if has_outcome_filter is not None:
                filtered = {k: v for k, v in filtered.items() if v.get("outcome", {}).get("tracked") == has_outcome_filter}
            
            # Sort by creation date (newest first)
            sorted_decisions = sorted(
                filtered.items(),
                key=lambda x: x[1].get("created", ""),
                reverse=True
            )
            
            return [TextContent(type="text", text=json.dumps({
                "decisions": dict(sorted_decisions),
                "count": len(sorted_decisions),
                "filters": {"project": project_filter, "has_outcome": has_outcome_filter}
            }, indent=2))]
        
        elif name == "track_decision_outcome":
            decision_id = arguments["decision_id"]
            outcome_text = arguments["outcome_text"]
            success_level = arguments["success_level"]
            lessons_learned = arguments.get("lessons_learned", "")
            today = datetime.now().strftime("%Y-%m-%d")
            
            def _track_outcome(cur: Dict[str, Any]) -> Dict[str, Any]:
                s = cur or {}
                if decision_id in s.get("decisions", {}):
                    decision = s["decisions"][decision_id]
                    decision["outcome"] = {
                        "tracked": True,
                        "outcome_text": outcome_text,
                        "success_level": success_level,
                        "lessons_learned": lessons_learned,
                        "tracked_date": today
                    }
                return s
            
            updated = await _update_state_atomic_async(_track_outcome)
            if decision_id in updated.get("decisions", {}):
                return [TextContent(type="text", text=json.dumps({"success": True, "decision": updated["decisions"][decision_id]}, indent=2))]
            return [TextContent(type="text", text=json.dumps({"error": "Decision not found"}, indent=2))]
        
        # === PATTERN ANALYSIS - COGNITIVE MODULES ===
        elif name == "get_insights":
            pressure_analysis = analyze_context_pressure(state)
            return [TextContent(type="text", text=json.dumps(pressure_analysis, indent=2))]
        
        elif name == "predict_cold_projects":
            pressure_analysis = analyze_context_pressure(state)
            cold_projects = [
                {"project": k, "urgency_score": v["urgency_score"], "days_stale": v["days_since_touch"]}
                for k, v in pressure_analysis["project_urgency"].items()
                if v["urgency_level"] in ["HIGH", "CRITICAL"]
            ]
            return [TextContent(type="text", text=json.dumps({"cold_projects": cold_projects}, indent=2))]
        
        elif name == "check_for_conflict":
            statement = arguments["statement"]
            sessions = log.get("sessions", [])
            conflict_analysis = check_statement_conflict(statement, sessions)
            return [TextContent(type="text", text=json.dumps(conflict_analysis, indent=2))]
        
        elif name == "get_story_arc":
            arc_analysis = get_story_arc_analysis(state, log)
            return [TextContent(type="text", text=json.dumps(arc_analysis, indent=2))]
        
        elif name == "get_affective_trends":
            affective_analysis = get_affective_trends_analysis(state, log)
            return [TextContent(type="text", text=json.dumps(affective_analysis, indent=2))]
        
        elif name == "get_patterns":
            return [TextContent(type="text", text=json.dumps({"message": "Pattern analysis available via cognitive modules"}, indent=2))]
        
        elif name == "analyze_productivity":
            days = int(arguments.get("days", 7))
            analysis = {"days_analyzed": days, "sessions": len(log.get("sessions", [])), "productivity": "steady"}
            return [TextContent(type="text", text=json.dumps(analysis, indent=2))]
        
        elif name == "get_suggested_actions":
            suggestions = ["Use get_insights for urgency analysis", "Use get_story_arc for narrative", "Use semantic_search for finding past work"]
            return [TextContent(type="text", text=json.dumps(suggestions, indent=2))]
        
        # === CONTEXT LOADING ===
        elif name == "search_files":
            # Search for files in REL directory matching query (threaded)
            query = arguments["query"].lower()
            limit = 50

            def _search_files_worker() -> Dict[str, Any]:
                found_files = []
                total_found = 0
                try:
                    for filepath in REL_PATH.rglob("*"):
                        if not filepath.is_file():
                            continue
                        hay = filepath.name.lower() + " " + str(filepath).lower()
                        if query in hay:
                            total_found += 1
                            if len(found_files) < limit:
                                try:
                                    st = filepath.stat()
                                    found_files.append({
                                        "path": str(filepath),
                                        "name": filepath.name,
                                        "size": st.st_size,
                                        "modified": datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                                    })
                                except Exception:
                                    # Still count it; skip metadata
                                    found_files.append({"path": str(filepath), "name": filepath.name})
                except Exception as e:
                    return {"error": str(e), "files": [], "query": query, "total_found": 0}

                return {"query": query, "files": found_files, "total_found": total_found}

            result = await asyncio.to_thread(_search_files_worker)
            if "error" in result:
                logger.error(f"File search error: {result['error']}")
                return [TextContent(type="text", text=json.dumps({"error": result["error"], "files": []}, indent=2))]

            return [TextContent(type="text", text=json.dumps({
                "query": query,
                "files": result["files"][:50],
                "total_found": result["total_found"]
            }, indent=2))]

        elif name == "load_context":
            # Load relevant context for a query (respects max_tokens)
            query = arguments["query"]
            max_tokens = int(arguments.get("max_tokens", 2000))
            context_parts: List[Dict[str, Any]] = []
            truncated = False

            def _estimate_tokens(obj: Any) -> int:
                # rough: 1 token ~= 4 chars
                try:
                    return len(json.dumps(obj, ensure_ascii=False)) // 4
                except Exception:
                    return 0

            def _try_add(part: Dict[str, Any]) -> None:
                nonlocal truncated
                if truncated:
                    return
                candidate = context_parts + [part]
                if _estimate_tokens(candidate) <= max_tokens:
                    context_parts.append(part)
                else:
                    truncated = True

            try:
                ql = query.lower()

                # 1) Relevant sessions (last 5)
                matching_sessions = [s for s in log.get("sessions", []) if ql in s.get("summary", "").lower()]
                if matching_sessions:
                    _try_add({"type": "sessions", "data": matching_sessions[-5:], "count": len(matching_sessions)})

                # 2) Relevant projects
                matching_projects = {
                    k: v for k, v in state.get("project_states", {}).items()
                    if ql in v.get("name", "").lower() or ql in v.get("description", "").lower()
                }
                if matching_projects:
                    _try_add({"type": "projects", "data": matching_projects, "count": len(matching_projects)})

                # 3) Relevant wins
                matching_wins = [w for w in state.get("recent_wins", []) if ql in w.get("win", "").lower()]
                if matching_wins:
                    _try_add({"type": "wins", "data": matching_wins[:10], "count": len(matching_wins)})

                # 4) Semantic search (FAISS)
                if BRAIN_AVAILABLE and not truncated:
                    brain = get_brain_instance()
                    if brain:
                        try:
                            semantic_results = await _brain_call(lambda: brain.search(query, 5))
                            if semantic_results:
                                _try_add({"type": "semantic_search", "data": semantic_results, "count": len(semantic_results)})
                        except Exception as e:
                            logger.error(f"Semantic search in load_context failed: {e}")

                # 5) Neural concepts
                if NEURAL_WEB_AVAILABLE and not truncated:
                    neural_web = get_neural_web_instance()
                    if neural_web:
                        try:
                            related = await _neural_call(lambda: neural_web.get_related_concepts(query, 10))
                            if related:
                                _try_add({"type": "neural_concepts", "data": related, "count": len(related)})
                        except Exception as e:
                            logger.error(f"Neural concepts in load_context failed: {e}")

                estimated_tokens = _estimate_tokens(context_parts)

            except Exception as e:
                logger.error(f"Load context error: {e}")
                return [TextContent(type="text", text=json.dumps({"error": str(e), "context": []}, indent=2))]

            return [TextContent(type="text", text=json.dumps({
                "query": query,
                "context": context_parts,
                "total_parts": len(context_parts),
                "estimated_tokens": estimated_tokens,
                "max_tokens": max_tokens,
                "truncated": truncated
            }, indent=2))]

        elif name == "get_loading_preview":
            # Preview what load_context would return without full data
            query = arguments["query"]
            preview = []
            
            try:
                # Count matching sessions
                session_matches = sum(1 for s in log.get("sessions", []) 
                                     if query.lower() in s.get("summary", "").lower())
                if session_matches > 0:
                    preview.append({
                        "type": "sessions",
                        "count": session_matches,
                        "preview": f"Would load {min(session_matches, 5)} of {session_matches} matching sessions"
                    })
                
                # Count matching projects
                project_matches = sum(1 for p in state.get("project_states", {}).values()
                                     if query.lower() in p.get("name", "").lower() or 
                                        query.lower() in p.get("description", "").lower())
                if project_matches > 0:
                    preview.append({
                        "type": "projects",
                        "count": project_matches,
                        "preview": f"Would load {project_matches} matching projects"
                    })
                
                # Count matching wins
                win_matches = sum(1 for w in state.get("recent_wins", [])
                                 if query.lower() in w.get("win", "").lower())
                if win_matches > 0:
                    preview.append({
                        "type": "wins",
                        "count": win_matches,
                        "preview": f"Would load {min(win_matches, 10)} of {win_matches} matching wins"
                    })
                
                # Add semantic search availability
                if BRAIN_AVAILABLE:
                    preview.append({
                        "type": "semantic_search",
                        "available": True,
                        "preview": "Would perform FAISS semantic search"
                    })
                
                # Add neural web availability
                if NEURAL_WEB_AVAILABLE:
                    preview.append({
                        "type": "neural_concepts",
                        "available": True,
                        "preview": "Would find related neural concepts"
                    })
                
            except Exception as e:
                logger.error(f"Loading preview error: {e}")
                return [TextContent(type="text", text=json.dumps({"error": str(e), "preview": []}, indent=2))]
            
            return [TextContent(type="text", text=json.dumps({
                "query": query,
                "preview": preview,
                "total_sources": len(preview)
            }, indent=2))]
        elif name == "get_recommendations":
            # Provide intelligent recommendations based on current state
            query = arguments.get("query", "").lower()
            recommendations = []
            
            try:
                # 1. Urgency-based recommendations
                pressure_analysis = analyze_context_pressure(state)
                high_urgency = [p for p in pressure_analysis["recommended_focus"] 
                               if p["urgency"] in ["HIGH", "CRITICAL"]]
                
                if high_urgency:
                    recommendations.append({
                        "type": "urgency",
                        "priority": "high",
                        "title": "High-urgency projects need attention",
                        "items": [f"{p['project']} ({p['urgency']})" for p in high_urgency]
                    })
                
                # 2. Stalled project recommendations
                stalled = [k for k, v in state.get("project_states", {}).items()
                          if v.get("status") == "active" and 
                          calculate_days_since(v.get("last_worked", "")) > 7]
                
                if stalled:
                    recommendations.append({
                        "type": "stalled_projects",
                        "priority": "medium",
                        "title": "Projects haven't been touched in 7+ days",
                        "items": stalled
                    })
                
                # 3. Near-completion recommendations
                near_done = [(k, v) for k, v in state.get("project_states", {}).items()
                            if v.get("status") == "active" and v.get("completion", 0) >= 70]
                
                if near_done:
                    recommendations.append({
                        "type": "near_completion",
                        "priority": "high",
                        "title": "Projects close to completion - finish strong!",
                        "items": [f"{k} ({v.get('completion')}%)" for k, v in near_done]
                    })
                
                # 4. Query-specific recommendations
                if query:
                    # Search for related work
                    related_sessions = [s for s in log.get("sessions", [])
                                       if query in s.get("summary", "").lower()]
                    
                    if related_sessions:
                        recommendations.append({
                            "type": "related_work",
                            "priority": "medium",
                            "title": f"Found {len(related_sessions)} past sessions related to '{query}'",
                            "items": [s.get("summary", "")[:100] for s in related_sessions[-3:]]
                        })
                    
                    # Search for related projects
                    related_projects = [(k, v) for k, v in state.get("project_states", {}).items()
                                       if query in v.get("name", "").lower() or 
                                          query in v.get("description", "").lower()]
                    
                    if related_projects:
                        recommendations.append({
                            "type": "related_projects",
                            "priority": "medium",
                            "title": f"Projects related to '{query}'",
                            "items": [f"{k}: {v.get('name')}" for k, v in related_projects]
                        })
                
                # 5. Learning opportunities (from neural web)
                if NEURAL_WEB_AVAILABLE and query:
                    neural_web = get_neural_web_instance()
                    if neural_web:
                        try:
                            related_concepts = await _neural_call(lambda: neural_web.get_related_concepts(query, 5))
                            if related_concepts:
                                formatted = []
                                for concept_item in related_concepts:
                                    strength_value = concept_item.get("weight", concept_item.get("strength", 0.0))
                                    try:
                                        strength_display = float(strength_value)
                                    except (TypeError, ValueError):
                                        strength_display = 0.0
                                    formatted.append(
                                        f"{concept_item.get('concept', 'unknown')} (strength: {strength_display:.2f})"
                                    )
                                recommendations.append({
                                    "type": "learning",
                                    "priority": "low",
                                    "title": f"Concepts related to '{query}' you might explore",
                                    "items": formatted,
                                })
                        except Exception as e:
                            logger.error(f"Neural recommendations error: {e}")
                
                # Sort by priority
                priority_order = {"high": 0, "medium": 1, "low": 2}
                recommendations.sort(key=lambda r: priority_order.get(r["priority"], 3))
                
            except Exception as e:
                logger.error(f"Recommendations error: {e}")
                return [TextContent(type="text", text=json.dumps({"error": str(e), "recommendations": []}, indent=2))]
            
            return [TextContent(type="text", text=json.dumps({
                "query": query if query else "general",
                "recommendations": recommendations,
                "total": len(recommendations)
            }, indent=2))]
        
        # === ADVANCED ===
        elif name == "get_analytics":
            analytics = {
                "total_sessions": len(log.get("sessions", [])),
                "total_projects": len(state.get("project_states", {})),
                "total_wins": len(state.get("recent_wins", [])),
                "monitoring": MONITORING.snapshot(),
            }
            
            # Add brain stats if available
            if BRAIN_AVAILABLE:
                brain = get_brain_instance()
                if brain:
                    try:
                        brain.initialize()
                        analytics["brain"] = brain.get_stats()
                    except Exception as e:
                        logger.error(f"Failed to get brain stats: {e}")
                        analytics["brain"] = {"error": str(e)}
            else:
                analytics["brain"] = {"status": "not_available"}
            
            # Add neural web stats
            if NEURAL_WEB_AVAILABLE:
                neural_web = get_neural_web_instance()
                if neural_web:
                    try:
                        analytics["neural_web"] = neural_web.get_stats()
                    except Exception as e:
                        logger.error(f"Failed to get neural web stats: {e}")
                        analytics["neural_web"] = {"error": str(e)}
            else:
                analytics["neural_web"] = {"status": "not_available"}
            
            return [TextContent(type="text", text=json.dumps(analytics, indent=2))]
            
        elif name == "create_snapshot":
            snapshot_name = arguments["name"]
            SNAPSHOTS_PATH.mkdir(parents=True, exist_ok=True)
            snapshot_path = SNAPSHOTS_PATH / f"{snapshot_name}.json"
            if snapshot_path.exists():
                timestamp_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
                snapshot_path = SNAPSHOTS_PATH / f"{snapshot_name}_{timestamp_suffix}.json"

            snapshot_payload = {
                "name": snapshot_name,
                "created_at": datetime.now().isoformat(),
                "state": state,
                "session_log": log,
            }
            atomic_write_json(snapshot_path, snapshot_payload)
            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "success": True,
                            "snapshot": snapshot_name,
                            "path": str(snapshot_path),
                        },
                        indent=2,
                    ),
                )
            ]
        elif name == "get_knowledge_graph":
            # Build knowledge graph from state and sessions
            nodes: List[Dict[str, Any]] = []
            edges: List[Dict[str, Any]] = []
            node_ids = set()

            def _add_node(node: Dict[str, Any]) -> None:
                nid = node.get("id")
                if nid and nid not in node_ids:
                    node_ids.add(nid)
                    nodes.append(node)

            try:
                # Project nodes
                for proj_key, proj in state.get("project_states", {}).items():
                    _add_node({
                        "id": f"project_{proj_key}",
                        "type": "project",
                        "label": proj.get("name", proj_key),
                        "status": proj.get("status"),
                        "completion": proj.get("completion", 0)
                    })

                # Idea nodes
                for idx, idea in enumerate(state.get("active_ideas", [])[:20]):
                    _add_node({
                        "id": f"idea_{idx}",
                        "type": "idea",
                        "label": idea[:50] + "..." if len(idea) > 50 else idea
                    })

                # Win nodes
                for idx, win in enumerate(state.get("recent_wins", [])[:20]):
                    _add_node({
                        "id": f"win_{idx}",
                        "type": "win",
                        "label": win.get("win", "")[:50],
                        "impact": win.get("impact")
                    })

                # Session nodes (last 30)
                for session in log.get("sessions", [])[-30:]:
                    sid = f"session_{session.get('session')}"
                    summary = session.get("summary", "")
                    _add_node({
                        "id": sid,
                        "type": "session",
                        "label": (summary[:50] + "...") if len(summary) > 50 else summary,
                        "date": session.get("date"),
                        "project": session.get("project"),
                        "status": session.get("status", "ended")
                    })

                    # Edge: session -> project
                    proj = session.get("project")
                    if proj:
                        edges.append({"source": sid, "target": f"project_{proj}", "type": "worked_on"})

                # Neural web strongest patterns
                if NEURAL_WEB_AVAILABLE:
                    neural_web = get_neural_web_instance()
                    if neural_web:
                        patterns = await _neural_call(lambda: neural_web.get_strongest_patterns(20))
                        for pattern in patterns:
                            src = pattern.get("source")
                            tgt = pattern.get("target")
                            if not src or not tgt:
                                continue
                            src_id = f"concept_{src}"
                            tgt_id = f"concept_{tgt}"
                            _add_node({"id": src_id, "type": "concept", "label": src})
                            _add_node({"id": tgt_id, "type": "concept", "label": tgt})
                            edges.append({
                                "source": src_id,
                                "target": tgt_id,
                                "type": "neural_connection",
                                "weight": pattern.get("weight"),
                                "strength": pattern.get("strength")
                            })

            except Exception as e:
                logger.error(f"Knowledge graph error: {e}")
                return [TextContent(type="text", text=json.dumps({"error": str(e), "nodes": [], "edges": []}, indent=2))]

            return [TextContent(type="text", text=json.dumps({
                "nodes": nodes,
                "edges": edges,
                "stats": {"total_nodes": len(nodes), "total_edges": len(edges)}
            }, indent=2))]

        elif name == "sync_obsidian":
            vault_raw = os.environ.get("REL_OBSIDIAN_VAULT_PATH", "").strip()
            vault_path = Path(vault_raw) if vault_raw else DEFAULT_OBSIDIAN_EXPORT_PATH
            vault_path.mkdir(parents=True, exist_ok=True)

            files_written = 0
            synced_projects = 0

            state_md = []
            state_md.append("# REL State Export")
            state_md.append("")
            state_md.append(f"- Exported: {datetime.now().isoformat()}")
            state_md.append(f"- Active Project: {state.get('current_context', {}).get('active_project')}")
            state_md.append(f"- Current Focus: {state.get('current_context', {}).get('current_focus', '')}")
            state_md.append("")
            state_md.append("## Active Projects")
            projects = state.get("project_states", {})
            for key, project in projects.items():
                if project.get("status") == "archived":
                    continue
                synced_projects += 1
                state_md.append(
                    f"- **{project.get('name', key)}** ({key}) | "
                    f"status: {project.get('status', 'active')} | completion: {project.get('completion', 0)}%"
                )

            state_path = vault_path / "REL_State.md"
            state_path.write_text("\n".join(state_md) + "\n", encoding="utf-8")
            files_written += 1

            sessions_md = []
            sessions_md.append("# REL Recent Sessions")
            sessions_md.append("")
            for session in log.get("sessions", [])[-50:]:
                sessions_md.append(
                    f"- {session.get('date', '')} {session.get('time', '')} | "
                    f"project: {session.get('project', 'n/a')} | {session.get('summary', '')}"
                )
            sessions_path = vault_path / "REL_Recent_Sessions.md"
            sessions_path.write_text("\n".join(sessions_md) + "\n", encoding="utf-8")
            files_written += 1

            project_notes_path = vault_path / "Projects"
            project_notes_path.mkdir(parents=True, exist_ok=True)
            for key, project in projects.items():
                safe_name = re.sub(r"[^a-zA-Z0-9_-]+", "_", key)[:80] or "project"
                note_path = project_notes_path / f"{safe_name}.md"
                note_lines = [
                    f"# {project.get('name', key)}",
                    "",
                    f"- Key: `{key}`",
                    f"- Status: {project.get('status', 'active')}",
                    f"- Priority: {project.get('priority', 'medium')}",
                    f"- Completion: {project.get('completion', 0)}%",
                    f"- Last Worked: {project.get('last_worked', 'n/a')}",
                    "",
                    "## Description",
                    project.get("description", ""),
                ]
                note_path.write_text("\n".join(note_lines) + "\n", encoding="utf-8")
                files_written += 1

            return [
                TextContent(
                    type="text",
                    text=json.dumps(
                        {
                            "success": True,
                            "message": "Obsidian export complete",
                            "vault_path": str(vault_path),
                            "files_written": files_written,
                            "projects_exported": synced_projects,
                        },
                        indent=2,
                    ),
                )
            ]
        
        elif name == "smart_load":
            # Smart load with brain ingestion
            query = arguments["query"].strip()
            ql = query.lower()
            matching_sessions = [s for s in log.get("sessions", []) if ql in s.get("summary", "").lower()]
            matching_projects = {
                k: v
                for k, v in state.get("project_states", {}).items()
                if ql in v.get("name", "").lower() or ql in v.get("description", "").lower()
            }
            matching_wins = [w for w in state.get("recent_wins", []) if ql in w.get("win", "").lower()]
            matching_ideas = [
                idea
                for idea in state.get("active_ideas", [])
                if isinstance(idea, str) and ql in idea.lower()
            ]
            total_matches = (
                len(matching_sessions) + len(matching_projects) + len(matching_wins) + len(matching_ideas)
            )

            result = {
                "loaded": True,
                "query": query,
                "matches": {
                    "sessions": len(matching_sessions),
                    "projects": len(matching_projects),
                    "wins": len(matching_wins),
                    "ideas": len(matching_ideas),
                    "total": total_matches,
                },
            }

            if BRAIN_AVAILABLE:
                brain = get_brain_instance()
                if brain:
                    try:
                        ingest_state = state
                        ingest_log = log
                        result["ingestion_scope"] = "query_matched" if total_matches > 0 else "full_fallback"
                        if total_matches > 0:
                            project_keys = set(matching_projects.keys())
                            state_projects = state.get("project_states", {})
                            if isinstance(state_projects, dict):
                                for session in matching_sessions:
                                    session_project = session.get("project")
                                    if isinstance(session_project, str) and session_project in state_projects:
                                        project_keys.add(session_project)
                            else:
                                state_projects = {}

                            scoped_projects = {
                                key: project
                                for key, project in state_projects.items()
                                if key in project_keys and isinstance(project, dict)
                            }
                            ingest_state = {
                                "project_states": scoped_projects,
                                "recent_wins": matching_wins,
                                "active_ideas": matching_ideas,
                            }
                            ingest_log = {"sessions": matching_sessions}

                        count = await _brain_call(lambda: brain.ingest_from_state_and_log(ingest_state, ingest_log))
                        result["ingested_to_brain"] = count
                        result["brain_stats"] = await _brain_call(lambda: brain.get_stats())
                    except Exception as e:
                        logger.error(f"Failed to ingest to brain: {e}")
                        result["brain_error"] = str(e)

            return [TextContent(type="text", text=json.dumps(result, indent=2))]

        # === BRAIN - SEMANTIC SEARCH ===
        elif name == "semantic_search":
            if not BRAIN_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Brain module not available", "results": []}, indent=2))]

            brain = get_brain_instance()
            if not brain:
                return [TextContent(type="text", text=json.dumps({"error": "Failed to initialize brain", "results": []}, indent=2))]

            try:
                query = arguments["query"]
                limit = int(arguments.get("limit", 5))
                results = await _brain_call(lambda: brain.search(query, limit))
                return [TextContent(type="text", text=json.dumps({"query": query, "results": results, "count": len(results)}, indent=2))]
            except Exception as e:
                logger.error(f"Semantic search failed: {e}")
                return [TextContent(type="text", text=json.dumps({"error": str(e), "results": []}, indent=2))]

        elif name == "neural_learn":
            if not NEURAL_WEB_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Neural web not available", "success": False}, indent=2))]

            neural_web = get_neural_web_instance()
            if not neural_web:
                return [TextContent(type="text", text=json.dumps({"error": "Failed to initialize neural web", "success": False}, indent=2))]

            try:
                text = arguments["text"]
                await _steward_enhanced_learn(neural_web, text)
                stats = await _neural_call(lambda: neural_web.get_stats())
                extraction_mode = "llm" if STEWARD_AVAILABLE else "naive"
                return [TextContent(type="text", text=json.dumps({"success": True, "learned_from": text[:100], "extraction_mode": extraction_mode, "neural_web_stats": stats}, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e), "success": False}, indent=2))]

        elif name == "neural_get_related":
            if not NEURAL_WEB_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Neural web not available", "related": []}, indent=2))]

            neural_web = get_neural_web_instance()
            if not neural_web:
                return [TextContent(type="text", text=json.dumps({"error": "Failed to initialize neural web", "related": []}, indent=2))]

            try:
                concept = arguments["concept"]
                limit = int(arguments.get("limit", 10))
                related = await _neural_call(lambda: neural_web.get_related_concepts(concept, limit))
                return [TextContent(type="text", text=json.dumps({"concept": concept, "related": related, "count": len(related)}, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e), "related": []}, indent=2))]

        elif name == "neural_get_patterns":
            if not NEURAL_WEB_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Neural web not available", "patterns": []}, indent=2))]

            neural_web = get_neural_web_instance()
            if not neural_web:
                return [TextContent(type="text", text=json.dumps({"error": "Failed to initialize neural web", "patterns": []}, indent=2))]

            try:
                limit = int(arguments.get("limit", 10))
                patterns = await _neural_call(lambda: neural_web.get_strongest_patterns(limit))
                return [TextContent(type="text", text=json.dumps({"patterns": patterns, "count": len(patterns)}, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e), "patterns": []}, indent=2))]

        elif name == "neural_apply_decay":
            if not NEURAL_WEB_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Neural web not available", "success": False}, indent=2))]

            neural_web = get_neural_web_instance()
            if not neural_web:
                return [TextContent(type="text", text=json.dumps({"error": "Failed to initialize neural web", "success": False}, indent=2))]

            try:
                days_threshold = int(arguments.get("days_threshold", 7))
                await _neural_call(lambda: (neural_web.apply_decay(days_threshold=days_threshold), neural_web.save()))
                stats = await _neural_call(lambda: neural_web.get_stats())
                return [TextContent(type="text", text=json.dumps({"success": True, "message": "Decay applied", "days_threshold": days_threshold, "neural_web_stats": stats}, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e), "success": False}, indent=2))]


        # WINDOWS DESKTOP TOOLS - Handlers
        elif name == "PowerShell":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.powershell, arguments.get("command", ""), int(arguments.get("timeout", 30)))
            return [TextContent(type="text", text=result)]

        elif name == "AppLaunch":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.app_tool, arguments.get("mode", "launch"), arguments.get("name"), arguments.get("window_loc"), arguments.get("window_size"))
            return [TextContent(type="text", text=str(result))]

        elif name == "Click":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.click, arguments.get("loc"), arguments.get("label"), arguments.get("button", "left"), int(arguments.get("clicks", 1)))
            return [TextContent(type="text", text=result)]

        elif name == "TypeText":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            clear = arguments.get("clear", False)
            if isinstance(clear, str): clear = clear.lower() == "true"
            pe = arguments.get("press_enter", False)
            if isinstance(pe, str): pe = pe.lower() == "true"
            result = await asyncio.to_thread(wb.type_text, arguments["text"], arguments.get("loc"), arguments.get("label"), clear, arguments.get("caret_position", "idle"), pe)
            return [TextContent(type="text", text=result)]

        elif name == "Scroll":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.scroll, arguments.get("loc"), arguments.get("label"), arguments.get("type", "vertical"), arguments.get("direction", "down"), int(arguments.get("wheel_times", 1)))
            return [TextContent(type="text", text=result)]

        elif name == "Move":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            drag = arguments.get("drag", False)
            if isinstance(drag, str): drag = drag.lower() == "true"
            result = await asyncio.to_thread(wb.move, arguments.get("loc"), arguments.get("label"), drag)
            return [TextContent(type="text", text=result)]

        elif name == "Shortcut":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.shortcut, arguments["shortcut"])
            return [TextContent(type="text", text=result)]

        elif name == "PauseSec":
            result = await asyncio.to_thread(wb.wait, int(arguments["duration"]))
            return [TextContent(type="text", text=result)]

        elif name == "Screenshot":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            ua = arguments.get("use_annotation", False)
            if isinstance(ua, str): ua = ua.lower() == "true"
            result = await asyncio.to_thread(wb.screenshot, ua, arguments.get("width_reference_line"), arguments.get("height_reference_line"), arguments.get("display"))
            if isinstance(result, list):
                return [TextContent(type="text", text=str(item)) if isinstance(item, str) else item for item in result]
            return [TextContent(type="text", text=str(result))]

        elif name == "DeskSnapshot":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            bools = {}
            for key in ("use_vision", "use_dom", "use_annotation", "use_ui_tree"):
                val = arguments.get(key, key in ("use_annotation", "use_ui_tree"))
                if isinstance(val, str): val = val.lower() == "true"
                bools[key] = val
            result = await asyncio.to_thread(wb.snapshot_tool, bools["use_vision"], bools["use_dom"], bools["use_annotation"], bools["use_ui_tree"], arguments.get("width_reference_line"), arguments.get("height_reference_line"), arguments.get("display"))
            if isinstance(result, list):
                return [TextContent(type="text", text=str(item)) if isinstance(item, str) else item for item in result]
            return [TextContent(type="text", text=str(result))]

        elif name == "WebScrape":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            ud = arguments.get("use_dom", False)
            if isinstance(ud, str): ud = ud.lower() == "true"
            result = await asyncio.to_thread(wb.scrape, arguments["url"], arguments.get("query"), ud)
            return [TextContent(type="text", text=result)]

        elif name == "MultiClick":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            pc = arguments.get("press_ctrl", True)
            if isinstance(pc, str): pc = pc.lower() == "true"
            result = await asyncio.to_thread(wb.multi_select, arguments.get("locs"), arguments.get("labels"), pc)
            return [TextContent(type="text", text=result)]

        elif name == "MultiEdit":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.multi_edit, arguments.get("locs"), arguments.get("labels"))
            return [TextContent(type="text", text=result)]

        elif name == "Clipboard":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.clipboard, arguments["mode"], arguments.get("text"))
            return [TextContent(type="text", text=result)]

        elif name == "Process":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            force = arguments.get("force", False)
            if isinstance(force, str): force = force.lower() == "true"
            result = await asyncio.to_thread(wb.process_tool, arguments["mode"], arguments.get("name"), arguments.get("pid"), arguments.get("sort_by", "memory"), int(arguments.get("limit", 20)), force)
            return [TextContent(type="text", text=result)]

        elif name == "Notification":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.notification, arguments["title"], arguments["message"])
            return [TextContent(type="text", text=str(result))]

        elif name == "Registry":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.registry, arguments["mode"], arguments["path"], arguments.get("name"), arguments.get("value"), arguments.get("type", "String"))
            return [TextContent(type="text", text=result)]

        elif name == "WinFileSystem":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            rec = arguments.get("recursive", False)
            if isinstance(rec, str): rec = rec.lower() == "true"
            ap = arguments.get("append", False)
            if isinstance(ap, str): ap = ap.lower() == "true"
            ow = arguments.get("overwrite", False)
            if isinstance(ow, str): ow = ow.lower() == "true"
            sh = arguments.get("show_hidden", False)
            if isinstance(sh, str): sh = sh.lower() == "true"
            result = await asyncio.to_thread(wb.win_filesystem, arguments["mode"], arguments["path"], arguments.get("destination"), arguments.get("content"), arguments.get("pattern"), rec, ap, ow, arguments.get("offset"), arguments.get("limit"), arguments.get("encoding", "utf-8"), sh)
            return [TextContent(type="text", text=result)]

        # NATIVE FILESYSTEM TOOLS - Handlers
        elif name == "fs_read_file":
            result = await asyncio.to_thread(fb.read_file, arguments["path"], arguments.get("head"), arguments.get("tail"))
            return [TextContent(type="text", text=result)]

        elif name == "fs_read_multiple":
            result = await asyncio.to_thread(fb.read_multiple_files, arguments["paths"])
            return [TextContent(type="text", text=result)]

        elif name == "fs_write_file":
            result = await asyncio.to_thread(fb.write_file, arguments["path"], arguments["content"])
            return [TextContent(type="text", text=result)]

        elif name == "fs_edit_file":
            dr = arguments.get("dry_run", False)
            if isinstance(dr, str): dr = dr.lower() == "true"
            result = await asyncio.to_thread(fb.edit_file, arguments["path"], arguments["edits"], dr)
            return [TextContent(type="text", text=result)]

        elif name == "fs_create_directory":
            result = await asyncio.to_thread(fb.create_directory, arguments["path"])
            return [TextContent(type="text", text=result)]

        elif name == "fs_list_directory":
            result = await asyncio.to_thread(fb.list_directory, arguments["path"])
            return [TextContent(type="text", text=result)]

        elif name == "fs_directory_tree":
            result = await asyncio.to_thread(fb.directory_tree, arguments["path"], int(arguments.get("max_depth", 3)))
            return [TextContent(type="text", text=result)]

        elif name == "fs_move_file":
            result = await asyncio.to_thread(fb.move_file, arguments["source"], arguments["destination"])
            return [TextContent(type="text", text=result)]

        elif name == "fs_search_files":
            result = await asyncio.to_thread(fb.search_files, arguments["path"], arguments["pattern"])
            return [TextContent(type="text", text=result)]

        elif name == "fs_get_file_info":
            result = await asyncio.to_thread(fb.get_file_info, arguments["path"])
            return [TextContent(type="text", text=result)]

        elif name == "fs_allowed_dirs":
            result = fb.list_allowed_directories()
            return [TextContent(type="text", text=result)]


        else:
            tool_status = "not_found"
            return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}, indent=2))]

    except Exception as e:
        tool_status = "error"
        logger.error(f"Error in {name}: {e}")
        return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]
    finally:
        MONITORING.record_tool_call(
            tool_name=name,
            status=tool_status,
            duration_ms=(time.perf_counter() - started) * 1000.0,
        )

# ============================================================================
# MAIN
# ============================================================================

async def main():
    """Run MCP server"""
    logger.info("=" * 80)
    logger.info("  REL (Radiant Ether Loom) - COMPLETE COGNITIVE ARCHITECTURE")
    logger.info("  Corwin's Memory That THINKS, ANALYZES, SEARCHES SEMANTICALLY, and LEARNS!")
    logger.info("=" * 80)
    logger.info(f"  Base Path: {REL_PATH}")
    logger.info("  âœ… All 87 Tools Operational (41 core + 4 neural + 10 task + 4 decision + 18 windows + 10 filesystem)")
    logger.info("  ðŸ§  Context Pressure â†’ get_insights, predict_cold_projects")
    logger.info("  ðŸ§  Contradiction Detection â†’ check_for_conflict")
    logger.info("  ðŸ§  Narrative Arc â†’ get_story_arc")
    logger.info("  ðŸ§  Affective Trends â†’ get_affective_trends")
    if BRAIN_AVAILABLE:
        logger.info("  ðŸ§  FAISS Brain â†’ semantic_search (ACTIVE)")
    else:
        logger.info("  âš ï¸  FAISS Brain â†’ Not available (install dependencies)")
    if NEURAL_WEB_AVAILABLE:
        logger.info("  ðŸ§  Neural Web â†’ AUTO-LEARNING from every session (ACTIVE)")
    else:
        logger.info("  âš ï¸  Neural Web â†’ Not available")
    logger.info("=" * 80)
    
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())

