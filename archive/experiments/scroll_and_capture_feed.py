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

# Move cursor over center feed and scroll down
cursor = HumanCursorController()
cursor.move_smooth(600, 500, duration=0.4)
time.sleep(0.2)

print("Scrolling down the LinkedIn hiring posts feed...")
pyautogui.scroll(-800)
time.sleep(2.0)

img = ImageGrab.grab()
img.save("linkedin_posts_search_page2.png")
print("Saved page 2 snapshot to linkedin_posts_search_page2.png.")
