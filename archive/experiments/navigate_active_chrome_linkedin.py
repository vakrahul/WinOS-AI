import time
import pyautogui
import win32gui
import win32con
import ctypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def focus_chrome():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "chrome" in title:
                windows.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if hwnds:
        h = hwnds[0]
        cur_thread = kernel32.GetCurrentThreadId()
        fg_hwnd = user32.GetForegroundWindow()
        fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
        user32.AttachThreadInput(cur_thread, fg_thread, True)
        user32.keybd_event(0x12, 0, 0, 0)
        user32.keybd_event(0x12, 0, 2, 0)
        user32.ShowWindow(h, win32con.SW_RESTORE)
        user32.ShowWindow(h, win32con.SW_MAXIMIZE)
        user32.BringWindowToTop(h)
        user32.SetForegroundWindow(h)
        user32.AttachThreadInput(cur_thread, fg_thread, False)
        time.sleep(1.0)

focus_chrome()

# Focus address bar and navigate directly
print("Focusing address bar via Ctrl + L...")
pyautogui.hotkey("ctrl", "l")
time.sleep(0.3)
url = "https://www.linkedin.com/search/results/content/?keywords=AI%20intern%20email&sortBy=%22date_posted%22"
pyautogui.write(url, interval=0.01)
time.sleep(0.2)
pyautogui.press("enter")
print("Navigated to LinkedIn. Waiting 5s for page to render...")
time.sleep(5.0)

from PIL import ImageGrab
img = ImageGrab.grab()
img.save("linkedin_real_view.png")
print("Saved linkedin_real_view.png")
