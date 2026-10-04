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
    user32.ShowWindow(hwnd, 3)
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)

hwnd = 15076238
force_foreground(hwnd)
time.sleep(0.8)

# Clear previous canvas: Ctrl + A -> Delete
pyautogui.hotkey("ctrl", "a")
time.sleep(0.1)
pyautogui.press("delete")
time.sleep(0.3)

# Click on Pencil tool: let's test clicking on (240, 70)
print("Clicking at (240, 70)...")
pyautogui.click(240, 70)
time.sleep(0.3)

# Draw a smooth curve on canvas
print("Drawing curved stroke on canvas...")
pyautogui.moveTo(600, 400)
time.sleep(0.05)
pyautogui.mouseDown()
time.sleep(0.02)

import math
for i in range(1, 50):
    t = i / 50.0
    x = 600 + t * 300
    y = 400 + math.sin(t * math.pi) * 100
    pyautogui.moveTo(x, y)
    time.sleep(0.005)

pyautogui.mouseUp()
time.sleep(0.5)

img = ImageGrab.grab()
img.save("test_pencil_curve.png")
print("Saved test_pencil_curve.png.")
