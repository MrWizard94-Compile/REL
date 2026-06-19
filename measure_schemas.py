import re, json

with open(r'C:\REL_Codex_Variant\mcp_server.py', encoding='utf-8') as f:
    src = f.read()

# Find the list_tools return block
start = src.index('    return [\n') + len('    return [\n')
end = src.index('\n    ]\n\n# =====', start)
block = src[start:end]

# Parse Tool entries
entries, current = [], []
for line in block.split('\n'):
    s = line.strip()
    if s.startswith('Tool(name=') and current:
        entries.append('\n'.join(current))
        current = [line]
    elif s.startswith('#') or s == '':
        pass
    elif s.startswith('Tool(name='):
        current = [line]
    elif current:
        current.append(line)
if current:
    entries.append('\n'.join(current))

# Measure each entry size
sizes = []
for entry in entries:
    m = re.search(r'Tool\(name="([^"]+)"', entry)
    if m:
        sizes.append((m.group(1), len(entry.encode('utf-8'))))

sizes.sort(key=lambda x: x[1], reverse=True)

# Write report
with open(r'C:\REL_Codex_Variant\schema_sizes.txt', 'w') as f:
    f.write("Tool schema sizes (bytes, largest first):\n\n")
    cumulative = 0
    # Also write in registration order
    name_order = [re.search(r'Tool\(name="([^"]+)"', e).group(1) for e in entries if re.search(r'Tool\(name="([^"]+)"', e)]
    
    f.write("--- BY REGISTRATION ORDER (with cumulative size) ---\n")
    cum = 0
    size_dict = dict(sizes)
    for i, name in enumerate(name_order, 1):
        sz = size_dict.get(name, 0)
        cum += sz
        f.write(f"  {i:3}. {name:<35} {sz:>6} bytes  (cumulative: {cum:>8})\n")
    
    f.write(f"\nTotal schema bytes: {cum}\n")
    f.write("\n--- BY SIZE (largest schemas) ---\n")
    for name, sz in sizes[:20]:
        f.write(f"  {name:<35} {sz:>6} bytes\n")
