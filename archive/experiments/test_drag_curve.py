import ctypes
import time
import math
import pyautogui
from PIL import ImageGrab

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

hwnd = 15076238
force_foreground(hwnd)
time.sleep(0.8)

# Click on canvas to ensure focus
pyautogui.click(600, 300)
time.sleep(0.2)

# Draw circle using dragTo
cx, cy = 700, 450
r = 60
pyautogui.moveTo(cx + r, cy)
time.sleep(0.05)

print("Drawing with pyautogui.dragTo...")
for i in range(1, 17):
    theta = (2 * math.pi * i) / 16
    x = int(cx + r * math.cos(theta))
    y = int(cy + r * math.sin(theta))
    pyautogui.dragTo(x, y, duration=0.02, button="left")

time.sleep(0.5)
img = ImageGrab.grab()
img.save("drag_circle_result.png")
print("Saved drag_circle_result.png.")
