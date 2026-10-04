import win32gui
import win32con
import ctypes
import time
from PIL import ImageGrab

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title and any(k in title.lower() for k in ["linkedin", "chrome", "google"]):
            windows.append((hwnd, title))
    return True

windows = []
win32gui.EnumWindows(callback, windows)
print("Visible matching windows:", windows)

if windows:
    # Prefer one with linkedin in title, else first chrome
    target_hwnd, target_title = sorted(windows, key=lambda x: "linkedin" in x[1].lower(), reverse=True)[0]
    print(f"Targeting HWND: {target_hwnd} -> '{target_title}'")
    cur_thread = kernel32.GetCurrentThreadId()
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    user32.AttachThreadInput(cur_thread, fg_thread, True)
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    user32.ShowWindow(target_hwnd, win32con.SW_RESTORE)
    user32.ShowWindow(target_hwnd, win32con.SW_MAXIMIZE)
    user32.BringWindowToTop(target_hwnd)
    user32.SetForegroundWindow(target_hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)
    time.sleep(1.5)

img = ImageGrab.grab()
img.save("chrome_linkedin_view.png")
print("Saved chrome_linkedin_view.png")
