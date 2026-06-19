import re, py_compile, sys

try:
    py_compile.compile(r'C:\REL_Codex_Variant\mcp_server.py', doraise=True)
    result = "SYNTAX: OK\n"
except py_compile.PyCompileError as e:
    result = f"SYNTAX ERROR: {e}\n"

with open(r'C:\REL_Codex_Variant\mcp_server.py', encoding='utf-8') as f:
    src = f.read()

new_names = ["TypeText","DeskSnapshot","PauseSec","WebScrape","AppLaunch","MultiClick"]
old_bad = ['"Type"','Tool(name="Snapshot"','Tool(name="Wait"','Tool(name="Scrape"','Tool(name="App"','Tool(name="MultiSelect"']

result += "\nNew names (expect 2 each = Tool reg + elif):\n"
for n in new_names:
    c = src.count(f'"{n}"')
    result += f"  {n}: {c}\n"

result += "\nOld Tool() registrations still present (expect 0):\n"
for n in old_bad:
    result += f"  {n}: {src.count(n)}\n"

with open(r'C:\REL_Codex_Variant\verify_out.txt', 'w') as f:
    f.write(result)
