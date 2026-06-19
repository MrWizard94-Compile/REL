"""
Filesystem Bridge for REL Codex Variant
========================================
Native Python implementation of filesystem operations.
Replaces the Anthropic Filesystem MCP Extension (Node.js server).

All operations respect allowed_directories configuration.
"""

import difflib
import fnmatch
import json
import logging
import os
import shutil
import stat
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("REL.filesystem")

# Default allowed directories - configurable via environment variable
_ALLOWED_DIRS: List[str] = []


def configure_allowed_dirs(dirs: Optional[List[str]] = None) -> None:
    """Configure which directories the filesystem bridge can access."""
    global _ALLOWED_DIRS
    if dirs:
        _ALLOWED_DIRS = [os.path.normpath(d) for d in dirs]
    else:
        # Default: all of C:\ (matching the current Filesystem Extension config)
        env_dirs = os.environ.get("FS_ALLOWED_DIRS", r"C:\\")
        _ALLOWED_DIRS = [os.path.normpath(d) for d in env_dirs.split(";") if d.strip()]
    logger.info("Filesystem bridge: allowed dirs = %s", _ALLOWED_DIRS)


def _check_access(path: str) -> bool:
    """Check if path is within allowed directories."""
    if not _ALLOWED_DIRS:
        configure_allowed_dirs()
    norm_path = os.path.normpath(os.path.abspath(path))
    return any(
        norm_path.startswith(os.path.normpath(d)) or norm_path == os.path.normpath(d)
        for d in _ALLOWED_DIRS
    )


def _deny_msg(path: str) -> str:
    return f"Access denied: {path} is not within allowed directories: {_ALLOWED_DIRS}"


# =============================================================================
# FILE READING
# =============================================================================


def read_file(path: str, head: Optional[int] = None, tail: Optional[int] = None) -> str:
    """Read the contents of a file as text."""
    if not _check_access(path):
        return _deny_msg(path)
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            if head is not None:
                lines = []
                for i, line in enumerate(f):
                    if i >= head:
                        break
                    lines.append(line)
                return "".join(lines)
            elif tail is not None:
                from collections import deque
                last_lines = deque(f, maxlen=tail)
                return "".join(last_lines)
            else:
                return f.read()
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


def read_multiple_files(paths: List[str]) -> str:
    """Read contents of multiple files."""
    results = []
    for p in paths:
        content = read_file(p)
        results.append(f"{p}:\n{content}")
    return "\n\n---\n".join(results)


# =============================================================================
# FILE WRITING
# =============================================================================


def write_file(path: str, content: str, create_dirs: bool = True) -> str:
    """Write content to a file (creates parent directories if needed)."""
    if not _check_access(path):
        return _deny_msg(path)
    try:
        if create_dirs:
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {path}"
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def edit_file(
    path: str,
    edits: List[Dict[str, Any]],
    dry_run: bool = False,
) -> str:
    """
    Apply edits to a file.
    Each edit: {"oldText": "...", "newText": "..."}
    """
    if not _check_access(path):
        return _deny_msg(path)
    try:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()

        modified = original
        for edit in edits:
            old_text = edit.get("oldText", "")
            new_text = edit.get("newText", "")
            if old_text not in modified:
                return f"Error: Could not find text to replace: {old_text[:100]}"
            modified = modified.replace(old_text, new_text, 1)

        if dry_run:
            diff = difflib.unified_diff(
                original.splitlines(keepends=True),
                modified.splitlines(keepends=True),
                fromfile=f"a/{os.path.basename(path)}",
                tofile=f"b/{os.path.basename(path)}",
            )
            return "".join(diff) or "No changes"

        with open(path, "w", encoding="utf-8") as f:
            f.write(modified)
        return f"Successfully edited {path}"
    except FileNotFoundError:
        return f"Error: File not found: {path}"
    except Exception as e:
        return f"Error editing file: {str(e)}"


# =============================================================================
# DIRECTORY OPERATIONS
# =============================================================================


def create_directory(path: str) -> str:
    """Create a directory (and parents)."""
    if not _check_access(path):
        return _deny_msg(path)
    try:
        os.makedirs(path, exist_ok=True)
        return f"Successfully created directory: {path}"
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error creating directory: {str(e)}"


def list_directory(path: str) -> str:
    """List directory contents with [FILE] and [DIR] prefixes."""
    if not _check_access(path):
        return _deny_msg(path)
    try:
        entries = sorted(os.listdir(path))
        lines = []
        for entry in entries:
            full_path = os.path.join(path, entry)
            if os.path.isdir(full_path):
                lines.append(f"[DIR] {entry}")
            else:
                lines.append(f"[FILE] {entry}")
        return "\n".join(lines) if lines else "(empty directory)"
    except FileNotFoundError:
        return f"Error: Directory not found: {path}"
    except PermissionError:
        return f"Error: Permission denied: {path}"
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def list_directory_with_sizes(path: str, sort_by: str = "name") -> str:
    """List directory with file sizes."""
    if not _check_access(path):
        return _deny_msg(path)
    try:
        entries = []
        for entry in os.listdir(path):
            full_path = os.path.join(path, entry)
            try:
                st = os.stat(full_path)
                size = st.st_size
                is_dir = stat.S_ISDIR(st.st_mode)
            except OSError:
                size = 0
                is_dir = False
            entries.append((entry, size, is_dir))

        if sort_by == "size":
            entries.sort(key=lambda x: x[1], reverse=True)
        else:
            entries.sort(key=lambda x: x[0].lower())

        lines = []
        for name, size, is_dir in entries:
            prefix = "[DIR]" if is_dir else "[FILE]"
            size_str = _format_size(size)
            lines.append(f"{prefix} {name} ({size_str})")
        return "\n".join(lines) if lines else "(empty directory)"
    except Exception as e:
        return f"Error listing directory: {str(e)}"


def _format_size(size: int) -> str:
    """Format file size in human-readable form."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.1f} {unit}" if unit != "B" else f"{size} {unit}"
        size /= 1024
    return f"{size:.1f} PB"


def directory_tree(path: str, max_depth: int = 3) -> str:
    """Get recursive directory tree as formatted text."""
    if not _check_access(path):
        return _deny_msg(path)

    def _build_tree(dir_path: str, prefix: str, depth: int) -> List[str]:
        if depth > max_depth:
            return [f"{prefix}..."]
        try:
            entries = sorted(os.listdir(dir_path))
        except PermissionError:
            return [f"{prefix}(permission denied)"]
        except OSError:
            return []

        # Filter out hidden/system
        entries = [e for e in entries if not e.startswith(".") and e != "node_modules" and e != "__pycache__"]

        lines = []
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "\\-- " if is_last else "|-- "
            full_path = os.path.join(dir_path, entry)
            if os.path.isdir(full_path):
                lines.append(f"{prefix}{connector}{entry}/")
                extension = "    " if is_last else "|   "
                lines.extend(_build_tree(full_path, prefix + extension, depth + 1))
            else:
                lines.append(f"{prefix}{connector}{entry}")
        return lines

    try:
        result = [f"{path}/"]
        result.extend(_build_tree(path, "", 1))
        return "\n".join(result)
    except Exception as e:
        return f"Error building tree: {str(e)}"


# =============================================================================
# FILE OPERATIONS
# =============================================================================


def move_file(source: str, destination: str) -> str:
    """Move or rename a file/directory."""
    if not _check_access(source):
        return _deny_msg(source)
    if not _check_access(destination):
        return _deny_msg(destination)
    try:
        shutil.move(source, destination)
        return f"Successfully moved {source} to {destination}"
    except FileNotFoundError:
        return f"Error: Source not found: {source}"
    except Exception as e:
        return f"Error moving file: {str(e)}"


def search_files(path: str, pattern: str, max_results: int = 50) -> str:
    """Search for files matching a pattern (glob or substring)."""
    if not _check_access(path):
        return _deny_msg(path)
    try:
        matches = []
        root = Path(path)
        for p in root.rglob("*"):
            if len(matches) >= max_results:
                break
            if fnmatch.fnmatch(p.name, pattern) or pattern.lower() in p.name.lower():
                matches.append(str(p))
        if matches:
            return "\n".join(matches)
        return f"No files matching '{pattern}' found in {path}"
    except Exception as e:
        return f"Error searching files: {str(e)}"


def get_file_info(path: str) -> str:
    """Get metadata about a file or directory."""
    if not _check_access(path):
        return _deny_msg(path)
    try:
        st = os.stat(path)
        info = {
            "path": path,
            "name": os.path.basename(path),
            "type": "directory" if stat.S_ISDIR(st.st_mode) else "file",
            "size": _format_size(st.st_size),
            "size_bytes": st.st_size,
            "created": datetime.fromtimestamp(st.st_ctime).isoformat(),
            "modified": datetime.fromtimestamp(st.st_mtime).isoformat(),
            "accessed": datetime.fromtimestamp(st.st_atime).isoformat(),
            "readable": os.access(path, os.R_OK),
            "writable": os.access(path, os.W_OK),
        }
        if not stat.S_ISDIR(st.st_mode):
            info["extension"] = os.path.splitext(path)[1]
        return json.dumps(info, indent=2)
    except FileNotFoundError:
        return f"Error: Path not found: {path}"
    except Exception as e:
        return f"Error getting file info: {str(e)}"


def list_allowed_directories() -> str:
    """List directories this server can access."""
    if not _ALLOWED_DIRS:
        configure_allowed_dirs()
    return "Allowed directories:\n" + "\n".join(_ALLOWED_DIRS)


# Initialize on import
configure_allowed_dirs()
