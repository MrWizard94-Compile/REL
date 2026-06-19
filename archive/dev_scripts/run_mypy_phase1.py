import subprocess
import sys

# Run mypy on phase 1
result = subprocess.run(
    [r'C:\REL\.venv\Scripts\mypy.exe', 
     'mcp_server_typed_phase1.py',
     '--pretty',
     '--show-error-codes'],
    capture_output=True,
    text=True,
    cwd=r'C:\REL'
)

# Write results
with open(r'C:\REL\mypy_phase1_results.txt', 'w', encoding='utf-8') as f:
    f.write("=== MYPY PHASE 1 RESULTS ===\n\n")
    f.write(f"Return code: {result.returncode}\n\n")
    f.write("=== STDOUT ===\n")
    f.write(result.stdout)
    f.write("\n\n=== STDERR ===\n")
    f.write(result.stderr)

# Print summary
print(f"Mypy completed with return code: {result.returncode}")
if result.returncode == 0:
    print("✅ No type errors found!")
else:
    print("⚠️  Type errors found - check mypy_phase1_results.txt")
    
# Print first 30 lines of output
lines = result.stdout.split('\n')
for line in lines[:30]:
    print(line)
