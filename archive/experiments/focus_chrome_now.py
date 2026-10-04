import ctypes
import subprocess
import time
from PIL import ImageGrab

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

cmd = ["powershell", "-NoProfile", "-Command", "(Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle"]
res = subprocess.run(cmd, capture_output=True, text=True)
hwnd = int(res.stdout.strip())
print(f"Targeting Chrome HWND: {hwnd}")

# Attach thread input to bypass Windows focus restrictions
cur_thread = kernel32.GetCurrentThreadId()
fg_hwnd = user32.GetForegroundWindow()
fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
user32.AttachThreadInput(cur_thread, fg_thread, True)

user32.ShowWindow(hwnd, 9) # SW_RESTORE
time.sleep(0.2)
user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
user32.BringWindowToTop(hwnd)
user32.SetForegroundWindow(hwnd)

user32.AttachThreadInput(cur_thread, fg_thread, False)
time.sleep(1.0)

# Switch to Tab 2 ('Workflows - n8n')
import pyautogui
pyautogui.hotkey("ctrl", "2")
time.sleep(2.0)

img = ImageGrab.grab()
img.save("n8n_workflows_page.png")
print("Saved snapshot to n8n_workflows_page.png.")
