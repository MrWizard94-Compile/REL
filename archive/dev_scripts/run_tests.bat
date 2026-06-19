@echo off
REM Run integration tests for REL project
REM This script runs pytest on the integration tests

echo ========================================
echo Running Integration Tests
echo ========================================
echo.

cd /d C:\REL

echo Running test_mcp_server.py...
.\.venv\Scripts\python.exe -m pytest tests\integration\test_mcp_server.py -v --tb=short > integration_test1_results.txt 2>&1

echo.
echo Running test_tool_handlers.py...
.\.venv\Scripts\python.exe -m pytest tests\integration\test_tool_handlers.py -v --tb=short > integration_test2_results.txt 2>&1

echo.
echo Running all tests with coverage...
.\.venv\Scripts\python.exe -m pytest tests\ -v --cov=. --cov-report=html --cov-report=term > all_tests_with_coverage.txt 2>&1

echo.
echo ========================================
echo Tests Complete!
echo ========================================
echo.
echo Results saved to:
echo   - integration_test1_results.txt
echo   - integration_test2_results.txt
echo   - all_tests_with_coverage.txt
echo   - htmlcov\index.html (coverage report)
echo.

pause
