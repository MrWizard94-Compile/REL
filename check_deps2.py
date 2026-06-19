import sys
results = []
for mod in ['pyautogui', 'psutil', 'PIL', 'winreg', 'mss']:
    try:
        __import__(mod)
        results.append(mod + ': OK')
    except ImportError as e:
        results.append(mod + ': MISSING - ' + str(e))

with open(r'C:\REL_Codex_Variant\dep_results.txt', 'w') as f:
    f.write('\n'.join(results) + '\n')
