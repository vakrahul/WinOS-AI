import ctypes
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

hwnd = 15076238
force_foreground(hwnd)
time.sleep(0.8)

# Press Escape to deselect any active box
user32.keybd_event(0x1B, 0, 0, 0)
time.sleep(0.05)
user32.keybd_event(0x1B, 0, 2, 0)
time.sleep(0.2)

# Click on the Brush tool at (360, 75)
print("Clicking Brush tool at (360, 75)...")
user32.SetCursorPos(360, 75)
time.sleep(0.1)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.3)

# Draw a spiral/circle on the canvas
print("Drawing on canvas with brush...")
cx, cy = 700, 450
r = 80

user32.SetCursorPos(cx + r, cy)
time.sleep(0.05)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.02)

import math
for i in range(1, 81):
    theta = (2 * math.pi * i) / 80
    x = int(cx + r * math.cos(theta))
    y = int(cy + r * math.sin(theta))
    user32.SetCursorPos(x, y)
    user32.mouse_event(0x0001, 0, 0, 0, 0)
    time.sleep(0.008)

user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.5)

img = ImageGrab.grab()
img.save("brush_real_result.png")
print("Saved brush_real_result.png.")
