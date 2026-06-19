"""Run all tests and generate coverage report"""
import subprocess
import sys

print("Running all tests with coverage...\n")

result = subprocess.run(
    [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--cov=.",
        "--cov-report=term-missing",
        "--cov-report=json",
        "--tb=short"
    ],
    capture_output=True,
    text=True,
    cwd=r"C:\REL"
)

# Write to file
with open(r"C:\REL\all_tests_output.txt", "w", encoding="utf-8") as f:
    f.write("=== PYTEST OUTPUT ===\n\n")
    f.write(f"Return code: {result.returncode}\n\n")
    f.write("=== STDOUT ===\n")
    f.write(result.stdout)
    f.write("\n\n=== STDERR ===\n")
    f.write(result.stderr)

print("✅ Tests complete!")
print(f"Return code: {result.returncode}")
print(f"\nOutput written to: all_tests_output.txt")

# Print summary
lines = result.stdout.split('\n')
for line in lines:
    if 'passed' in line or 'failed' in line or 'error' in line or 'coverage' in line.lower():
        print(line)
