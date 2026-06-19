"""
Verify integration tests can import and basic functionality works
This doesn't run full pytest but checks that tests would be able to run
"""
import sys
from pathlib import Path
import ast

# Add REL to path
sys.path.insert(0, r"C:\REL")

print("=" * 70)
print("INTEGRATION TEST VERIFICATION")
print("=" * 70)
print()

# Check 1: Can we import from mcp_server?
print("1. Testing mcp_server imports...")
try:
    from mcp_server import (
        file_lock,
        atomic_write_json,
        deep_merge,
        calculate_days_since,
        get_priority_weight,
        calculate_urgency,
        analyze_context_pressure,
        check_statement_conflict,
        get_story_arc_analysis,
        get_affective_trends_analysis,
    )
    print("   ✅ All required functions importable")
except ImportError as e:
    print(f"   ❌ Import error: {e}")
    sys.exit(1)

# Check 2: Test basic functionality
print()
print("2. Testing basic functions...")
try:
    # Test calculate_days_since
    days = calculate_days_since("2026-02-01")
    assert isinstance(days, int)
    print(f"   ✅ calculate_days_since: {days} days")
    
    # Test deep_merge
    result = deep_merge({"a": 1}, {"b": 2})
    assert result == {"a": 1, "b": 2}
    print(f"   ✅ deep_merge: {result}")
    
    # Test get_priority_weight
    weight = get_priority_weight("high")
    assert weight == 2.0
    print(f"   ✅ get_priority_weight('high'): {weight}")
    
    # Test calculate_urgency
    project = {
        "last_worked": "2026-02-09",
        "priority": "high",
        "completion": 50,
        "status": "active"
    }
    urgency = calculate_urgency(project)
    assert isinstance(urgency, float)
    print(f"   ✅ calculate_urgency: {urgency}")
    
except Exception as e:
    print(f"   ❌ Function test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Check 3: Can we parse test files?
print()
print("3. Validating test file syntax...")
test_files = [
    Path(r"C:\REL\tests\integration\test_mcp_server.py"),
    Path(r"C:\REL\tests\integration\test_tool_handlers.py"),
]

total_tests = 0
for test_file in test_files:
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the file
        tree = ast.parse(content)
        
        # Count test functions
        test_funcs = [
            node.name for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')
        ]
        
        print(f"   ✅ {test_file.name}: {len(test_funcs)} tests")
        total_tests += len(test_funcs)
        
    except Exception as e:
        print(f"   ❌ {test_file.name}: {e}")
        sys.exit(1)

# Check 4: Test pytest is available
print()
print("4. Checking pytest availability...")
try:
    import pytest
    print(f"   ✅ pytest {pytest.__version__} available")
except ImportError:
    print("   ❌ pytest not installed")
    print("      Run: pip install pytest pytest-asyncio pytest-cov")
    sys.exit(1)

# Summary
print()
print("=" * 70)
print("VERIFICATION SUMMARY")
print("=" * 70)
print(f"✅ All imports successful")
print(f"✅ Basic functions working")
print(f"✅ {total_tests} test functions found")
print(f"✅ pytest available")
print()
print("Tests are ready to run!")
print()
print("To run tests:")
print("  cd C:\\REL")
print("  .\\run_tests.bat")
print()
print("Or manually:")
print("  .venv\\Scripts\\python.exe -m pytest tests/integration/ -v")
print()
print("=" * 70)
