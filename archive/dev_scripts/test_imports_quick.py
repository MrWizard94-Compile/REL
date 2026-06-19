"""Quick test to verify imports work"""
import sys
from pathlib import Path

sys.path.insert(0, r"C:\REL")

try:
    from mcp_server import (
        file_lock,
        atomic_write_json,
        calculate_days_since,
        deep_merge,
    )
    print("✅ Basic imports successful")
    
    # Test calculate_days_since
    days = calculate_days_since("2026-02-01")
    print(f"✅ calculate_days_since works: {days} days")
    
    # Test deep_merge
    result = deep_merge({"a": 1}, {"b": 2})
    print(f"✅ deep_merge works: {result}")
    
    print("\n✅ All basic tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
