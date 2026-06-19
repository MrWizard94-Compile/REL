#!/usr/bin/env python3
"""
Build complete mcp_server_typed.py from phases
"""
from pathlib import Path

# Read Phase 1 (infrastructure)
phase1_path = Path("C:/REL/mcp_server_typed_phase1.py")
phase1_content = phase1_path.read_text(encoding='utf-8')

# Read Phase 2 (cognitive modules) 
phase2_path = Path("C:/REL/mcp_server_typed_phase2.py")
phase2_content = phase2_path.read_text(encoding='utf-8')

# Read original for reference
original_path = Path("C:/REL/mcp_server.py")
original_content = original_path.read_text(encoding='utf-8')

# Build complete typed version
# Phase 1 has everything up to cognitive modules
# Remove the trailing comment from Phase 1
phase1_lines = phase1_content.split('\n')
# Find where to cut Phase 1 (before the trailing notes)
cutoff = None
for i, line in enumerate(phase1_lines):
    if "INFRASTRUCTURE COMPLETE" in line:
        cutoff = i + 3  # Include the separator and comment
        break

if cutoff:
    phase1_clean = '\n'.join(phase1_lines[:cutoff])
else:
    phase1_clean = phase1_content

# Phase 2 cognitive modules (skip imports and docstring)
phase2_lines = phase2_content.split('\n')
phase2_start = None
for i, line in enumerate(phase2_lines):
    if "COGNITIVE MODULE 1" in line:
        phase2_start = i - 3  # Include the separator
        break

if phase2_start:
    phase2_clean = '\n'.join(phase2_lines[phase2_start:])
else:
    phase2_clean = ""

# Now we need to add Phase 3 - tool definitions and handlers
# Find where tools start in original
original_lines = original_content.split('\n')
tool_start = None
for i, line in enumerate(original_lines):
    if "@app.list_tools()" in line or "TOOL DEFINITIONS" in line:
        tool_start = i - 3
        break

if tool_start:
    phase3_content = '\n'.join(original_lines[tool_start:])
else:
    phase3_content = ""

# Now add type hints to Phase 3
# The tool definitions and handlers need typing

# Combine everything
complete_content = f"""{phase1_clean}

{phase2_clean}

{phase3_content}
"""

# Write complete typed version
output_path = Path("C:/REL/mcp_server_typed_INCOMPLETE.py")
output_path.write_text(complete_content, encoding='utf-8')

print(f"✅ Created incomplete version: {len(complete_content.split(chr(10)))} lines")
print(f"Next step: Add type hints to tool handlers section")
print(f"Original: {len(original_lines)} lines")
