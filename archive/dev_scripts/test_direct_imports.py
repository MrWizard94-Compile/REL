"""Direct test of integration test imports"""
import sys
from pathlib import Path

# Add REL to path
sys.path.insert(0, r"C:\REL")

print("Testing imports...")
print("=" * 60)

try:
    # Test basic mcp_server imports
    print("1. Importing from mcp_server...")
    from mcp_server import (
        file_lock,
        atomic_write_json,
        deep_merge,
        calculate_days_since,
        get_priority_weight,
        calculate_urgency,
    )
    print("   ✅ Basic imports successful")
    
    # Test calculations
    print("\n2. Testing calculate_days_since...")
    days = calculate_days_since("2026-02-01")
    print(f"   ✅ Days since 2026-02-01: {days}")
    
    print("\n3. Testing deep_merge...")
    result = deep_merge({"a": 1}, {"b": 2})
    print(f"   ✅ Merge result: {result}")
    
    print("\n4. Testing get_priority_weight...")
    weight = get_priority_weight("high")
    print(f"   ✅ High priority weight: {weight}")
    
    print("\n5. Testing calculate_urgency...")
    project = {
        "last_worked": "2026-02-09",
        "priority": "high",
        "completion": 50,
        "status": "active"
    }
    urgency = calculate_urgency(project)
    print(f"   ✅ Urgency score: {urgency}")
    
    print("\n" + "=" * 60)
    print("✅ ALL IMPORTS AND BASIC TESTS PASSED!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
