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

VK_CONTROL = 0x11
VK_N = 0x4E

# Press Ctrl + N (New)
print("Creating new Paint document (Ctrl + N)...")
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_N, 0, 0, 0)
time.sleep(0.08)
user32.keybd_event(VK_N, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)
time.sleep(0.5)

# Press 'n' or Right Arrow + Enter to choose 'Don't Save'
VK_RIGHT = 0x27
VK_RETURN = 0x0D
user32.keybd_event(VK_RIGHT, 0, 0, 0)
time.sleep(0.05)
user32.keybd_event(VK_RIGHT, 0, 2, 0)
time.sleep(0.1)
user32.keybd_event(VK_RETURN, 0, 0, 0)
time.sleep(0.05)
user32.keybd_event(VK_RETURN, 0, 2, 0)
time.sleep(0.8)

# Draw a diagonal line
print("Drawing stroke on fresh canvas...")
start_x, start_y = 500, 300
end_x, end_y = 800, 600

user32.SetCursorPos(start_x, start_y)
time.sleep(0.05)
user32.mouse_event(0x0002, 0, 0, 0, 0) # Left Down
time.sleep(0.02)

steps = 40
for i in range(1, steps + 1):
    cx = int(start_x + (end_x - start_x) * (i / steps))
    cy = int(start_y + (end_y - start_y) * (i / steps))
    user32.SetCursorPos(cx, cy)
    user32.mouse_event(0x0001, 0, 0, 0, 0) # Move
    time.sleep(0.005)

user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.5)

img = ImageGrab.grab()
img.save("new_doc_stroke_test.png")
print("Saved new_doc_stroke_test.png.")
