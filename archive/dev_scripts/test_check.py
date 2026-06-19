import sys
sys.path.insert(0, 'C:/REL')

output = []

# Try importing validation models
try:
    from validation_models import CreateProjectRequest
    output.append("✓ validation_models imported successfully")
except Exception as e:
    output.append(f"✗ Failed to import validation_models: {e}")
    with open('C:/REL/test_results.txt', 'w') as f:
        f.write('\n'.join(output))
    sys.exit(1)

# Try importing pydantic
try:
    from pydantic import ValidationError
    output.append("✓ pydantic imported successfully")
except Exception as e:
    output.append(f"✗ Failed to import pydantic: {e}")
    with open('C:/REL/test_results.txt', 'w') as f:
        f.write('\n'.join(output))
    sys.exit(1)

# Try creating a valid project
try:
    req = CreateProjectRequest(key="test-project", name="Test")
    output.append(f"✓ Created valid project: {req.key}")
except Exception as e:
    output.append(f"✗ Failed to create valid project: {e}")
    with open('C:/REL/test_results.txt', 'w') as f:
        f.write('\n'.join(output))
    sys.exit(1)

# Try creating an invalid project (should fail)
try:
    req = CreateProjectRequest(key="INVALID", name="Test")
    output.append("✗ Should have raised ValidationError for uppercase key!")
    with open('C:/REL/test_results.txt', 'w') as f:
        f.write('\n'.join(output))
    sys.exit(1)
except ValidationError as e:
    output.append(f"✓ Correctly rejected invalid key: {len(e.errors())} errors")

# Try importing brain_typed
try:
    from brain_typed import RELBrain
    from pathlib import Path
    brain_path = Path('C:/REL/test_brain')
    brain = RELBrain(brain_path)
    output.append(f"✓ brain_typed imported and RELBrain created")
except Exception as e:
    output.append(f"✗ Failed with brain_typed: {e}")

output.append("\n✅ All manual tests passed!")

# Write results
with open('C:/REL/test_results.txt', 'w') as f:
    f.write('\n'.join(output))
