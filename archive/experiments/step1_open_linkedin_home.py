import time
import win32gui
import win32con
import ctypes
import pyautogui
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

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

def main():
    print("[1] Bringing Chrome to foreground...")
    focus_chrome()
    cursor = HumanCursorController()

    print("[2] Gliding cursor to address bar over 2.5s...")
    cursor.move_smooth(500, 65, duration=2.5)
    cursor.click_smooth(500, 65, duration=0.2)
    time.sleep(0.3)

    print("[3] Navigating to base https://www.linkedin.com ...")
    pyautogui.write("https://www.linkedin.com", interval=0.01)
    pyautogui.press("enter")
    print("Waiting 5.0s for LinkedIn home to load...")
    time.sleep(5.0)

    img = ImageGrab.grab()
    img.save("linkedin_home_screen.png")
    print("Saved linkedin_home_screen.png")

if __name__ == "__main__":
    main()
