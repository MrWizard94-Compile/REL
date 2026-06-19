#!/usr/bin/env python3
"""Quick mypy test for phase 1"""
import subprocess

result = subprocess.run(
    ['C:/REL/.venv/Scripts/mypy.exe', 'mcp_server_typed_phase1.py'],
    cwd='C:/REL',
    capture_output=True,
    text=True
)

print("STDOUT:")
print(result.stdout)
print("\nSTDERR:")
print(result.stderr)
print(f"\nReturn code: {result.returncode}")

# Save to file
with open('C:/REL/mypy_output.txt', 'w') as f:
    f.write(f"Return code: {result.returncode}\n\n")
    f.write("STDOUT:\n")
    f.write(result.stdout)
    f.write("\n\nSTDERR:\n")
    f.write(result.stderr)

print("\nSaved to mypy_output.txt")
