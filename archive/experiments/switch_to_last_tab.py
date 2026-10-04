import ctypes
import subprocess
import time
from PIL import ImageGrab
import pyautogui

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

cmd = ["powershell", "-NoProfile", "-Command", "(Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle"]
res = subprocess.run(cmd, capture_output=True, text=True)
hwnd = int(res.stdout.strip())
print(f"Targeting Chrome HWND: {hwnd}")

# Bring to foreground
cur_thread = kernel32.GetCurrentThreadId()
fg_hwnd = user32.GetForegroundWindow()
fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
user32.AttachThreadInput(cur_thread, fg_thread, True)
user32.ShowWindow(hwnd, 3) # Maximize
user32.SetForegroundWindow(hwnd)
user32.BringWindowToTop(hwnd)
user32.AttachThreadInput(cur_thread, fg_thread, False)
time.sleep(1.0)

# Press Ctrl + 9 to switch to the last (newest) tab
print("Switching to last tab (Ctrl + 9)...")
pyautogui.hotkey("ctrl", "9")
time.sleep(2.5)

img = ImageGrab.grab()
img.save("last_tab_snapshot.png")
print("Saved snapshot to last_tab_snapshot.png.")
