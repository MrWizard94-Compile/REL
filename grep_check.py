import re

with open(r'C:\REL_Codex_Variant\mcp_server.py', encoding='utf-8') as f:
    src = f.read()

targets = ["TypeText","DeskSnapshot","PauseSec","WebScrape","AppLaunch","MultiClick"]
with open(r'C:\REL_Codex_Variant\grep_check.txt', 'w') as f:
    for name in targets:
        # Find the actual lines containing this name
        lines = [(i+1, l.strip()) for i, l in enumerate(src.splitlines()) if name in l]
        f.write(f"\n{name} ({len(lines)} occurrences):\n")
        for lineno, line in lines:
            f.write(f"  Line {lineno}: {line[:120]}\n")
