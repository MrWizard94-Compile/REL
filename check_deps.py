import sys
for mod in ['pyautogui','psutil','PIL','winreg']:
    try:
        __import__(mod)
        print(mod + ': OK')
    except ImportError as e:
        print(mod + ': MISSING - ' + str(e))
