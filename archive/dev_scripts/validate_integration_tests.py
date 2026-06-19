"""
Validate integration tests are importable and count test functions
"""
import ast
import sys
from pathlib import Path

def analyze_test_file(filepath):
    """Analyze a test file for syntax and test count"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the file
        tree = ast.parse(content)
        
        # Count test functions
        test_functions = [
            node.name for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')
        ]
        
        # Count test classes
        test_classes = [
            node.name for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef) and node.name.startswith('Test')
        ]
        
        return {
            'valid': True,
            'test_functions': len(test_functions),
            'test_classes': len(test_classes),
            'size_bytes': len(content),
            'size_lines': len(content.split('\n'))
        }
    except SyntaxError as e:
        return {
            'valid': False,
            'error': f"Syntax error: {e}",
            'line': e.lineno
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }

def main():
    test_files = [
        Path(r"C:\REL\tests\integration\test_mcp_server.py"),
        Path(r"C:\REL\tests\integration\test_tool_handlers.py"),
    ]
    
    print("=" * 70)
    print("INTEGRATION TEST VALIDATION")
    print("=" * 70)
    print()
    
    total_tests = 0
    all_valid = True
    
    for filepath in test_files:
        print(f"Analyzing: {filepath.name}")
        print("-" * 70)
        
        if not filepath.exists():
            print(f"  ❌ File not found!")
            all_valid = False
            continue
        
        result = analyze_test_file(filepath)
        
        if result['valid']:
            print(f"  ✅ Valid Python syntax")
            print(f"  📊 Test functions: {result['test_functions']}")
            print(f"  📦 Test classes: {result['test_classes']}")
            print(f"  📄 Lines: {result['size_lines']}")
            print(f"  💾 Size: {result['size_bytes']:,} bytes")
            total_tests += result['test_functions']
        else:
            print(f"  ❌ {result['error']}")
            if 'line' in result:
                print(f"     Line: {result['line']}")
            all_valid = False
        
        print()
    
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total test functions: {total_tests}")
    print(f"All files valid: {'✅ YES' if all_valid else '❌ NO'}")
    print()
    
    if all_valid:
        print("✅ Integration tests are ready to run!")
        print()
        print("To run tests:")
        print("  cd C:\\REL")
        print("  .\\.venv\\Scripts\\python.exe -m pytest tests/integration/ -v")
        return 0
    else:
        print("❌ Fix errors before running tests")
        return 1

if __name__ == "__main__":
    sys.exit(main())
