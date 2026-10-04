import ctypes
import time
from PIL import ImageGrab
import pyautogui

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

hwnd = 7081570
print(f"Bringing Chrome window (HWND: {hwnd}) to foreground...")
force_foreground(hwnd)
time.sleep(1.0)

# Switch to Tab 2 (Ctrl + 2) which is 'Workflows - n8n'
print("Switching to Tab 2 ('Workflows - n8n')...")
pyautogui.hotkey("ctrl", "2")
time.sleep(2.0)

img = ImageGrab.grab()
img.save("n8n_workflows_page.png")
print("Saved snapshot to n8n_workflows_page.png.")
