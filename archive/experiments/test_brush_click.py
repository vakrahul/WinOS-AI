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

# Press Escape multiple times to clear any selection box
for _ in range(3):
    user32.keybd_event(0x1B, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(0x1B, 0, 2, 0)
    time.sleep(0.05)

# Click on the Brushes button at (x=369, y=75)
print("Clicking Brushes button at (369, 75)...")
user32.SetCursorPos(369, 75)
time.sleep(0.1)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.3)

# Now draw on the canvas at x=500..800, y=300..500
print("Drawing a brush stroke across canvas...")
start_x, start_y = 500, 350
end_x, end_y = 800, 350

user32.SetCursorPos(start_x, start_y)
time.sleep(0.05)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.02)

steps = 40
for i in range(1, steps + 1):
    cx = int(start_x + (end_x - start_x) * (i / steps))
    cy = int(start_y + (end_y - start_y) * (i / steps))
    user32.SetCursorPos(cx, cy)
    user32.mouse_event(0x0001, 0, 0, 0, 0) # MOVE
    time.sleep(0.005)

user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.5)

img = ImageGrab.grab()
img.save("brush_stroke_test.png")
print("Saved brush_stroke_test.png.")
