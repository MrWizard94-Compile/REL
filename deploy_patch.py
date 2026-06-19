#!/usr/bin/env python3
"""Deploy patched mcp_server.py from clean backup. Run once then delete."""
import json, shutil, sys
from pathlib import Path
from datetime import datetime

REL = Path(r"C:\REL_Codex_Variant")
BAK = REL / "mcp_server.py.bak_20260327_012732"
OUT = REL / "mcp_server.py"
CFG = Path(r"C:\Users\Bulkl\AppData\Roaming\Claude\claude_desktop_config.json")
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

if not BAK.exists():
    print(f"ERROR: Backup not found at {BAK}")
    sys.exit(1)

# Backup current broken version
broken_bak = OUT.with_suffix(f".py.broken_{TS}")
if OUT.exists():
    shutil.copy2(OUT, broken_bak)
    print(f"Backed up broken version to {broken_bak.name}")

lines = BAK.read_text(encoding="utf-8").splitlines(keepends=True)
print(f"Read {len(lines)} lines from clean backup")

# === PATCH 1: Bridge imports after STEWARD_AVAILABLE = False ===
IMPORT_BLOCK = """
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

"""

insert_idx = None
for i, line in enumerate(lines):
    if "STEWARD_AVAILABLE = False" in line and "logger" not in line:
        insert_idx = i + 1
        break
assert insert_idx, "Could not find STEWARD_AVAILABLE = False"
import_lines = [l + "\n" for l in IMPORT_BLOCK.split("\n")]
lines = lines[:insert_idx] + import_lines + lines[insert_idx:]
print(f"P1: Inserted bridge imports at line {insert_idx}")

# === PATCH 2: Rename server ===
for i, line in enumerate(lines):
    if 'app = Server("rel")' in line:
        lines[i] = 'app = Server("REL")\n'
        print(f"P2: Renamed server to REL at line {i+1}")
        break

# === PATCH 3: Update banner ===
for i, line in enumerate(lines):
    if "All 59 Tools Operational" in line:
        lines[i] = lines[i].replace(
            "All 59 Tools Operational (41 core + 4 neural learning + 10 task tracking + 4 decision log)",
            "All 87 Tools Operational (41 core + 4 neural + 10 task + 4 decision + 18 windows + 10 filesystem)"
        )
        print(f"P3: Updated banner at line {i+1}")
        break

# === PATCH 4: Tool definitions ===
TOOL_DEFS = '''
        # WINDOWS DESKTOP TOOLS (18)
        Tool(name="PowerShell", description="Execute PowerShell commands (with self-protection)", inputSchema={"type": "object", "properties": {"command": {"type": "string"}, "timeout": {"type": "number", "default": 30}}, "required": ["command"]}),
        Tool(name="App", description="Launch/resize/switch applications", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["launch", "resize", "switch"], "default": "launch"}, "name": {"type": "string"}, "window_loc": {"type": "array", "items": {"type": "integer"}}, "window_size": {"type": "array", "items": {"type": "integer"}}}}),
        Tool(name="Click", description="Mouse clicks at [x,y] or UI label", inputSchema={"type": "object", "properties": {"loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "button": {"type": "string", "default": "left"}, "clicks": {"type": "integer", "default": 1}}}),
        Tool(name="Type", description="Type text at [x,y] or label", inputSchema={"type": "object", "properties": {"text": {"type": "string"}, "loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "clear": {"type": "boolean"}, "caret_position": {"type": "string"}, "press_enter": {"type": "boolean"}}, "required": ["text"]}),
        Tool(name="Scroll", description="Scroll at [x,y] or label", inputSchema={"type": "object", "properties": {"loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "type": {"type": "string", "default": "vertical"}, "direction": {"type": "string", "default": "down"}, "wheel_times": {"type": "integer", "default": 1}}}),
        Tool(name="Move", description="Move mouse or drag", inputSchema={"type": "object", "properties": {"loc": {"type": "array", "items": {"type": "integer"}}, "label": {"type": "integer"}, "drag": {"type": "boolean"}}}),
        Tool(name="Shortcut", description="Keyboard shortcuts", inputSchema={"type": "object", "properties": {"shortcut": {"type": "string"}}, "required": ["shortcut"]}),
        Tool(name="Wait", description="Pause N seconds", inputSchema={"type": "object", "properties": {"duration": {"type": "integer"}}, "required": ["duration"]}),
        Tool(name="Screenshot", description="Fast screenshot", inputSchema={"type": "object", "properties": {"use_annotation": {"type": "boolean"}, "width_reference_line": {"type": "integer"}, "height_reference_line": {"type": "integer"}, "display": {"type": "array", "items": {"type": "integer"}}}}),
        Tool(name="Snapshot", description="Full desktop state with UI tree", inputSchema={"type": "object", "properties": {"use_vision": {"type": "boolean"}, "use_dom": {"type": "boolean"}, "use_annotation": {"type": "boolean"}, "use_ui_tree": {"type": "boolean"}, "width_reference_line": {"type": "integer"}, "height_reference_line": {"type": "integer"}, "display": {"type": "array", "items": {"type": "integer"}}}}),
        Tool(name="Scrape", description="Fetch web page content", inputSchema={"type": "object", "properties": {"url": {"type": "string"}, "query": {"type": "string"}, "use_dom": {"type": "boolean"}}, "required": ["url"]}),
        Tool(name="MultiSelect", description="Select multiple items", inputSchema={"type": "object", "properties": {"locs": {"type": "array"}, "labels": {"type": "array"}, "press_ctrl": {"type": "boolean", "default": true}}}),
        Tool(name="MultiEdit", description="Edit multiple fields", inputSchema={"type": "object", "properties": {"locs": {"type": "array"}, "labels": {"type": "array"}}}),
        Tool(name="Clipboard", description="Clipboard get/set", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["get", "set"]}, "text": {"type": "string"}}, "required": ["mode"]}),
        Tool(name="Process", description="List/kill processes (self-protected)", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["list", "kill"]}, "name": {"type": "string"}, "pid": {"type": "integer"}, "sort_by": {"type": "string"}, "limit": {"type": "integer"}, "force": {"type": "boolean"}}, "required": ["mode"]}),
        Tool(name="Notification", description="Windows toast notification", inputSchema={"type": "object", "properties": {"title": {"type": "string"}, "message": {"type": "string"}}, "required": ["title", "message"]}),
        Tool(name="Registry", description="Windows Registry ops", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["get", "set", "delete", "list"]}, "path": {"type": "string"}, "name": {"type": "string"}, "value": {"type": "string"}, "type": {"type": "string"}}, "required": ["mode", "path"]}),
        Tool(name="WinFileSystem", description="Win file ops: read/write/copy/move/delete/list/search/info", inputSchema={"type": "object", "properties": {"mode": {"type": "string", "enum": ["read", "write", "copy", "move", "delete", "list", "search", "info"]}, "path": {"type": "string"}, "destination": {"type": "string"}, "content": {"type": "string"}, "pattern": {"type": "string"}, "recursive": {"type": "boolean"}, "append": {"type": "boolean"}, "overwrite": {"type": "boolean"}, "offset": {"type": "integer"}, "limit": {"type": "integer"}, "encoding": {"type": "string"}, "show_hidden": {"type": "boolean"}}, "required": ["mode", "path"]}),
        # NATIVE FILESYSTEM TOOLS (11)
        Tool(name="fs_read_file", description="Read file contents", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "head": {"type": "integer"}, "tail": {"type": "integer"}}, "required": ["path"]}),
        Tool(name="fs_read_multiple", description="Read multiple files", inputSchema={"type": "object", "properties": {"paths": {"type": "array", "items": {"type": "string"}}}, "required": ["paths"]}),
        Tool(name="fs_write_file", description="Write file", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "content": {"type": "string"}}, "required": ["path", "content"]}),
        Tool(name="fs_edit_file", description="Edit file", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "edits": {"type": "array"}, "dry_run": {"type": "boolean"}}, "required": ["path", "edits"]}),
        Tool(name="fs_create_directory", description="Create directory", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        Tool(name="fs_list_directory", description="List directory", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        Tool(name="fs_directory_tree", description="Directory tree", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "max_depth": {"type": "integer"}}, "required": ["path"]}),
        Tool(name="fs_move_file", description="Move/rename file", inputSchema={"type": "object", "properties": {"source": {"type": "string"}, "destination": {"type": "string"}}, "required": ["source", "destination"]}),
        Tool(name="fs_search_files", description="Search files", inputSchema={"type": "object", "properties": {"path": {"type": "string"}, "pattern": {"type": "string"}}, "required": ["path", "pattern"]}),
        Tool(name="fs_get_file_info", description="File metadata", inputSchema={"type": "object", "properties": {"path": {"type": "string"}}, "required": ["path"]}),
        Tool(name="fs_allowed_dirs", description="List allowed dirs", inputSchema={"type": "object", "properties": {}}),
'''

decay_line = None
for i, line in enumerate(lines):
    if '"neural_apply_decay"' in line and 'Tool(name=' in line:
        decay_line = i
        break
assert decay_line is not None, "Could not find neural_apply_decay"
bracket_line = None
for i in range(decay_line + 1, min(decay_line + 5, len(lines))):
    if lines[i].strip() == ']':
        bracket_line = i
        break
assert bracket_line is not None, "Could not find closing ]"
td_lines = [l + "\n" for l in TOOL_DEFS.split("\n")]
lines = lines[:bracket_line] + td_lines + lines[bracket_line:]
print(f"P4: Inserted tool definitions before line {bracket_line+1}")

# === PATCH 5: Tool handlers ===
HANDLERS = '''
        # WINDOWS DESKTOP TOOLS - Handlers
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

        elif name == "Wait":
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

        elif name == "Snapshot":
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

        elif name == "Scrape":
            if not WINDOWS_AVAILABLE:
                return [TextContent(type="text", text=json.dumps({"error": "Windows bridge not available"}))]
            ud = arguments.get("use_dom", False)
            if isinstance(ud, str): ud = ud.lower() == "true"
            result = await asyncio.to_thread(wb.scrape, arguments["url"], arguments.get("query"), ud)
            return [TextContent(type="text", text=result)]

        elif name == "MultiSelect":
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

'''

nf_line = None
for i, line in enumerate(lines):
    if 'tool_status = "not_found"' in line:
        nf_line = i
        break
assert nf_line is not None, "Could not find tool_status = not_found"
el_line = None
for i in range(nf_line - 1, max(nf_line - 5, 0), -1):
    if lines[i].strip() == "else:":
        el_line = i
        break
assert el_line is not None, "Could not find else: before not_found"
h_lines = [l + "\n" for l in HANDLERS.split("\n")]
lines = lines[:el_line] + h_lines + lines[el_line:]
print(f"P5: Inserted tool handlers before line {el_line+1}")

# Write result
content = "".join(lines)
OUT.write_text(content, encoding="utf-8")
print(f"\nWrote {len(lines)} lines to {OUT}")

# Syntax check
import py_compile
try:
    py_compile.compile(str(OUT), doraise=True)
    print("SYNTAX CHECK: PASSED")
except py_compile.PyCompileError as e:
    print(f"SYNTAX CHECK: FAILED - {e}")
    print("Restoring from backup...")
    shutil.copy2(BAK, OUT)
    print("Restored. Please report this error.")
    sys.exit(1)

# Update config
if CFG.exists():
    cfg_bak = CFG.with_suffix(f".json.bak_{TS}")
    shutil.copy2(CFG, cfg_bak)
    print(f"\nBacked up config to {cfg_bak.name}")

config = {
    "mcpServers": {
        "REL": {
            "command": str(REL / ".venv" / "Scripts" / "python.exe"),
            "args": [str(REL / "mcp_server.py")],
            "env": {
                "REL_PATH": str(REL),
                "WINDOWS_MCP_SRC": r"C:\Users\Bulkl\AppData\Roaming\Claude\Claude Extensions\ant.dir.cursortouch.windows-mcp\src",
                "FS_ALLOWED_DIRS": "C:\\"
            }
        }
    },
    "preferences": {
        "coworkScheduledTasksEnabled": False,
        "ccdScheduledTasksEnabled": True,
        "sidebarMode": "chat",
        "coworkWebSearchEnabled": True
    }
}
CFG.write_text(json.dumps(config, indent=2), encoding="utf-8")
print(f"Updated config - server renamed to 'REL'")
print("\nDONE! Restart Claude Desktop now.")
