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
    user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)

hwnd = 15076238
force_foreground(hwnd)
time.sleep(1.0)

# Click on Pencil icon (x=210, y=85)
user32.SetCursorPos(210, 85)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.3)

# Clear canvas: Ctrl + A -> Delete
VK_CONTROL = 0x11
VK_A = 0x41
VK_DELETE = 0x2E
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_A, 0, 0, 0)
time.sleep(0.05)
user32.keybd_event(VK_A, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)
time.sleep(0.2)
user32.keybd_event(VK_DELETE, 0, 0, 0)
time.sleep(0.05)
user32.keybd_event(VK_DELETE, 0, 2, 0)
time.sleep(0.3)

# Click on Pencil tool AGAIN to exit selection box and select pencil!
user32.SetCursorPos(210, 85)
user32.mouse_event(0x0002, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(0x0004, 0, 0, 0, 0)
time.sleep(0.3)

# Draw an X on the canvas
def draw_line(x1, y1, x2, y2):
    user32.SetCursorPos(x1, y1)
    time.sleep(0.02)
    user32.mouse_event(0x0002, 0, 0, 0, 0)
    time.sleep(0.02)
    steps = 40
    for i in range(1, steps + 1):
        cx = int(x1 + (x2 - x1) * (i / steps))
        cy = int(y1 + (y2 - y1) * (i / steps))
        user32.SetCursorPos(cx, cy)
        user32.mouse_event(0x0001, 0, 0, 0, 0) # MOVE
        time.sleep(0.005)
    user32.mouse_event(0x0004, 0, 0, 0, 0)
    time.sleep(0.02)

draw_line(600, 350, 900, 650)
draw_line(900, 350, 600, 650)

time.sleep(0.5)
img = ImageGrab.grab()
img.save("verify_stroke.png")
print("Verification snapshot saved to verify_stroke.png")
