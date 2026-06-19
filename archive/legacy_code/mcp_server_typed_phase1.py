#!/usr/bin/env python3
"""
REL (Radiant Ether Loom) - Complete MCP Server with Cognitive Modules + FAISS Brain
Type-Safe Version - Phase 1: Core Infrastructure Complete

Corwin's persistent cognitive architecture
ALL 45 TOOLS + 4 COGNITIVE MODULES + FAISS BRAIN + NEURAL WEB LEARNING
This is MY complete memory system that can THINK, ANALYZE, SEARCH, and LEARN!
"""

import asyncio
import json
import logging
import os
import re
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

# Platform-specific file locking
if sys.platform == "win32":
    import msvcrt
else:
    import fcntl

# Setup logging
logging.basicConfig(level=logging.INFO)
logger: logging.Logger = logging.getLogger("REL")

# Base path (override with env var REL_PATH)
REL_PATH: Path = Path(os.environ.get("REL_PATH", "C:/REL"))
DATA_PATH: Path = REL_PATH / "data"
BRAIN_PATH: Path = DATA_PATH / "brain"
NEURAL_WEB_PATH: Path = DATA_PATH / "neural_web"
CORE_STATE_PATH: Path = DATA_PATH / "CoreState.json"
SESSION_LOG_PATH: Path = DATA_PATH / "SessionLog.json"

# Ensure folders exist
for _p in (REL_PATH, DATA_PATH, BRAIN_PATH, NEURAL_WEB_PATH):
    try:
        _p.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

# Add REL to path for brain import
sys.path.insert(0, str(REL_PATH))

# Import brain module with type checking
BRAIN_AVAILABLE: bool = False
try:
    from brain import RELBrain, get_brain

    BRAIN_AVAILABLE = True
    logger.info("✅ Brain module loaded successfully")
except ImportError as e:
    logger.warning(f"⚠️  Brain module not available: {e}")
    RELBrain = Any  # type: ignore
    get_brain = None  # type: ignore

# Import neural web module with type checking
NEURAL_WEB_AVAILABLE: bool = False
try:
    from neural_web import NeuralWeb, get_neural_web

    NEURAL_WEB_AVAILABLE = True
    logger.info("✅ Neural Web module loaded")
except ImportError as e:
    logger.warning(f"⚠️  Neural Web module not available: {e}")
    NeuralWeb = Any  # type: ignore
    get_neural_web = None  # type: ignore

# Create MCP server
app: Server = Server("rel")

# Global instances with proper types
_brain: Optional[Any] = None  # Will be RELBrain if available
_neural_web: Optional[Any] = None  # Will be NeuralWeb if available

# Async locks (prevent concurrent mutation of in-memory brain / neural web objects)
_brain_lock: asyncio.Lock = asyncio.Lock()
_neural_lock: asyncio.Lock = asyncio.Lock()


# ============================================================================
# ASYNC WRAPPER FUNCTIONS
# ============================================================================


async def _update_state_atomic_async(
    update_fn: Callable[[Dict[str, Any]], Dict[str, Any]]
) -> Dict[str, Any]:
    """Async wrapper for update_state_atomic
    
    Args:
        update_fn: Function that takes current state and returns updated state
        
    Returns:
        Updated state dictionary
    """
    return await asyncio.to_thread(update_state_atomic, update_fn)


async def _update_session_log_atomic_async(
    update_fn: Callable[[Dict[str, Any]], Dict[str, Any]]
) -> Dict[str, Any]:
    """Async wrapper for update_session_log_atomic
    
    Args:
        update_fn: Function that takes current log and returns updated log
        
    Returns:
        Updated session log dictionary
    """
    return await asyncio.to_thread(update_session_log_atomic, update_fn)


async def _brain_call(fn: Callable[[], Any]) -> Any:
    """Execute brain operation with locking
    
    Ensures only one brain operation runs at a time to prevent
    concurrent modification issues.
    
    Args:
        fn: Function to execute (brain operation)
        
    Returns:
        Result of the brain operation
    """
    async with _brain_lock:
        return await asyncio.to_thread(fn)


async def _neural_call(fn: Callable[[], Any]) -> Any:
    """Execute neural web operation with locking
    
    Ensures only one neural web operation runs at a time.
    
    Args:
        fn: Function to execute (neural web operation)
        
    Returns:
        Result of the neural web operation
    """
    async with _neural_lock:
        return await asyncio.to_thread(fn)


def get_brain_instance() -> Optional[Any]:
    """Get or create brain instance
    
    Returns:
        RELBrain instance if available, None otherwise
    """
    global _brain
    if _brain is None and BRAIN_AVAILABLE and get_brain is not None:
        _brain = get_brain(BRAIN_PATH)
    return _brain


def get_neural_web_instance() -> Optional[Any]:
    """Get or create neural web instance
    
    Returns:
        NeuralWeb instance if available, None otherwise
    """
    global _neural_web
    if _neural_web is None and NEURAL_WEB_AVAILABLE and get_neural_web is not None:
        _neural_web = get_neural_web(NEURAL_WEB_PATH)
    return _neural_web


# ============================================================================
# FILE LOCKING & VERSIONING FOR CONCURRENT ACCESS PROTECTION
# ============================================================================


class VersionConflictError(Exception):
    """Raised when version check fails during atomic update"""

    pass


@contextmanager
def file_lock(lock_path: Path, timeout: float = 10.0) -> Generator[None, None, None]:
    """Cross-platform file locking context manager
    
    Acquires exclusive lock, yields, then releases. Works on both
    Windows (msvcrt) and Unix (fcntl).
    
    Args:
        lock_path: Path to lock file
        timeout: Maximum seconds to wait for lock
        
    Yields:
        None
        
    Raises:
        TimeoutError: If lock cannot be acquired within timeout
    """
    lock_file: Optional[Any] = None
    acquired: bool = False
    start_time: float = time.time()

    try:
        # Create lock file parent directory if needed
        lock_path.parent.mkdir(parents=True, exist_ok=True)

        # Open lock file (create if doesn't exist)
        if sys.platform == "win32":
            # Windows: MUST use binary mode for msvcrt.locking
            lock_file = open(lock_path, "ab+")
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
            lock_file = open(lock_path, "a")

            # Try to acquire lock with timeout
            while time.time() - start_time < timeout:
                try:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    acquired = True
                    break
                except (IOError, OSError):
                    time.sleep(0.1)

        if not acquired:
            raise TimeoutError(
                f"Could not acquire lock on {lock_path} within {timeout}s"
            )

        yield

    finally:
        # Release lock
        if lock_file and acquired:
            try:
                if sys.platform == "win32":
                    lock_file.seek(0)
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
            except Exception:
                pass

        # Close file
        if lock_file:
            try:
                lock_file.close()
            except Exception:
                pass


def load_versioned_json(filepath: Path) -> Tuple[Dict[str, Any], int]:
    """Load JSON file with version number
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Tuple of (data dictionary, version number)
        Returns ({}, 0) if file not found
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)

        version: int = data.get("_version", 1)
        return data, version

    except FileNotFoundError:
        return {}, 0


def save_versioned_json(
    filepath: Path, data: Dict[str, Any], expected_version: Optional[int] = None
) -> None:
    """Save JSON file with version check and increment
    
    Implements optimistic locking by checking version number before save.
    
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
    data["_version"] = current_version + 1

    # Atomic write
    atomic_write_json(filepath, data)


def atomic_update(
    filepath: Path,
    lock_path: Path,
    update_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
    max_retries: int = 3,
) -> Dict[str, Any]:
    """Atomically update a JSON file with locking and version checking
    
    Pattern:
        1. Acquire file lock
        2. Load current data + version
        3. Apply update function
        4. Save with version check
        5. Release lock
        
    Implements retry logic with exponential backoff for version conflicts.
    
    Args:
        filepath: Path to JSON file
        lock_path: Path to lock file
        update_fn: Function that takes current data and returns updated data
        max_retries: Maximum retry attempts on version conflict
        
    Returns:
        Updated data dictionary
        
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
            time.sleep(0.1 * (2**attempt))
            logger.warning(
                f"Version conflict on {filepath}, retrying ({attempt + 1}/{max_retries})"
            )

    raise VersionConflictError(
        f"Failed to update {filepath} after {max_retries} attempts"
    )


# Convenience wrappers for CoreState and SessionLog
def update_state_atomic(
    update_fn: Callable[[Dict[str, Any]], Dict[str, Any]]
) -> Dict[str, Any]:
    """Atomically update CoreState.json
    
    Args:
        update_fn: Function that transforms state
        
    Returns:
        Updated state
    """
    lock_path = DATA_PATH / "CoreState.lock"
    return atomic_update(CORE_STATE_PATH, lock_path, update_fn)


def update_session_log_atomic(
    update_fn: Callable[[Dict[str, Any]], Dict[str, Any]]
) -> Dict[str, Any]:
    """Atomically update SessionLog.json
    
    Args:
        update_fn: Function that transforms session log
        
    Returns:
        Updated session log
    """
    lock_path = DATA_PATH / "SessionLog.lock"
    return atomic_update(SESSION_LOG_PATH, lock_path, update_fn)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def atomic_write_json(filepath: Path, data: Dict[str, Any]) -> None:
    """Atomic write to JSON file - prevents corruption on crash
    
    Writes to temporary file first, then atomically renames.
    This ensures the file is never in a half-written state.
    
    Args:
        filepath: Destination file path
        data: Data to write as JSON
        
    Raises:
        Exception: If write fails (temp file is cleaned up)
    """
    import os
    import tempfile

    # Write to temporary file in same directory
    temp_fd, temp_path = tempfile.mkstemp(
        dir=filepath.parent, prefix=f".{filepath.name}.", suffix=".tmp"
    )

    try:
        # Write JSON to temp file
        with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # Atomic rename (overwrites destination)
        # This is atomic on both Windows and Unix
        os.replace(temp_path, filepath)

    except Exception as e:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except Exception:
            pass
        raise e


def load_state() -> Dict[str, Any]:
    """Load CoreState.json
    
    Returns:
        State dictionary, or empty dict if file doesn't exist or is invalid
    """
    try:
        with open(CORE_STATE_PATH, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
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
    """Save CoreState.json atomically
    
    Args:
        state: State dictionary to save
    """
    atomic_write_json(CORE_STATE_PATH, state)


def load_session_log() -> Dict[str, Any]:
    """Load SessionLog.json
    
    Returns:
        Session log dictionary with 'sessions' key, or {"sessions": []} if not found
    """
    try:
        with open(SESSION_LOG_PATH, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
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
    """Save SessionLog.json atomically
    
    Args:
        log: Session log dictionary to save
    """
    atomic_write_json(SESSION_LOG_PATH, log)


def deep_merge(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    """Deep merge two dictionaries
    
    Recursively merges source into target. For nested dictionaries,
    performs deep merge. For other values, source overwrites target.
    
    Args:
        target: Target dictionary
        source: Source dictionary to merge in
        
    Returns:
        Merged dictionary (new dict, doesn't modify inputs)
    """
    output: Dict[str, Any] = {**target}
    for key, value in source.items():
        if (
            isinstance(value, dict)
            and key in target
            and isinstance(target[key], dict)
        ):
            output[key] = deep_merge(target[key], value)
        else:
            output[key] = value
    return output


def calculate_days_since(date_str: str) -> int:
    """Calculate days since a given date
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Number of days since the date, or 0 if date is invalid
    """
    if not date_str:
        return 0
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        delta = datetime.now() - date
        return delta.days
    except (ValueError, TypeError):
        return 0


# ============================================================================
# INFRASTRUCTURE COMPLETE - READY FOR COGNITIVE MODULES
# ============================================================================

# NOTE: Cognitive modules, tool definitions, and handlers follow in subsequent phases
# This completes Phase 1: Core Infrastructure with full type coverage
