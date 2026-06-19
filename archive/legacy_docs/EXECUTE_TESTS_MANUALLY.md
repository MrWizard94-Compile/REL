# Integration Tests - Manual Execution Required

**Status:** Tests created, verification scripts ready, **manual execution required**

**Issue:** I cannot directly execute tests on your Windows machine from this environment.

---

## What I Created

✅ **97 integration tests**
- tests/integration/test_mcp_server.py (47 tests)
- tests/integration/test_tool_handlers.py (50 tests)

✅ **Execution scripts**
- run_tests.bat (Windows batch file)
- verify_tests_ready.py (Pre-flight check)
- run_integration_now.py (Python test runner)

✅ **Documentation**
- Complete guides in improvement-plan/
- This execution instructions file

---

## How to Run Tests (3 Options)

### Option 1: Quick Batch File (EASIEST) ⭐

**Double-click:**
```
C:\REL\run_tests.bat
```

This will:
1. Run test_mcp_server.py
2. Run test_tool_handlers.py  
3. Run all tests with coverage
4. Generate HTML coverage report
5. Save results to text files

**Results will be in:**
- `integration_test1_results.txt`
- `integration_test2_results.txt`
- `all_tests_with_coverage.txt`
- `htmlcov/index.html` (open in browser)

---

### Option 2: Command Line (For detailed output)

**Open Command Prompt in C:\REL and run:**

```cmd
REM Verify tests are ready
.venv\Scripts\python.exe verify_tests_ready.py

REM Run integration tests only
.venv\Scripts\python.exe -m pytest tests/integration/ -v

REM Run all tests with coverage
.venv\Scripts\python.exe -m pytest tests/ -v --cov=. --cov-report=html

REM View coverage report
start htmlcov\index.html
```

---

### Option 3: PowerShell

```powershell
cd C:\REL

# Verify ready
& .\.venv\Scripts\python.exe verify_tests_ready.py

# Run tests
& .\.venv\Scripts\python.exe -m pytest tests/integration/ -v

# With coverage
& .\.venv\Scripts\python.exe -m pytest tests/ -v --cov=. --cov-report=html
```

---

## Expected Results

### If All Pass (Expected) ✅

```
========================== test session starts ==========================
platform win32 -- Python 3.14.3, pytest-9.0.2, pluggy-1.6.0
collected 191 items

tests/integration/test_mcp_server.py::TestFileLocking::test_file_lock_creates_lock_file PASSED [1%]
tests/integration/test_mcp_server.py::TestFileLocking::test_file_lock_releases_on_exit PASSED [2%]
... (all tests pass) ...

=================== 189 passed, 2 skipped in 25.0s ====================

Coverage report:
mcp_server.py        45%     (was 0%)
brain_typed.py       72%     (was 70.66%)
neural_web_typed.py  96%     (was 95.56%)
validation_models.py 72%     (was 70.15%)
------------------------
TOTAL                48%     (was 22.02%)
```

**This means:**
- ✅ All critical infrastructure works
- ✅ File locking prevents corruption
- ✅ Atomic operations work
- ✅ Cognitive modules verified
- ✅ Coverage doubled (22% → 48%)

---

### If Some Fail (Possible) ⚠️

**Common failures and fixes:**

1. **Import errors:**
   ```
   ImportError: cannot import name 'file_lock'
   ```
   **Fix:** Check mcp_server.py has all expected functions

2. **Fixture errors:**
   ```
   fixture 'tmp_path' not found
   ```
   **Fix:** Update pytest: `pip install -U pytest`

3. **Timeout errors:**
   ```
   TimeoutError in test_file_lock_timeout
   ```
   **Fix:** Adjust timeout values in test

4. **Path errors:**
   ```
   FileNotFoundError: C:\REL\...
   ```
   **Fix:** Check working directory is C:\REL

---

## What to Do After Running

### 1. Check Results

**Look for:**
- How many tests passed/failed
- What the coverage percentage is
- Any error messages

### 2. Review Coverage Report

**Open:** `C:\REL\htmlcov\index.html`

**Check:**
- mcp_server.py coverage (target: ~45%)
- Which lines are not covered
- Critical functions tested

### 3. Document Results

**Update these files:**
- improvement-plan/CURRENT_STATUS.md
- improvement-plan/SESSION_SUMMARY.md

**Record:**
- Actual test count passed
- Actual coverage achieved
- Any failures encountered

---

## Expected Coverage by File

| File | Before | After (Target) | Actual |
|------|--------|----------------|--------|
| mcp_server.py | 0.00% | ~45% | ? |
| brain_typed.py | 70.66% | ~72% | ? |
| neural_web_typed.py | 95.56% | ~96% | ? |
| validation_models.py | 70.15% | ~72% | ? |
| **TOTAL** | **22.02%** | **~48%** | **?** |

Fill in "Actual" after running tests.

---

## If Tests Pass - Next Steps

1. ✅ Update documentation with actual results
2. ✅ Commit tests to version control
3. ⏭️ **Phase 2 next:** Add more tests to reach 80% coverage
4. ⏭️ **Phase 3 next:** Add API documentation
5. ⏭️ **Phase 4 next:** Set up CI/CD

---

## If Tests Fail - Debugging

1. **Read error messages carefully**
2. **Check which test failed** - look at test name
3. **Check the traceback** - shows exact line
4. **Run single test:**
   ```cmd
   .venv\Scripts\python.exe -m pytest tests/integration/test_mcp_server.py::TestFileLocking::test_file_lock_creates_lock_file -v
   ```
5. **Add print statements if needed**
6. **Check test assumptions** - are paths correct?

---

## Troubleshooting

### "pytest not found"
```cmd
cd C:\REL
.venv\Scripts\pip install pytest pytest-asyncio pytest-cov
```

### "No module named 'mcp_server'"
Make sure you're in C:\REL directory when running tests.

### "Permission denied" on lock files
Close any programs that might have files open.

### Tests hang/timeout
Check for infinite loops or missing timeout parameters.

---

## Quick Validation Without Full Test Run

**Just check if tests can import:**
```cmd
cd C:\REL
.venv\Scripts\python.exe verify_tests_ready.py
```

This will:
- ✅ Check all imports work
- ✅ Test basic functions
- ✅ Count test functions
- ✅ Verify pytest available
- ⚠️ Not run full test suite (faster)

---

## Summary

**I created everything needed:**
- ✅ 97 integration tests
- ✅ 3 ways to run them
- ✅ Verification scripts
- ✅ Complete documentation

**You need to:**
1. Run: `C:\REL\run_tests.bat` or use command line
2. Check results
3. View coverage report: `htmlcov\index.html`
4. Report back actual coverage achieved

**Expected outcome:**
- 189-191 tests pass
- 2 tests skip (brain integration)
- Coverage: 22% → 48%
- mcp_server.py: 0% → 45%

---

**Status:** Ready to execute, waiting for manual run ⏳

**Estimated run time:** 20-30 seconds
