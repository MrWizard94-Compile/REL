import subprocess

result = subprocess.run(
    [r'C:\REL\.venv\Scripts\pytest.exe', '--co', '-q', 'tests/'],
    capture_output=True,
    text=True,
    cwd=r'C:\REL'
)

with open(r'C:\REL\test_count.txt', 'w') as f:
    f.write(result.stdout)
    f.write('\n\n')
    f.write(result.stderr)

print("Test count written to test_count.txt")
