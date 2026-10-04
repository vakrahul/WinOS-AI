import ctypes
import time
from PIL import ImageGrab
import pyautogui
from src.windows_integration.vision_automation import HumanCursorController

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

hwnd = 4654542
print(f"[1/3] Bringing LinkedIn window (HWND: {hwnd}) to foreground...")
force_foreground(hwnd)
time.sleep(1.0)

# Card 3 coordinates in physical: (375, 1120)
# In logical: (300, 896)
cursor = HumanCursorController()
print("[2/3] Gliding smoothly to Card 3: Alignerr...")
cursor.move_smooth(375, 1120, duration=0.8)
time.sleep(0.1)
pyautogui.click()
print("Clicked on Card 3 (Alignerr). Waiting 2.5s for detail pane to load...")
time.sleep(2.5)

print("[3/3] Capturing updated job detail snapshot...")
img = ImageGrab.grab()
img.save("alignerr_job_detail.png")
print("Saved snapshot to alignerr_job_detail.png.")
