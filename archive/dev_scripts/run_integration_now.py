"""Run integration tests and save output"""
import subprocess
import sys
from pathlib import Path

rel_path = Path(r"C:\REL")
python_exe = rel_path / ".venv" / "Scripts" / "python.exe"

print("Running integration tests...")
print("=" * 70)

# Run just the first test file
result = subprocess.run(
    [
        str(python_exe),
        "-m", "pytest",
        "tests/integration/test_mcp_server.py",
        "-v",
        "--tb=short",
        "-x"  # Stop on first failure
    ],
    cwd=str(rel_path),
    capture_output=True,
    text=True,
    timeout=120
)

# Print to console
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# Save to file
output_file = rel_path / "integration_test_results.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("=" * 70 + "\n")
    f.write("INTEGRATION TEST RESULTS - test_mcp_server.py\n")
    f.write("=" * 70 + "\n\n")
    f.write(result.stdout)
    if result.stderr:
        f.write("\n\nSTDERR:\n")
        f.write(result.stderr)
    f.write(f"\n\nReturn code: {result.returncode}\n")

print(f"\nOutput saved to: {output_file}")
print(f"Return code: {result.returncode}")

sys.exit(result.returncode)
