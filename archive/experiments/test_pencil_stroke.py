import ctypes
import time

user32 = ctypes.windll.user32

hwnd = 15076238
user32.ShowWindow(hwnd, 3) # Maximize
user32.BringWindowToTop(hwnd)
user32.SetForegroundWindow(hwnd)
time.sleep(0.8)

# 1. Click on the Pencil tool in the toolbar (x=210, y=85)
print("Selecting Pencil tool...")
user32.SetCursorPos(210, 85)
user32.mouse_event(0x0002, 0, 0, 0, 0) # Left down
time.sleep(0.05)
user32.mouse_event(0x0004, 0, 0, 0, 0) # Left up
time.sleep(0.3)

# 2. Draw a big clear diagonal test stroke across the canvas
print("Drawing test stroke with MOUSEEVENTF_MOVE...")
start_x, start_y = 600, 300
end_x, end_y = 900, 600

user32.SetCursorPos(start_x, start_y)
time.sleep(0.05)
user32.mouse_event(0x0002, 0, 0, 0, 0) # Left down
time.sleep(0.02)

steps = 60
for i in range(1, steps + 1):
    cx = int(start_x + (end_x - start_x) * (i / steps))
    cy = int(start_y + (end_y - start_y) * (i / steps))
    user32.SetCursorPos(cx, cy)
    user32.mouse_event(0x0001, 0, 0, 0, 0) # MOUSEEVENTF_MOVE!
    time.sleep(0.01)

user32.mouse_event(0x0004, 0, 0, 0, 0) # Left up
print("Stroke completed.")
