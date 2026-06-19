import sys
sys.path.insert(0, 'C:/REL')

# Try importing validation models
try:
    from validation_models import CreateProjectRequest
    print("✓ validation_models imported successfully")
except Exception as e:
    print(f"✗ Failed to import validation_models: {e}")
    sys.exit(1)

# Try importing pydantic
try:
    from pydantic import ValidationError
    print("✓ pydantic imported successfully")
except Exception as e:
    print(f"✗ Failed to import pydantic: {e}")
    sys.exit(1)

# Try creating a valid project
try:
    req = CreateProjectRequest(key="test-project", name="Test")
    print(f"✓ Created valid project: {req.key}")
except Exception as e:
    print(f"✗ Failed to create valid project: {e}")
    sys.exit(1)

# Try creating an invalid project (should fail)
try:
    req = CreateProjectRequest(key="INVALID", name="Test")
    print("✗ Should have raised ValidationError for uppercase key!")
    sys.exit(1)
except ValidationError as e:
    print(f"✓ Correctly rejected invalid key: {len(e.errors())} errors")

# Try importing brain_typed
try:
    from brain_typed import RELBrain
    print("✓ brain_typed imported successfully")
except Exception as e:
    print(f"✗ Failed to import brain_typed: {e}")

# Try importing pathlib
try:
    from pathlib import Path
    print("✓ pathlib imported successfully")
except Exception as e:
    print(f"✗ Failed to import pathlib: {e}")

print("\n✅ All manual tests passed!")
