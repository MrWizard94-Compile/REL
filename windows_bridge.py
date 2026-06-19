"""
Windows Desktop Bridge for REL Codex Variant
=============================================
Native Python implementation — no windows_mcp dependency.

Tools implemented using:
  - pyautogui   : mouse, keyboard, screenshots
  - psutil      : process management
  - winreg      : Windows registry (stdlib)
  - subprocess  : PowerShell, app launch
  - urllib      : web scraping
  - win32clipboard / PowerShell fallback : clipboard

CRITICAL: Includes self-protection to prevent PowerShell commands from
killing the REL server process (which IS a Python process).
"""

import base64
import io
import logging
import os
import re
import subprocess
import sys
import time
import winreg
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

logger = logging.getLogger("REL.windows")

# =============================================================================
# SELF-PROTECTION
# =============================================================================

REL_SERVER_PID = os.getpid()

_PYTHON_KILL_PATTERNS = [
    (
        r'Get-Process\s+(?:-Name\s+)?python(?:[\w.]*)?(?:\s+-ErrorAction\s+\w+)?\s*\|\s*Stop-Process(?:\s+-Force)?',
        'Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {{$_.Id -ne {pid}}} | Stop-Process -Force',
    ),
    (
        r'Stop-Process\s+(?:-Force\s+)?-Name\s+python(?:[\w.]*)?',
        'Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {{$_.Id -ne {pid}}} | Stop-Process -Force',
    ),
    (
        r'Stop-Process\s+-Name\s+python(?:[\w.]*)?\s+-Force',
        'Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {{$_.Id -ne {pid}}} | Stop-Process -Force',
    ),
    (
        r'taskkill\s+(?:/f\s+)?/im\s+python(?:[\w.]*)?\.exe',
        'Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {{$_.Id -ne {pid}}} | Stop-Process -Force',
    ),
    (
        r'taskkill\s+/im\s+python(?:[\w.]*)?\.exe\s+/f',
        'Get-Process -Name python -ErrorAction SilentlyContinue | Where-Object {{$_.Id -ne {pid}}} | Stop-Process -Force',
    ),
]


def protect_command(command: str) -> str:
    """Intercept commands that would kill Python processes indiscriminately."""
    modified = command
    protected = False
    for pattern, replacement_template in _PYTHON_KILL_PATTERNS:
        if re.search(pattern, modified, re.IGNORECASE):
            replacement = replacement_template.format(pid=REL_SERVER_PID)
            modified = re.sub(pattern, replacement, modified, flags=re.IGNORECASE)
            protected = True
    if protected:
        logger.warning(
            "Self-protection: modified command to exclude PID %d.\n  Original: %s\n  Modified: %s",
            REL_SERVER_PID, command[:200], modified[:200],
        )
    return modified


# =============================================================================
# LAZY IMPORTS — pyautogui needs a display; fail gracefully in headless env
# =============================================================================

_pag = None
_pag_error = None


def _get_pyautogui():
    global _pag, _pag_error
    if _pag is not None:
        return _pag
    if _pag_error:
        raise RuntimeError(f"pyautogui unavailable: {_pag_error}")
    try:
        import pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.05
        _pag = pyautogui
        logger.info("pyautogui loaded OK")
        return _pag
    except Exception as e:
        _pag_error = str(e)
        raise RuntimeError(f"pyautogui unavailable: {e}")


_psutil = None
_psutil_error = None


def _get_psutil():
    global _psutil, _psutil_error
    if _psutil is not None:
        return _psutil
    if _psutil_error:
        raise RuntimeError(f"psutil unavailable: {_psutil_error}")
    try:
        import psutil
        _psutil = psutil
        return _psutil
    except Exception as e:
        _psutil_error = str(e)
        raise RuntimeError(f"psutil unavailable: {e}")


# =============================================================================
# TOOL IMPLEMENTATIONS
# =============================================================================


def powershell(command: str, timeout: int = 30) -> str:
    """Execute PowerShell command with self-protection."""
    safe_command = protect_command(command)
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", safe_command],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout.strip()
        if not output and result.stderr.strip():
            output = result.stderr.strip()
        return f"Response: {output}\nStatus Code: {result.returncode}"
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout}s\nStatus Code: 1"
    except Exception as e:
        return f"Error executing command: {e}\nStatus Code: 1"


def app_tool(
    mode: str = "launch",
    name: Optional[str] = None,
    window_loc: Optional[List[int]] = None,
    window_size: Optional[List[int]] = None,
) -> str:
    """Launch, resize, or switch applications."""
    if mode == "launch":
        if not name:
            return "Error: name required for launch mode."
        try:
            subprocess.Popen(name, shell=True)
            return f"Launched: {name}"
        except Exception as e:
            return f"Error launching {name}: {e}"

    elif mode == "switch":
        if not name:
            return "Error: name required for switch mode."
        # Use PowerShell to bring window to foreground
        ps = (
            f'$w = Get-Process | Where-Object {{$_.MainWindowTitle -like "*{name}*"}} | '
            f'Select-Object -First 1; '
            f'if ($w) {{ '
            f'Add-Type -AssemblyName Microsoft.VisualBasic; '
            f'[Microsoft.VisualBasic.Interaction]::AppActivate($w.Id); '
            f'"Switched to $($w.MainWindowTitle)" }} '
            f'else {{ "Window not found: {name}" }}'
        )
        return powershell(ps, timeout=10)

    elif mode == "resize":
        if not name:
            return "Error: name required for resize mode."
        if not window_size or len(window_size) < 2:
            return "Error: window_size [w, h] required for resize mode."
        w, h = window_size[0], window_size[1]
        x = window_loc[0] if window_loc and len(window_loc) >= 2 else 0
        y = window_loc[1] if window_loc and len(window_loc) >= 2 else 0
        ps = (
            f'Add-Type @"\nusing System; using System.Runtime.InteropServices;\n'
            f'public class Win {{\n'
            f'  [DllImport("user32.dll")] public static extern bool MoveWindow(IntPtr h, int x, int y, int w, int h, bool r);\n'
            f'  [DllImport("user32.dll")] public static extern IntPtr FindWindow(string c, string t);\n'
            f'}}\n"@ -Language CSharp;\n'
            f'$p = Get-Process | Where-Object {{$_.MainWindowTitle -like "*{name}*"}} | Select-Object -First 1;\n'
            f'if ($p) {{ [Win]::MoveWindow($p.MainWindowHandle, {x}, {y}, {w}, {h}, $true); "Resized" }}\n'
            f'else {{ "Window not found: {name}" }}'
        )
        return powershell(ps, timeout=10)

    else:
        return f'Error: Unknown mode "{mode}". Use: launch, switch, resize.'


def click(
    loc: Optional[List[int]] = None,
    label: Optional[int] = None,
    button: str = "left",
    clicks: int = 1,
) -> str:
    """Perform mouse clicks at coordinates."""
    if loc is None:
        return "Error: loc [x, y] is required."
    if len(loc) != 2:
        return "Error: loc must be [x, y]."
    pag = _get_pyautogui()
    x, y = loc[0], loc[1]
    btn = button if button in ("left", "right", "middle") else "left"
    if clicks == 0:
        pag.moveTo(x, y, duration=0.1)
        return f"Hover at ({x}, {y})."
    pag.click(x, y, clicks=clicks, button=btn, interval=0.1)
    label_str = {1: "Single", 2: "Double"}.get(clicks, str(clicks))
    return f"{label_str} {btn} click at ({x}, {y})."


def type_text(
    text: str,
    loc: Optional[List[int]] = None,
    label: Optional[int] = None,
    clear: bool = False,
    caret_position: str = "idle",
    press_enter: bool = False,
) -> str:
    """Type text, optionally clicking a location first."""
    pag = _get_pyautogui()
    if loc and len(loc) == 2:
        pag.click(loc[0], loc[1])
        time.sleep(0.1)
    if clear:
        pag.hotkey("ctrl", "a")
        time.sleep(0.05)
    pag.typewrite(text, interval=0.03)
    if press_enter:
        pag.press("enter")
    loc_str = f" at ({loc[0]}, {loc[1]})" if loc else ""
    return f"Typed text{loc_str}: {text[:80]}{'...' if len(text) > 80 else ''}"


def scroll(
    loc: Optional[List[int]] = None,
    label: Optional[int] = None,
    scroll_type: str = "vertical",
    direction: str = "down",
    wheel_times: int = 1,
) -> str:
    """Scroll at a screen location."""
    pag = _get_pyautogui()
    # pyautogui scroll: positive = up, negative = down
    clicks = wheel_times if direction == "up" else -wheel_times
    if loc and len(loc) == 2:
        pag.scroll(clicks, x=loc[0], y=loc[1])
        return f"Scrolled {direction} {wheel_times}x at ({loc[0]}, {loc[1]})."
    else:
        pag.scroll(clicks)
        return f"Scrolled {direction} {wheel_times}x at current position."


def move(
    loc: Optional[List[int]] = None,
    label: Optional[int] = None,
    drag: bool = False,
) -> str:
    """Move mouse or drag to coordinates."""
    if not loc or len(loc) != 2:
        return "Error: loc [x, y] is required."
    pag = _get_pyautogui()
    x, y = loc[0], loc[1]
    if drag:
        pag.dragTo(x, y, duration=0.3, button="left")
        return f"Dragged to ({x}, {y})."
    else:
        pag.moveTo(x, y, duration=0.1)
        return f"Moved mouse to ({x}, {y})."


def shortcut(shortcut_keys: str) -> str:
    """Execute keyboard shortcut. Use '+' to separate keys e.g. 'ctrl+c'."""
    pag = _get_pyautogui()
    keys = [k.strip().lower() for k in shortcut_keys.replace("+", " ").split()]
    if len(keys) == 1:
        pag.press(keys[0])
    else:
        pag.hotkey(*keys)
    return f"Pressed: {shortcut_keys}"


def wait(duration: int) -> str:
    """Pause for N seconds."""
    time.sleep(duration)
    return f"Waited {duration} seconds."


def screenshot(
    use_annotation: bool = False,
    width_reference_line: Optional[int] = None,
    height_reference_line: Optional[int] = None,
    display: Optional[List[int]] = None,
) -> Any:
    """Capture screenshot and return as base64-encoded image."""
    try:
        pag = _get_pyautogui()
        img = pag.screenshot()

        # Encode as base64 PNG
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode("utf-8")

        w, h = img.size
        return {
            "type": "image",
            "format": "png",
            "width": w,
            "height": h,
            "data": b64,
            "size_bytes": len(buf.getvalue()),
        }
    except Exception as e:
        return f"Error capturing screenshot: {e}"


def snapshot_tool(
    use_vision: bool = False,
    use_dom: bool = False,
    use_annotation: bool = True,
    use_ui_tree: bool = True,
    width_reference_line: Optional[int] = None,
    height_reference_line: Optional[int] = None,
    display: Optional[List[int]] = None,
) -> Any:
    """Capture screenshot. Full UI tree requires additional setup."""
    # For now, return screenshot + basic window list via PowerShell
    try:
        img_result = screenshot(use_annotation=use_annotation)

        # Get window list via PowerShell for lightweight UI context
        ps_result = powershell(
            'Get-Process | Where-Object {$_.MainWindowTitle -ne ""} | '
            'Select-Object Id, ProcessName, MainWindowTitle | '
            'Format-Table -AutoSize | Out-String',
            timeout=8,
        )

        if isinstance(img_result, dict):
            img_result["windows"] = ps_result
            img_result["note"] = "Full UI tree not available — using screenshot + window list."
        return img_result
    except Exception as e:
        return f"Error capturing desktop state: {e}"


def scrape(url: str, query: Optional[str] = None, use_dom: bool = False) -> str:
    """Fetch web page content using urllib."""
    try:
        import urllib.request
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            raw = resp.read()
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                text = raw.decode("latin-1", errors="replace")

        # Strip HTML tags for readable output
        clean = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
        clean = re.sub(r"<script[^>]*>.*?</script>", " ", clean, flags=re.DOTALL | re.IGNORECASE)
        clean = re.sub(r"<[^>]+>", " ", clean)
        clean = re.sub(r"\s{3,}", "\n\n", clean).strip()

        # Limit output
        if len(clean) > 8000:
            clean = clean[:8000] + "\n\n[...content truncated...]"

        return f"URL: {url}\n\n{clean}"
    except Exception as e:
        return f"Error scraping {url}: {e}"


def multi_select(
    locs: Optional[List[List[int]]] = None,
    labels: Optional[List[int]] = None,
    press_ctrl: bool = True,
) -> str:
    """Click multiple locations while holding Ctrl."""
    if not locs:
        return "Error: locs list of [x, y] coordinates required."
    pag = _get_pyautogui()
    if press_ctrl:
        pag.keyDown("ctrl")
    try:
        for loc in locs:
            if len(loc) == 2:
                pag.click(loc[0], loc[1])
                time.sleep(0.05)
    finally:
        if press_ctrl:
            pag.keyUp("ctrl")
    pts = ", ".join(f"({l[0]},{l[1]})" for l in locs if len(l) == 2)
    return f"Multi-selected {len(locs)} elements at: {pts}"


def multi_edit(
    locs: Optional[List[List]] = None,
    labels: Optional[List[List]] = None,
) -> str:
    """Click each [x, y, text] location and type the associated text."""
    if not locs:
        return "Error: locs list of [x, y, text] required."
    pag = _get_pyautogui()
    results = []
    for item in locs:
        if len(item) < 3:
            results.append(f"Skipped invalid item: {item}")
            continue
        x, y, text = item[0], item[1], str(item[2])
        pag.click(x, y)
        time.sleep(0.08)
        pag.hotkey("ctrl", "a")
        time.sleep(0.04)
        pag.typewrite(text, interval=0.02)
        results.append(f"({x},{y}): typed '{text[:40]}'")
    return "Multi-edit results:\n" + "\n".join(results)


def clipboard(mode: str, text: Optional[str] = None) -> str:
    """Clipboard get/set via win32clipboard with PowerShell fallback."""
    try:
        import win32clipboard
        if mode == "get":
            win32clipboard.OpenClipboard()
            try:
                if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_UNICODETEXT):
                    data = win32clipboard.GetClipboardData(win32clipboard.CF_UNICODETEXT)
                    return f"Clipboard content:\n{data}"
                return "Clipboard is empty or contains non-text data."
            finally:
                win32clipboard.CloseClipboard()
        elif mode == "set":
            if text is None:
                return "Error: text required for set mode."
            win32clipboard.OpenClipboard()
            try:
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(text, win32clipboard.CF_UNICODETEXT)
                return f"Clipboard set to: {text[:100]}{'...' if len(text) > 100 else ''}"
            finally:
                win32clipboard.CloseClipboard()
        else:
            return 'Error: mode must be "get" or "set".'
    except ImportError:
        # PowerShell fallback
        if mode == "get":
            return powershell("Get-Clipboard", timeout=5)
        elif mode == "set":
            safe = (text or "").replace('"', '`"')
            return powershell(f'Set-Clipboard -Value "{safe}"', timeout=5)
        return "Error: clipboard operation failed."
    except Exception as e:
        return f"Error managing clipboard: {e}"


def process_tool(
    mode: str,
    name: Optional[str] = None,
    pid: Optional[int] = None,
    sort_by: str = "memory",
    limit: int = 20,
    force: bool = False,
) -> str:
    """List or kill processes with self-protection."""
    ps = _get_psutil()

    if mode == "list":
        procs = []
        for p in ps.process_iter(["pid", "name", "memory_info", "cpu_percent", "status"]):
            try:
                info = p.info
                mem_mb = round(info["memory_info"].rss / 1024 / 1024, 1) if info["memory_info"] else 0
                if name and name.lower() not in (info["name"] or "").lower():
                    continue
                procs.append({
                    "pid": info["pid"],
                    "name": info["name"],
                    "memory_mb": mem_mb,
                    "cpu": info["cpu_percent"],
                    "status": info["status"],
                })
            except (ps.NoSuchProcess, ps.AccessDenied):
                pass

        if sort_by == "memory":
            procs.sort(key=lambda x: x["memory_mb"], reverse=True)
        elif sort_by == "cpu":
            procs.sort(key=lambda x: x["cpu"], reverse=True)
        else:
            procs.sort(key=lambda x: x["name"].lower())

        procs = procs[:limit]
        lines = [f"{'PID':>7}  {'Name':<25}  {'Mem MB':>8}  {'CPU%':>6}  Status"]
        lines.append("-" * 60)
        for p in procs:
            lines.append(f"{p['pid']:>7}  {p['name']:<25}  {p['memory_mb']:>8.1f}  {p['cpu']:>6.1f}  {p['status']}")
        return "\n".join(lines)

    elif mode == "kill":
        # SELF-PROTECTION
        if pid is not None and pid == REL_SERVER_PID:
            return f"Error: Cannot kill PID {pid} — this is the REL server process."

        killed = []
        errors = []

        if pid is not None:
            try:
                p = ps.Process(pid)
                if p.pid == REL_SERVER_PID:
                    return f"Error: Cannot kill PID {pid} — this is the REL server process."
                p.kill() if force else p.terminate()
                killed.append(f"PID {pid} ({p.name()})")
            except ps.NoSuchProcess:
                errors.append(f"PID {pid} not found.")
            except ps.AccessDenied:
                errors.append(f"Access denied for PID {pid}.")

        elif name:
            for p in ps.process_iter(["pid", "name"]):
                try:
                    if name.lower() in (p.info["name"] or "").lower():
                        if p.pid == REL_SERVER_PID:
                            errors.append(f"Skipped REL server (PID {p.pid}).")
                            continue
                        p.kill() if force else p.terminate()
                        killed.append(f"PID {p.pid} ({p.info['name']})")
                except (ps.NoSuchProcess, ps.AccessDenied):
                    pass

        result = []
        if killed:
            result.append("Killed: " + ", ".join(killed))
        if errors:
            result.append("Errors: " + "; ".join(errors))
        return "\n".join(result) if result else "No matching processes found."

    else:
        return 'Error: mode must be "list" or "kill".'


def notification(title: str, message: str) -> str:
    """Send Windows toast notification via PowerShell."""
    safe_title = title.replace("'", "''")
    safe_message = message.replace("'", "''")
    ps_cmd = (
        f"Add-Type -AssemblyName System.Windows.Forms; "
        f"$n = New-Object System.Windows.Forms.NotifyIcon; "
        f"$n.Icon = [System.Drawing.SystemIcons]::Information; "
        f"$n.Visible = $true; "
        f"$n.ShowBalloonTip(3000, '{safe_title}', '{safe_message}', "
        f"[System.Windows.Forms.ToolTipIcon]::Info); "
        f"Start-Sleep 4; $n.Dispose()"
    )
    return powershell(ps_cmd, timeout=8)


def registry(
    mode: str,
    path: str,
    name: Optional[str] = None,
    value: Optional[str] = None,
    reg_type: str = "String",
) -> str:
    """Windows Registry operations using stdlib winreg."""
    # Map hive prefix to winreg constant
    _HIVES = {
        "HKLM": winreg.HKEY_LOCAL_MACHINE,
        "HKCU": winreg.HKEY_CURRENT_USER,
        "HKCR": winreg.HKEY_CLASSES_ROOT,
        "HKU":  winreg.HKEY_USERS,
        "HKCC": winreg.HKEY_CURRENT_CONFIG,
        "HKEY_LOCAL_MACHINE":   winreg.HKEY_LOCAL_MACHINE,
        "HKEY_CURRENT_USER":    winreg.HKEY_CURRENT_USER,
        "HKEY_CLASSES_ROOT":    winreg.HKEY_CLASSES_ROOT,
        "HKEY_USERS":           winreg.HKEY_USERS,
        "HKEY_CURRENT_CONFIG":  winreg.HKEY_CURRENT_CONFIG,
    }
    _TYPES = {
        "String":   winreg.REG_SZ,
        "REG_SZ":   winreg.REG_SZ,
        "DWORD":    winreg.REG_DWORD,
        "REG_DWORD": winreg.REG_DWORD,
        "QWORD":    winreg.REG_QWORD,
        "REG_QWORD": winreg.REG_QWORD,
        "Binary":   winreg.REG_BINARY,
        "REG_BINARY": winreg.REG_BINARY,
        "ExpandSZ": winreg.REG_EXPAND_SZ,
        "MultiSZ":  winreg.REG_MULTI_SZ,
    }

    # Split hive from subkey
    parts = path.replace("/", "\\").split("\\", 1)
    hive_str = parts[0].upper()
    subkey = parts[1] if len(parts) > 1 else ""

    hive = _HIVES.get(hive_str)
    if hive is None:
        return f"Error: Unknown hive '{hive_str}'. Use HKLM, HKCU, HKCR, HKU, or HKCC."

    try:
        if mode == "get":
            if not name:
                return "Error: name required for get mode."
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ) as key:
                val, vtype = winreg.QueryValueEx(key, name)
            return f"{path}\\{name} = {val}  (type: {vtype})"

        elif mode == "set":
            if not name:
                return "Error: name required for set mode."
            if value is None:
                return "Error: value required for set mode."
            rtype = _TYPES.get(reg_type, winreg.REG_SZ)
            # Convert value type as needed
            typed_value: Any = value
            if rtype in (winreg.REG_DWORD, winreg.REG_QWORD):
                typed_value = int(value)
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, name, 0, rtype, typed_value)
            return f"Set {path}\\{name} = {value}"

        elif mode == "delete":
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_SET_VALUE) as key:
                if name:
                    winreg.DeleteValue(key, name)
                    return f"Deleted value {path}\\{name}"
                else:
                    winreg.DeleteKey(key, "")
                    return f"Deleted key {path}"

        elif mode == "list":
            results = []
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ) as key:
                # List subkeys
                i = 0
                while True:
                    try:
                        results.append("[KEY] " + winreg.EnumKey(key, i))
                        i += 1
                    except OSError:
                        break
                # List values
                i = 0
                while True:
                    try:
                        vname, vdata, vtype = winreg.EnumValue(key, i)
                        results.append(f"[VAL] {vname or '(Default)'} = {str(vdata)[:80]}")
                        i += 1
                    except OSError:
                        break
            return f"Contents of {path}:\n" + "\n".join(results) if results else f"{path} is empty."

        else:
            return 'Error: mode must be "get", "set", "delete", or "list".'

    except FileNotFoundError:
        return f"Error: Registry path not found: {path}"
    except PermissionError:
        return f"Error: Access denied for {path}. Try running as administrator."
    except Exception as e:
        return f"Error accessing registry: {e}"


def win_filesystem(
    mode: str,
    path: str,
    destination: Optional[str] = None,
    content: Optional[str] = None,
    pattern: Optional[str] = None,
    recursive: bool = False,
    append: bool = False,
    overwrite: bool = False,
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    encoding: str = "utf-8",
    show_hidden: bool = False,
) -> str:
    """Windows file system operations using native Python."""
    import glob
    import shutil
    import stat

    p = Path(path)

    try:
        if mode == "read":
            if not p.exists():
                return f"Error: File not found: {path}"
            text = p.read_text(encoding=encoding, errors="replace")
            lines = text.splitlines()
            if offset:
                lines = lines[offset:]
            if limit:
                lines = lines[:limit]
            return "\n".join(lines)

        elif mode == "write":
            if content is None:
                return "Error: content required for write mode."
            p.parent.mkdir(parents=True, exist_ok=True)
            if append:
                with p.open("a", encoding=encoding) as f:
                    f.write(content)
            else:
                p.write_text(content, encoding=encoding)
            return f"Written {len(content)} chars to {path}"

        elif mode == "copy":
            if not destination:
                return "Error: destination required for copy mode."
            dest = Path(destination)
            if dest.exists() and not overwrite:
                return f"Error: Destination exists. Use overwrite=true to replace."
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(str(p), str(dest))
            return f"Copied {path} → {destination}"

        elif mode == "move":
            if not destination:
                return "Error: destination required for move mode."
            dest = Path(destination)
            if dest.exists() and not overwrite:
                return f"Error: Destination exists. Use overwrite=true to replace."
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(p), str(dest))
            return f"Moved {path} → {destination}"

        elif mode == "delete":
            if p.is_dir():
                if recursive:
                    shutil.rmtree(str(p))
                    return f"Deleted directory: {path}"
                else:
                    p.rmdir()
                    return f"Deleted empty directory: {path}"
            else:
                p.unlink()
                return f"Deleted: {path}"

        elif mode == "list":
            if not p.exists():
                return f"Error: Path not found: {path}"
            entries = []
            for item in sorted(p.iterdir()):
                if not show_hidden and item.name.startswith("."):
                    continue
                tag = "[DIR]" if item.is_dir() else "[FILE]"
                entries.append(f"{tag} {item.name}")
            return "\n".join(entries) if entries else f"{path} is empty."

        elif mode == "search":
            if not pattern:
                return "Error: pattern required for search mode."
            if recursive:
                matches = list(p.rglob(pattern))
            else:
                matches = list(p.glob(pattern))
            return "\n".join(str(m) for m in matches) if matches else "No matches found."

        elif mode == "info":
            if not p.exists():
                return f"Error: Path not found: {path}"
            s = p.stat()
            return (
                f"Path: {p}\n"
                f"Type: {'directory' if p.is_dir() else 'file'}\n"
                f"Size: {s.st_size} bytes\n"
                f"Modified: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(s.st_mtime))}\n"
                f"Created: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(s.st_ctime))}"
            )

        else:
            return f'Error: Unknown mode "{mode}". Use: read, write, copy, move, delete, list, search, info.'

    except Exception as e:
        return f"Error in WinFileSystem ({mode}): {e}"


# =============================================================================
# CLEANUP
# =============================================================================

def shutdown():
    """Clean shutdown."""
    logger.info("Windows bridge shut down (PID=%d)", REL_SERVER_PID)
