import re
with open(r'C:\REL_Codex_Variant\mcp_server.py', encoding='utf-8') as f:
    src = f.read()
names = re.findall(r'Tool\(name=["\x27]([^"\']+)["\x27]', src)
unique = sorted(set(names))
with open(r'C:\REL_Codex_Variant\all_tools.txt', 'w') as f:
    f.write(f"Total unique tools registered: {len(unique)}\n\n")
    for i, n in enumerate(unique, 1):
        f.write(f"{i:3}. {n}\n")
