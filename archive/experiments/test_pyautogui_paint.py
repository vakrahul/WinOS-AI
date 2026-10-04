import ctypes
import time
import pyautogui
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

hwnd = 15076238
force_foreground(hwnd)
time.sleep(1.0)

print("Testing pyautogui drag on canvas...")
pyautogui.moveTo(500, 350)
time.sleep(0.1)
pyautogui.dragTo(800, 550, duration=0.6, button="left")
time.sleep(0.5)

img = ImageGrab.grab()
img.save("pyautogui_test_result.png")
print("Saved pyautogui_test_result.png.")
