import subprocess
import sys

# Run pytest and capture output
result = subprocess.run(
    [r'C:\REL\.venv\Scripts\pytest.exe', '-v', '--tb=short', '--co', 'tests/'],
    capture_output=True,
    text=True,
    cwd=r'C:\REL'
)

# Count tests
output_lines = result.stdout.split('\n')
test_lines = [line for line in output_lines if '::test_' in line]

print(f"Total tests discovered: {len(test_lines)}")
print(f"\nRunning full test suite...")

# Now run tests for real
result = subprocess.run(
    [r'C:\REL\.venv\Scripts\pytest.exe', '-v', '--tb=line', 'tests/'],
    capture_output=True,
    text=True,
    cwd=r'C:\REL'
)

# Write results to file
with open(r'C:\REL\full_test_results.txt', 'w', encoding='utf-8') as f:
    f.write("=== FULL TEST SUITE RESULTS ===\n\n")
    f.write(f"Return code: {result.returncode}\n\n")
    f.write("=== OUTPUT ===\n")
    f.write(result.stdout)
    if result.stderr:
        f.write("\n\n=== ERRORS ===\n")
        f.write(result.stderr)

# Print summary
if result.returncode == 0:
    print("\n✅ ALL TESTS PASSED!")
else:
    print(f"\n❌ Tests failed with return code: {result.returncode}")

print(f"\nFull results written to: C:\\REL\\full_test_results.txt")

# Try to extract summary from output
summary_started = False
for line in result.stdout.split('\n'):
    if 'passed' in line.lower() or 'failed' in line.lower():
        summary_started = True
    if summary_started:
        print(line)
