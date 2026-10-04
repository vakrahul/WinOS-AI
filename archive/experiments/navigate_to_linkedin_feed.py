import time
import win32gui
import win32con
import ctypes
import pyautogui
import pyperclip
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

LINKEDIN_SEARCH_URL = "https://www.linkedin.com/search/results/content/?keywords=SDE%20intern%20email%20apply&sortBy=%22date_posted%22"

def force_chrome_foreground():
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
    force_chrome_foreground()
    cursor = HumanCursorController()

    print("[2] Gliding cursor slowly to Address Bar (500, 65)...")
    cursor.move_smooth(500, 65, duration=2.5)
    cursor.click_smooth(500, 65, duration=0.2)
    time.sleep(0.4)

    # Use clipboard copy-paste to ensure 100% exact URL navigation
    print(f"[3] Pasting LinkedIn Search URL: {LINKEDIN_SEARCH_URL}...")
    pyperclip.copy(LINKEDIN_SEARCH_URL)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.3)
    pyautogui.press("enter")

    print("[4] Waiting 8.0s for LinkedIn search results feed to load completely...")
    time.sleep(8.0)

    # Save verification snapshot
    img = ImageGrab.grab()
    img.save("linkedin_real_feed_loaded.png")
    print("Saved 'linkedin_real_feed_loaded.png'.")

if __name__ == "__main__":
    main()
