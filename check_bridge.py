import sys
sys.path.insert(0, r'C:\REL_Codex_Variant')
try:
    import py_compile
    py_compile.compile(r'C:\REL_Codex_Variant\windows_bridge.py', doraise=True)
    result = 'SYNTAX OK'
except py_compile.PyCompileError as e:
    result = f'SYNTAX ERROR: {e}'

# Also test the import
try:
    import windows_bridge
    result += '\nIMPORT OK - REL_SERVER_PID=' + str(windows_bridge.REL_SERVER_PID)
except Exception as e:
    result += f'\nIMPORT ERROR: {e}'

with open(r'C:\REL_Codex_Variant\bridge_check.txt', 'w') as f:
    f.write(result + '\n')
