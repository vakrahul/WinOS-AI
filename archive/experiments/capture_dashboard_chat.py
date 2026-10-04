import ctypes
import subprocess
import time
from PIL import ImageGrab

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def force_foreground(hwnd):
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    cur_thread = kernel32.GetCurrentThreadId()
    user32.AttachThreadInput(cur_thread, fg_thread, True)
    user32.ShowWindow(hwnd, 3) # Maximize
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)

cmd = [
    "powershell",
    "-NoProfile",
    "-Command",
    "(Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like '*WinAI-OE*' } | Select-Object -First 1).MainWindowHandle"
]
res = subprocess.run(cmd, capture_output=True, text=True)
hwnd_str = res.stdout.strip()
if hwnd_str and hwnd_str.isdigit():
    hwnd = int(hwnd_str)
    force_foreground(hwnd)
    time.sleep(1.0)
    img = ImageGrab.grab()
    img.save("dashboard_chat_snapshot.png")
    print("Captured updated dashboard to dashboard_chat_snapshot.png.")
else:
    print("Window handle not found.")
