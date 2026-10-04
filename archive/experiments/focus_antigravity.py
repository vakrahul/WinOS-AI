import ctypes
import subprocess
import time

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def force_foreground(hwnd):
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    cur_thread = kernel32.GetCurrentThreadId()
    user32.AttachThreadInput(cur_thread, fg_thread, True)
    user32.ShowWindow(hwnd, 3) # Maximize / Restore
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)

cmd = [
    "powershell",
    "-NoProfile",
    "-Command",
    "(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -like '*Antigravity*' -and $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle"
]
res = subprocess.run(cmd, capture_output=True, text=True)
hwnd_str = res.stdout.strip()
if hwnd_str and hwnd_str.isdigit():
    hwnd = int(hwnd_str)
    print(f"Found Antigravity IDE (HWND: {hwnd}). Bringing to foreground...")
    force_foreground(hwnd)
    time.sleep(1.0)
    print("Antigravity IDE focused.")
else:
    print("Could not find Antigravity IDE window handle.")
