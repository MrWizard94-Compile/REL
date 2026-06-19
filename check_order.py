import re
with open(r'C:\REL_Codex_Variant\mcp_server.py', encoding='utf-8') as f:
    src = f.read()
names = re.findall(r'Tool\(name="([^"]+)"', src)
with open(r'C:\REL_Codex_Variant\tool_order_check.txt', 'w') as f:
    f.write(f"Total: {len(names)}\n")
    f.write("Order:\n")
    for i, n in enumerate(names, 1):
        f.write(f"  {i:3}. {n}\n")
