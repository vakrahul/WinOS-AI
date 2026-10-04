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

# Clear selection: press Escape 3 times
print("Pressing Escape to clear selection...")
pyautogui.press("escape")
time.sleep(0.1)
pyautogui.press("escape")
time.sleep(0.2)

# Click on Pencil at logical (256, 88)
print("Clicking Pencil at (256, 88)...")
pyautogui.click(256, 88)
time.sleep(0.3)

# Now drag on canvas
print("Drawing stroke from (400, 300) to (700, 500)...")
pyautogui.moveTo(400, 300)
time.sleep(0.05)
pyautogui.dragTo(700, 500, duration=0.4, button="left")
time.sleep(0.5)

img = ImageGrab.grab()
img.save("test_escape_result.png")
print("Saved test_escape_result.png.")
