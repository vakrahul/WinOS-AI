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

# Click on Pencil icon at (233, 67)
print("Clicking on Pencil tool at (233, 67)...")
user32.SetCursorPos(233, 67)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.3)

# Click on canvas at (600, 300) to clear any active selection
user32.SetCursorPos(600, 300)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.2)

# Click on Pencil icon again to ensure it's selected
user32.SetCursorPos(233, 67)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.3)

# Now draw a circle on the canvas
print("Drawing a circle on canvas...")
cx, cy = 700, 400
r = 60

user32.SetCursorPos(cx + r, cy)
time.sleep(0.05)
user32.mouse_event(0x0002, 0, 0, 0, 0) # Left down
time.sleep(0.02)

import math
for i in range(1, 61):
    theta = (2 * math.pi * i) / 60
    x = int(cx + r * math.cos(theta))
    y = int(cy + r * math.sin(theta))
    user32.SetCursorPos(x, y)
    user32.mouse_event(0x0001, 0, 0, 0, 0) # Move
    time.sleep(0.008)

user32.mouse_event(0x0004, 0, 0, 0, 0) # Left up
time.sleep(0.5)

img = ImageGrab.grab()
img.save("pencil_test.png")
print("Saved pencil_test.png.")
