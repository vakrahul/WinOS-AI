import ctypes
import time
from PIL import ImageGrab
import pyautogui
from src.windows_integration.vision_automation import HumanCursorController

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

hwnd = 7735086
print(f"[1/3] Focusing n8n window (HWND: {hwnd})...")
force_foreground(hwnd)
time.sleep(1.0)

# Physical coordinates of "Create workflow": (982, 281)
cursor = HumanCursorController()
print("[2/3] Gliding smoothly to 'Create workflow' button...")
cursor.move_smooth(982, 281, duration=0.8)
time.sleep(0.1)
pyautogui.click()
print("Clicked 'Create workflow'. Waiting 3.5s for canvas to initialize...")
time.sleep(3.5)

print("[3/3] Capturing new canvas snapshot...")
img = ImageGrab.grab()
img.save("n8n_new_canvas_live.png")
print("Saved snapshot to n8n_new_canvas_live.png.")
