#!/usr/bin/env python3
"""
REL Codex Variant — Unified Server Installer
=============================================
Patches mcp_server.py to include Windows-MCP and Filesystem tools.
Run this ONCE from the REL_Codex_Variant directory.

Usage:
    cd C:\REL_Codex_Variant
    .\.venv\Scripts\python.exe install_unified.py

What it does:
  1. Backs up mcp_server.py
  2. Copies windows_bridge.py and filesystem_bridge.py into place
  3. Patches mcp_server.py to import bridges and register new tools
  4. Updates claude_desktop_config.json
  5. Prints instructions for installing Windows-MCP dependencies
"""

import json
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

REL_DIR = Path(r"C:\REL_Codex_Variant")
MCP_SERVER = REL_DIR / "mcp_server.py"
CLAUDE_CONFIG = Path(os.environ.get(
    "CLAUDE_CONFIG",
    r"C:\Users\Bulkl\AppData\Roaming\Claude\claude_desktop_config.json"
))

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")


def backup_file(path: Path) -> Path:
    """Create timestamped backup."""
    backup = path.with_suffix(f".py.bak_{TIMESTAMP}")
    shutil.copy2(path, backup)
    print(f"  ✅ Backed up {path.name} → {backup.name}")
    return backup


# =============================================================================
# NEW TOOL DEFINITIONS (to insert into list_tools())
# =============================================================================

NEW_TOOL_DEFINITIONS = '''
        # ================================================================
        # WINDOWS DESKTOP TOOLS (18) — Merged from Windows-MCP Extension
        # ================================================================
        Tool(name="PowerShell", description="Execute PowerShell commands (with self-protection against killing REL server)", inputSchema={"type": "object", "properties": {"command": {"type": "string"}, "timeout": {"type": "number", "default": 30}}, "required": ["command"]}),
        Tool(name="App", description="Open/start/launch applications and manage windows. Modes: launch, resize, switch", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["launch", "resize", "switch"], "default": "launch"}, "name": {"type": "string"}, "window_loc": {"type": "array", "items": {"type": "integer"}}, "window_size": {"type": "array", "items": {"type": "integer"}}}}),
        Tool(name="Click", description="Mouse clicks at [x,y] or UI element label. button: left/right/middle, clicks: 0=hover,1=single,2=double", inputSchema={"type": "object", "properties": {"loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "button": {"type": "string", "default": "left"}, "clicks": {"type": "integer", "default": 1}}}),
        Tool(name="Type", description="Type text at [x,y] or label. clear=true to clear first, press_enter=true to submit", inputSchema={"type": "object", "properties": {"text": {"type": "string"}, "loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "clear": {"type": "boolean", "default": false}, "caret_position": {"type": "string", "default": "idle"}, "press_enter": {"type": "boolean", "default": false}}, "required": ["text"]}),
        Tool(name="Scroll", description="Scroll at [x,y] or label. vertical/horizontal, up/down/left/right", inputSchema={"type": "object", "properties": {"loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "type": {"type": "string", "default": "vertical"}, "direction": {"type": "string", "default": "down"}, "wheel_times": {"type": "integer", "default": 1}}}),
        Tool(name="Move", description="Move mouse to [x,y] or label. drag=true for drag-and-drop", inputSchema={"type": "object", "properties": {"loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "drag": {"type": "boolean", "default": false}}}),
        Tool(name="Shortcut", description="Execute keyboard shortcuts (e.g. ctrl+c, alt+tab, win+r)", inputSchema={"type": "object", "properties": {"shortcut": {"type": "string"}}, "required": ["shortcut"]}),
        Tool(name="Wait", description="Pause execution for N seconds", inputSchema={"type": "object", "properties": {"duration": {"type": "integer"}}, "required": ["duration"]}),
        Tool(name="Screenshot", description="Fast screenshot with cursor position and window info", inputSchema={"type": "object", "properties": {"use_annotation": {"type": "boolean", "default": false}, "width_reference_line": {"type": "integer"}, "height_reference_line": {"type": "integer"}, "display": {"type": "array", "items": {"type": "integer"}}}}),
        Tool(name="Snapshot", description="Full desktop state: windows, interactive elements, scrollable areas. use_vision for screenshot, use_dom for browser DOM", inputSchema={"type": "object", "properties": {"use_vision": {"type": "boolean", "default": false}, "use_dom": {"type": "boolean", "default": false}, "use_annotation": {"type": "boolean", "default": true}, "use_ui_tree": {"type": "boolean", "default": true}, "width_reference_line": {"type": "integer"}, "height_reference_line": {"type": "integer"}, "display": {"type": "array", "items": {"type": "integer"}}}}),
        Tool(name="Scrape", description="Fetch web page content from URL. use_dom=true for active browser tab", inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "query": {"type": "string"}, "use_dom": {"type": "boolean", "default": false}}, "required": ["url"]}),
        Tool(name="MultiSelect", description="Select multiple items via locs [[x,y],...] or labels [id,...]. press_ctrl for multi-select", inputSchema={"type": "object", "properties": {"locs": {"type": "array", "items": {"type": "array", "items": {"type": "integer"}}}, "labels": {"type": "array", "items": {"type": "integer"}}, "press_ctrl": {"type": "boolean", "default": true}}}),
        Tool(name="MultiEdit", description="Edit multiple input fields via locs [[x,y,text],...] or labels [[label,text],...]", inputSchema={"type": "object", "properties": {"locs": {"type": "array"}, "labels": {"type": "array"}}}),
        Tool(name="Clipboard", description="Clipboard operations. mode=get to read, mode=set to write", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["get", "set"]}, "text": {"type": "string"}}, "required": ["mode"]}),
        Tool(name="Process", description="List or kill processes (with self-protection). mode=list or mode=kill", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["list", "kill"]}, "name": {"type": "string"}, "pid": {"type": "integer"}, "sort_by": {"type": "string", "default": "memory"}, "limit": {"type": "integer", "default": 20}, "force": {"type": "boolean", "default": false}}, "required": ["mode"]}),
        Tool(name="Notification", description="Send Windows toast notification", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "message": {"type": "string"}}, "required": ["title", "message"]}),
        Tool(name="Registry", description="Windows Registry: get/set/delete/list", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["get", "set", "delete", "list"]}, "path": {"type": "string"}, "name": {"type": "string"}, "value": {"type": "string"}, "type": {"type": "string", "default": "String"}}, "required": ["mode", "path"]}),
        Tool(name="WinFileSystem", description="Windows file operations: read/write/copy/move/delete/list/search/info (relative paths from Desktop)", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["read", "write", "copy", "move", "delete", "list", "search", "info"]}, "path": {"type": "string"}, "destination": {"type": "string"}, "content": {"type": "string"}, "pattern": {"type": "string"}, "recursive": {"type": "boolean", "default": false}, "append": {"type": "boolean", "default": false}, "overwrite": {"type": "boolean", "default": false}, "offset": {"type": "integer"}, "limit": {"type": "integer"}, "encoding": {"type": "string", "default": "utf-8"}, "show_hidden": {"type": "boolean", "default": false}}, "required": ["mode", "path"]}),

        # ================================================================
        # NATIVE FILESYSTEM TOOLS (10) — Merged from Filesystem Extension
        # ================================================================
        Tool(name="fs_read_file", description="Read file contents as text", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "head": {"type": "integer"}, "tail": {"type": "integer"}}, "required": ["path"]}),
        Tool(name="fs_read_multiple", description="Read multiple files at once", inputSchema={"type": "object", "properties": {"paths": {"type": "array", "items": {"type": "string"}}}, "required": ["paths"]}),
        Tool(name="fs_write_file", description="Write content to file", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}),
        Tool(name="fs_edit_file", description="Apply edits to a file (find and replace)", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "edits": {"type": "array", "items": {"type": "object", "properties": {"oldText": {"type": "string"}, "newText": {"type": "string"}}}}, "dry_run": {"type": "boolean", "default": false}}, "required": ["path", "edits"]}),
        Tool(name="fs_create_directory", description="Create directory (with parents)", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        Tool(name="fs_list_directory", description="List directory contents", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        Tool(name="fs_directory_tree", description="Recursive directory tree view", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "max_depth": {"type": "integer", "default": 3}}, "required": ["path"]}),
        Tool(name="fs_move_file", description="Move or rename file/directory", inputSchema={"type": "object", "properties": {"source": {"type": "string"}, "destination": {"type": "string"}}, "required": ["source", "destination"]}),
        Tool(name="fs_search_files", description="Search for files by name/pattern", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "pattern": {"type": "string"}}, "required": ["path", "pattern"]}),
        Tool(name="fs_get_file_info", description="Get file/directory metadata", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        Tool(name="fs_allowed_dirs", description="List allowed directories", inputSchema={"type": "object", "properties": {}}),
'''

# =============================================================================
# NEW TOOL HANDLERS (to insert into handle_call_tool())
# =============================================================================

NEW_TOOL_HANDLERS = '''
        # ================================================================
        # WINDOWS DESKTOP TOOLS — Handlers
        # ================================================================
        elif name == "PowerShell":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.powershell, arguments.get("command", ""), int(arguments.get("timeout", 30)))
            return [TextContent(type="text", text=result)]

        elif name == "App":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.app_tool, arguments.get("mode", "launch"), arguments.get("name"), arguments.get("window_loc"), arguments.get("window_size"))
            return [TextContent(type="text", text=str(result))]

        elif name == "Click":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            result = await asyncio.to_thread(wb.click, arguments.get("loc"), arguments.get("label"), arguments.get("button", "left"), int(arguments.get("clicks", 1)))
            return [TextContent(type="text", text=result)]

        elif name == "Type":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            clear = arguments.get("clear", False)
            if isinstance(clear, str): clear = clear.lower() == "true"
            press_enter = arguments.get("press_enter", False)
            if isinstance(press_enter, str): press_enter = press_enter.lower() == "true"
            result = await asyncio.to_thread(wb.type_text, arguments["text"], arguments.get("loc"), arguments.get("label"), clear, arguments.get("caret_position", "idle"), press_enter)
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

        elif name == "Wait":
            result = await asyncio.to_thread(wb.wait, int(arguments["duration"]))
            return [TextContent(type="text", text=result)]

        elif name == "Screenshot":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            use_annotation = arguments.get("use_annotation", False)
            if isinstance(use_annotation, str): use_annotation = use_annotation.lower() == "true"
            result = await asyncio.to_thread(wb.screenshot, use_annotation, arguments.get("width_reference_line"), arguments.get("height_reference_line"), arguments.get("display"))
            if isinstance(result, list):
                return [TextContent(type="text", text=str(item)) if isinstance(item, str) else item for item in result]
            return [TextContent(type="text", text=str(result))]

        elif name == "Snapshot":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            bools = {}
            for key in ("use_vision", "use_dom", "use_annotation", "use_ui_tree"):
                val = arguments.get(key, key == "use_annotation" or key == "use_ui_tree")
                if isinstance(val, str): val = val.lower() == "true"
                bools[key] = val
            result = await asyncio.to_thread(wb.snapshot, bools["use_vision"], bools["use_dom"], bools["use_annotation"], bools["use_ui_tree"], arguments.get("width_reference_line"), arguments.get("height_reference_line"), arguments.get("display"))
            if isinstance(result, list):
                return [TextContent(type="text", text=str(item)) if isinstance(item, str) else item for item in result]
            return [TextContent(type="text", text=str(result))]

        elif name == "Scrape":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            use_dom = arguments.get("use_dom", False)
            if isinstance(use_dom, str): use_dom = use_dom.lower() == "true"
            result = await asyncio.to_thread(wb.scrape, arguments["url"], arguments.get("query"), use_dom)
            return [TextContent(type="text", text=result)]

        elif name == "MultiSelect":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            press_ctrl = arguments.get("press_ctrl", True)
            if isinstance(press_ctrl, str): press_ctrl = press_ctrl.lower() == "true"
            result = await asyncio.to_thread(wb.multi_select, arguments.get("locs"), arguments.get("labels"), press_ctrl)
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
            recursive = arguments.get("recursive", False)
            if isinstance(recursive, str): recursive = recursive.lower() == "true"
            append = arguments.get("append", False)
            if isinstance(append, str): append = append.lower() == "true"
            overwrite = arguments.get("overwrite", False)
            if isinstance(overwrite, str): overwrite = overwrite.lower() == "true"
            show_hidden = arguments.get("show_hidden", False)
            if isinstance(show_hidden, str): show_hidden = show_hidden.lower() == "true"
            result = await asyncio.to_thread(wb.win_filesystem, arguments["mode"], arguments["path"], arguments.get("destination"), arguments.get("content"), arguments.get("pattern"), recursive, append, overwrite, arguments.get("offset"), arguments.get("limit"), arguments.get("encoding", "utf-8"), show_hidden)
            return [TextContent(type="text", text=result)]

        # ================================================================
        # NATIVE FILESYSTEM TOOLS — Handlers
        # ================================================================
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
            dry_run = arguments.get("dry_run", False)
            if isinstance(dry_run, str): dry_run = dry_run.lower() == "true"
            result = await asyncio.to_thread(fb.edit_file, arguments["path"], arguments["edits"], dry_run)
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
'''

# =============================================================================
# IMPORT BLOCK (to add near top of mcp_server.py after other imports)
# =============================================================================

IMPORT_BLOCK = '''
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
'''


# =============================================================================
# PATCH LOGIC
# =============================================================================

def patch_mcp_server():
    """Apply patches to mcp_server.py to register new tools."""
    print("\n📝 Patching mcp_server.py...")

    with open(MCP_SERVER, "r", encoding="utf-8") as f:
        content = f.read()

    # --- 1. Add import block ---
    # Insert after the last import section (after steward import)
    steward_marker = "STEWARD_AVAILABLE = False"
    if steward_marker in content:
        # Find the end of the steward import block
        idx = content.index(steward_marker)
        # Find the next blank line after it
        next_newline = content.index("\n\n", idx)
        insert_point = next_newline
        if "import windows_bridge" not in content:
            content = content[:insert_point] + "\n" + IMPORT_BLOCK + content[insert_point:]
            print("  ✅ Added bridge imports")
        else:
            print("  ⏭️  Bridge imports already present")
    else:
        # Fallback: insert before "# Create MCP server"
        marker = "# Create MCP server"
        if marker in content and "import windows_bridge" not in content:
            idx = content.index(marker)
            content = content[:idx] + IMPORT_BLOCK + "\n" + content[idx:]
            print("  ✅ Added bridge imports (fallback position)")
        else:
            print("  ⚠️  Could not find insertion point for imports")

    # --- 2. Add tool definitions to list_tools() ---
    # Find the last Tool() entry before the closing bracket
    # Look for the neural_apply_decay tool (last defined tool)
    decay_marker = '"neural_apply_decay"'
    if decay_marker in content:
        # Find the end of that Tool() entry
        idx = content.index(decay_marker)
        # Find the closing })  of that Tool entry
        close_idx = content.index("})", idx) + 2
        # Find the next ] which closes the return list
        bracket_idx = content.index("]", close_idx)

        if "PowerShell" not in content.split("list_tools")[1].split("handle_call_tool")[0]:
            # Insert new tools before the closing ]
            content = content[:bracket_idx] + ",\n" + NEW_TOOL_DEFINITIONS + "\n    " + content[bracket_idx:]
            print("  ✅ Added 28 new tool definitions to list_tools()")
        else:
            print("  ⏭️  Tool definitions already present")
    else:
        print("  ⚠️  Could not find neural_apply_decay marker for tool insertion")

    # --- 3. Add tool handlers to handle_call_tool() ---
    # Find the "else: tool_status = not_found" block
    notfound_marker = 'tool_status = "not_found"'
    if notfound_marker in content:
        idx = content.index(notfound_marker)
        # Go back to find the "else:" before it
        else_idx = content.rindex("else:", 0, idx)

        if "elif name == \"PowerShell\":" not in content:
            # Insert new handlers before the final else
            content = content[:else_idx] + NEW_TOOL_HANDLERS + "\n        " + content[else_idx:]
            print("  ✅ Added 28 new tool handlers to handle_call_tool()")
        else:
            print("  ⏭️  Tool handlers already present")
    else:
        print("  ⚠️  Could not find not_found marker for handler insertion")

    # --- 4. Add cleanup to main() ---
    if "wb.shutdown()" not in content:
        # Add atexit handler after the imports
        atexit_code = "\nimport atexit\n\ndef _cleanup_bridges():\n    if WINDOWS_AVAILABLE:\n        try:\n            wb.shutdown()\n        except Exception:\n            pass\n\natexit.register(_cleanup_bridges)\n"

        # Insert after the bridge imports
        if "FILESYSTEM_AVAILABLE = False" in content:
            idx = content.index("FILESYSTEM_AVAILABLE = False")
            end = content.index("\n", idx) + 1
            content = content[:end] + atexit_code + content[end:]
            print("  ✅ Added atexit cleanup handler")

    # --- 5. Update tool count in banner ---
    content = content.replace(
        "All 59 Tools Operational (41 core + 4 neural learning + 10 task tracking + 4 decision log)",
        "All 87 Tools Operational (41 core + 4 neural + 10 task + 4 decision + 18 windows + 10 filesystem)"
    )

    # Write patched file
    with open(MCP_SERVER, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"  ✅ Patched mcp_server.py ({len(content)} chars)")


def update_config():
    """Update claude_desktop_config.json to use unified server only."""
    print("\n📝 Updating Claude Desktop config...")

    # Backup
    if CLAUDE_CONFIG.exists():
        backup = CLAUDE_CONFIG.with_suffix(f".json.bak_{TIMESTAMP}")
        shutil.copy2(CLAUDE_CONFIG, backup)
        print(f"  ✅ Backed up config → {backup.name}")

        with open(CLAUDE_CONFIG, "r") as f:
            config = json.load(f)
    else:
        config = {}

    # Ensure mcpServers has only our unified server
    config["mcpServers"] = {
        "rel_codex_variant": {
            "command": str(REL_DIR / ".venv" / "Scripts" / "python.exe"),
            "args": [str(REL_DIR / "mcp_server.py")],
            "env": {
                "REL_PATH": str(REL_DIR),
                "WINDOWS_MCP_SRC": str(Path(r"C:\Users\Bulkl\AppData\Roaming\Claude\Claude Extensions\ant.dir.cursortouch.windows-mcp\src")),
                "FS_ALLOWED_DIRS": "C:\\"
            }
        }
    }

    # Preserve preferences
    if "preferences" not in config:
        config["preferences"] = {}

    with open(CLAUDE_CONFIG, "w") as f:
        json.dump(config, f, indent=2)

    print("  ✅ Config updated — unified server only")
    print("  ℹ️  Note: Windows-MCP and Filesystem Extensions can be disabled in Claude Desktop settings")


def main():
    print("=" * 70)
    print("  REL Codex Variant — Unified Server Installer")
    print("=" * 70)

    # Step 1: Backup
    print("\n📦 Creating backups...")
    backup_file(MCP_SERVER)

    # Step 2: Copy bridge modules
    print("\n📦 Checking bridge modules...")
    for module in ("windows_bridge.py", "filesystem_bridge.py"):
        target = REL_DIR / module
        if target.exists():
            print(f"  ✅ {module} already in place")
        else:
            print(f"  ⚠️  {module} not found at {target}")
            print(f"      Please copy it to {REL_DIR}")

    # Step 3: Patch mcp_server.py
    patch_mcp_server()

    # Step 4: Update config
    update_config()

    # Step 5: Print dependency install instructions
    print("\n" + "=" * 70)
    print("  NEXT STEPS")
    print("=" * 70)
    print("""
1. COPY BRIDGE MODULES (if not already done):
   Copy windows_bridge.py and filesystem_bridge.py to C:\\REL_Codex_Variant\\

2. INSTALL WINDOWS-MCP DEPENDENCIES into REL's venv:
   cd C:\\REL_Codex_Variant
   .venv\\Scripts\\pip.exe install pywin32 psutil pillow dxcam comtypes ^
       markdownify fuzzywuzzy python-levenshtein platformdirs requests ^
       tabulate click python-dotenv mss --break-system-packages

3. DISABLE EXTENSIONS in Claude Desktop:
   Settings → Extensions → Disable "Windows-MCP" and "Filesystem"
   (Keep them installed as backup — just disable to avoid conflicts)

4. RESTART Claude Desktop completely (close + reopen)

5. TEST by calling any tool:
   - Try: rel_codex_variant:PowerShell with command "echo hello"
   - Try: rel_codex_variant:fs_list_directory with path "C:\\"
""")


if __name__ == "__main__":
    main()
