"""
Simple test runner to execute integration tests and capture results
"""
import subprocess
import sys
from pathlib import Path

# Change to REL directory
rel_path = Path(r"C:\REL")
python_exe = rel_path / ".venv" / "Scripts" / "python.exe"

print("=" * 80)
print("RUNNING INTEGRATION TESTS")
print("=" * 80)
print(f"REL Path: {rel_path}")
print(f"Python: {python_exe}")
print()

# Run pytest
result = subprocess.run(
    [
        str(python_exe),
        "-m", "pytest",
        "tests/integration/",
        "-v",
        "--tb=short",
        "-x"  # Stop on first failure
    ],
    cwd=str(rel_path),
    capture_output=True,
    text=True
)

print(result.stdout)
if result.stderr:
    print("STDERR:")
    print(result.stderr)

print()
print(f"Return code: {result.returncode}")

# Save to file
output_file = rel_path / "integration_test_run.txt"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(result.stdout)
    if result.stderr:
        f.write("\n\nSTDERR:\n")
        f.write(result.stderr)
    f.write(f"\n\nReturn code: {result.returncode}\n")

print(f"\nFull output saved to: {output_file}")

sys.exit(result.returncode)
