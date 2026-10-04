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
    user32.ShowWindow(hwnd, 3)
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)

hwnd = 4654542
force_foreground(hwnd)
time.sleep(1.0)

# Move cursor over the right detail pane (physical x=1000, y=550)
cursor = HumanCursorController()
print("Moving cursor over the right job description pane...")
cursor.move_smooth(1000, 550, duration=0.6)
time.sleep(0.2)

# Click once to ensure right pane is active, then scroll down
pyautogui.click()
time.sleep(0.2)
print("Scrolling down to reveal full job requirements...")
pyautogui.scroll(-600)
time.sleep(1.5)

img = ImageGrab.grab()
img.save("alignerr_scrolled_desc.png")
print("Saved scrolled description snapshot to alignerr_scrolled_desc.png.")
