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

# Scroll down smoothly
cursor = HumanCursorController()
cursor.move_smooth(600, 500, duration=0.4)
time.sleep(0.2)
pyautogui.scroll(-450)
time.sleep(2.0)

img = ImageGrab.grab()
img.save("oxastra_post_lower.png")
print("Saved lower half of OxAstra post to oxastra_post_lower.png.")
