@echo off
REM Run fixed integration tests
REM This script runs pytest on the fixed integration tests

echo ========================================
echo Running FIXED Integration Tests
echo ========================================
echo.

cd /d C:\REL

echo [1/3] Running test_mcp_server.py (FIXED)...
.\.venv\Scripts\python.exe -m pytest tests\integration\test_mcp_server.py -v --tb=short > test_mcp_server_fixed.txt 2>&1

echo [2/3] Running test_tool_handlers.py (FIXED)...
.\.venv\Scripts\python.exe -m pytest tests\integration\test_tool_handlers.py -v --tb=short > test_tool_handlers_fixed.txt 2>&1

echo [3/3] Running test_coverage_boost.py (NEW)...
.\.venv\Scripts\python.exe -m pytest tests\integration\test_coverage_boost.py -v --tb=short > test_coverage_boost.txt 2>&1

echo.
echo Running ALL tests with coverage measurement...
.\.venv\Scripts\python.exe -m pytest tests\ -v --cov=mcp_server --cov-report=html --cov-report=term > all_tests_fixed_results.txt 2>&1

echo.
echo ========================================
echo Tests Complete!
echo ========================================
echo.
echo Results saved to:
echo   - test_mcp_server_fixed.txt
echo   - test_tool_handlers_fixed.txt
echo   - test_coverage_boost.txt
echo   - all_tests_fixed_results.txt
echo   - htmlcov\index.html (coverage report)
echo.

pause
