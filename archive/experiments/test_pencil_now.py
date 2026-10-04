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

# Click on Pencil tool at (237, 65)
print("Clicking on Pencil tool at (237, 65)...")
user32.SetCursorPos(237, 65)
time.sleep(0.1)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.3)

# Now draw on the canvas from (500, 300) to (800, 500)
print("Drawing stroke from (500, 300) to (800, 500)...")
start_x, start_y = 500, 300
end_x, end_y = 800, 500

user32.SetCursorPos(start_x, start_y)
time.sleep(0.05)
user32.mouse_event(0x0002, 0, 0, 0, 0) # Left down
time.sleep(0.02)

steps = 60
for i in range(1, steps + 1):
    cx = int(start_x + (end_x - start_x) * (i / steps))
    cy = int(start_y + (end_y - start_y) * (i / steps))
    user32.SetCursorPos(cx, cy)
    user32.mouse_event(0x0001, 0, 0, 0, 0)
    time.sleep(0.005)

user32.mouse_event(0x0004, 0, 0, 0, 0) # Left up
time.sleep(0.5)

img = ImageGrab.grab()
img.save("pencil_now_result.png")
print("Saved pencil_now_result.png.")
