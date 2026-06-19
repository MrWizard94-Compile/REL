@echo off
cd C:\REL
.\.venv\Scripts\pip.exe install -e ".[dev]" > install_log.txt 2>&1
.\.venv\Scripts\pytest.exe -v --tb=short > test_log.txt 2>&1
echo Installation and test logs created
type install_log.txt
echo.
echo ====================
echo.
type test_log.txt
