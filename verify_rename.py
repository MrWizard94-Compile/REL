import re, py_compile

# Syntax check
try:
    py_compile.compile(r'C:\REL_Codex_Variant\mcp_server.py', doraise=True)
    print("SYNTAX: OK")
except py_compile.PyCompileError as e:
    print(f"SYNTAX ERROR: {e}")

# Verify new names present, old names absent
with open(r'C:\REL_Codex_Variant\mcp_server.py', encoding='utf-8') as f:
    src = f.read()

new_names = ["TypeText", "DeskSnapshot", "PauseSec", "WebScrape", "AppLaunch", "MultiClick"]
old_names = ['"Type"', '"Snapshot"', '"Wait"', '"Scrape"', '"App"', '"MultiSelect"']

print("\nNew names in file:")
for n in new_names:
    count = src.count(f'"{n}"')
    print(f"  {n}: {count} occurrences (Tool reg + elif dispatch = expect 2)")

print("\nOld names still in file (should be 0):")
for n in old_names:
    # exclude create_snapshot and similar
    tool_reg = f'Tool(name={n},'
    elif_ref = f'elif name == {n}:'
    reg_count = src.count(tool_reg)
    elif_count = src.count(elif_ref)
    print(f"  {n}: Tool()={reg_count} elif={elif_count}")

# Schema size check
names = re.findall(r'Tool\(name="([^"]+)"', src)
entries_raw = []
lines = src.split('\n')
current = []
in_return = False
for line in lines:
    if 'return [' in line and 'list_tools' not in line:
        in_return = True
        continue
    if in_return:
        s = line.strip()
        if s.startswith('Tool(name=') and current:
            entries_raw.append('\n'.join(current))
            current = [line]
        elif s.startswith('#') or s == '':
            pass
        elif s.startswith('Tool(name='):
            current = [line]
        elif current:
            current.append(line)
        elif s.startswith(']') and not s.startswith(']}'):
            break
if current:
    entries_raw.append('\n'.join(current))

size_map = {}
for e in entries_raw:
    m = re.search(r'Tool\(name="([^"]+)"', e)
    if m:
        size_map[m.group(1)] = len(e.encode('utf-8'))

print(f"\nTotal tools: {len(size_map)}")
target = ["TypeText","DeskSnapshot","PauseSec","WebScrape","AppLaunch","MultiClick"]
print("New tool schema sizes:")
for n in target:
    print(f"  {n}: {size_map.get(n, 'NOT FOUND')} bytes")
