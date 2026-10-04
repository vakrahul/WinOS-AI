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

# Click on Pencil tool at logical (256, 88)
print("Clicking Pencil tool at logical (256, 88)...")
pyautogui.click(256, 88)
time.sleep(0.3)

# Clear canvas
pyautogui.hotkey("ctrl", "a")
time.sleep(0.1)
pyautogui.press("delete")
time.sleep(0.3)

# Click Pencil tool AGAIN to deselect any selection box
pyautogui.click(256, 88)
time.sleep(0.3)

# Draw a diagonal line using dragTo
print("Drawing stroke on canvas from (500, 300) to (800, 600)...")
pyautogui.moveTo(500, 300)
time.sleep(0.05)
pyautogui.dragTo(800, 600, duration=0.5, button="left")
time.sleep(0.5)

img = ImageGrab.grab()
img.save("pencil_exact_result.png")
print("Saved pencil_exact_result.png.")
