import time
import win32gui
import win32con
from PIL import ImageGrab

def callback(hwnd, windows):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:
            windows.append((hwnd, title))
    return True

windows = []
win32gui.EnumWindows(callback, windows)

chrome_windows = []
for hwnd, title in windows:
    if any(k in title.lower() for k in ["deadshot", "chrome"]):
        chrome_windows.append((hwnd, title))
        print(f"Found Window: HWND {hwnd} -> '{title}'")

if chrome_windows:
    target_hwnd, target_title = sorted(chrome_windows, key=lambda x: "deadshot" in x[1].lower(), reverse=True)[0]
    print(f"Activating target: HWND {target_hwnd} -> '{target_title}'")

    import ctypes
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    cur_thread = kernel32.GetCurrentThreadId()
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)

    user32.AttachThreadInput(cur_thread, fg_thread, True)
    # Simulate ALT tap to break lock
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)

    user32.ShowWindow(target_hwnd, 9) # SW_RESTORE
    user32.ShowWindow(target_hwnd, 3) # SW_MAXIMIZE
    user32.BringWindowToTop(target_hwnd)
    user32.SetForegroundWindow(target_hwnd)

    user32.AttachThreadInput(cur_thread, fg_thread, False)
    time.sleep(1.5)

img = ImageGrab.grab()
img.save("deadshot_active.png")
print("Saved deadshot_active.png")
