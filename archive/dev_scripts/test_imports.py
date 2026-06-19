#!/usr/bin/env python3
import sys
print(f"Python: {sys.version}", file=sys.stderr)
print(f"Platform: {sys.platform}", file=sys.stderr)

try:
    import msvcrt
    print("✓ msvcrt OK", file=sys.stderr)
except Exception as e:
    print(f"✗ msvcrt: {e}", file=sys.stderr)
    sys.exit(1)

try:
    from mcp.server import Server
    print("✓ mcp OK", file=sys.stderr)
except Exception as e:
    print(f"✗ mcp: {e}", file=sys.stderr)
    sys.exit(1)

try:
    sys.path.insert(0, "C:/REL")
    from brain import get_brain
    from neural_web import get_neural_web
    print("✓ brain & neural_web OK", file=sys.stderr)
except Exception as e:
    print(f"✗ modules: {e}", file=sys.stderr)
    sys.exit(1)

print("All imports successful!", file=sys.stderr)
sys.exit(0)
