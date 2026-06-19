import subprocess
import sys

# Run pytest and capture output
result = subprocess.run(
    [r'C:\REL\.venv\Scripts\pytest.exe', '-v', '--tb=line', 'tests/'],
    capture_output=True,
    text=True,
    cwd=r'C:\REL'
)

# Write results to file
with open(r'C:\REL\pytest_results.txt', 'w', encoding='utf-8') as f:
    f.write("=== PYTEST OUTPUT ===\n\n")
    f.write(f"Return code: {result.returncode}\n\n")
    f.write("=== STDOUT ===\n")
    f.write(result.stdout)
    f.write("\n\n=== STDERR ===\n")
    f.write(result.stderr)

print(f"Results written to pytest_results.txt (return code: {result.returncode})")
