import re
with open(r'C:\REL_Codex_Variant\mcp_server.py', encoding='utf-8') as f:
    src = f.read()
names = re.findall(r'Tool\(name=["\x27]([^"\']+)["\x27]', src)
windows_tools = [n for n in names if n in [
    'PowerShell','App','Click','Type','Scroll','Move','Shortcut','Wait',
    'Screenshot','Snapshot','Scrape','MultiSelect','MultiEdit','Clipboard',
    'Process','Notification','Registry','WinFileSystem'
]]
all_tool_names = sorted(set(names))
with open(r'C:\REL_Codex_Variant\tool_list.txt', 'w') as f:
    f.write("ALL TOOLS:\n")
    for n in all_tool_names:
        f.write(f"  {n}\n")
    f.write(f"\nWINDOWS TOOLS REGISTERED ({len(windows_tools)}):\n")
    for n in sorted(windows_tools):
        f.write(f"  {n}\n")
    win_expected = ['PowerShell','App','Click','Type','Scroll','Move','Shortcut','Wait',
                    'Screenshot','Snapshot','Scrape','MultiSelect','MultiEdit','Clipboard',
                    'Process','Notification','Registry','WinFileSystem']
    missing = [n for n in win_expected if n not in windows_tools]
    f.write(f"\nMISSING ({len(missing)}):\n")
    for n in missing:
        f.write(f"  {n}\n")
