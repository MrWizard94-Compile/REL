import subprocess
import sys

result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/integration/test_mcp_server.py", "-v", "--tb=short"],
    capture_output=True,
    text=True,
    cwd=r"C:\REL"
)

with open(r"C:\REL\integration_output.txt", "w") as f:
    f.write("=== STDOUT ===\n")
    f.write(result.stdout)
    f.write("\n\n=== STDERR ===\n")
    f.write(result.stderr)
    f.write(f"\n\n=== RETURN CODE: {result.returncode} ===\n")

print("Output written to integration_output.txt")
