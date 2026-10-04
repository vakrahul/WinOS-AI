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
    user32.ShowWindow(hwnd, 3) # Maximize
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)

hwnd = 4654542
print(f"Bringing Gmail window (HWND: {hwnd}) to foreground...")
force_foreground(hwnd)
time.sleep(1.0)

# Dismiss any AI helper / popup by clicking in the message body
pyautogui.click(600, 600)
time.sleep(0.3)

# Send the email using Ctrl + Enter
print("Executing Send command (Ctrl + Enter)...")
pyautogui.hotkey("ctrl", "enter")
time.sleep(3.0)

img = ImageGrab.grab()
img.save("gmail_sent_confirmation.png")
print("Saved sent confirmation snapshot to gmail_sent_confirmation.png.")
