"""Step 1: Open Gmail normally (no URL params) and click Compose with slow visible cursor."""
import time
import win32gui
import win32con
import ctypes
import pyautogui
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def force_chrome_foreground():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "chrome" in title or "linkedin" in title:
                windows.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if hwnds:
        h = sorted(hwnds, key=lambda x: "linkedin" in x[1] or "chrome" in x[1], reverse=True)[0][0]
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
    print("[1] Focusing Chrome...")
    force_chrome_foreground()
    cursor = HumanCursorController()

    print("[2] Gliding cursor slowly to Address Bar (500, 65)...")
    cursor.move_smooth(500, 65, duration=2.5)
    cursor.click_smooth(500, 65, duration=0.2)
    time.sleep(0.3)

    print("[3] Navigating to clean Gmail URL (https://mail.google.com/mail/u/0/#inbox)...")
    pyautogui.write("https://mail.google.com/mail/u/0/#inbox", interval=0.01)
    pyautogui.press("enter")
    print("Waiting 6.0s for Gmail inbox to load...")
    time.sleep(6.0)

    # Click Compose button at (55, 230)
    print("[4] Gliding cursor slowly to 'Compose' button at (55, 230) over 3.0s...")
    cursor.move_smooth(55, 230, duration=3.0)
    time.sleep(0.4)
    print("Clicking Compose...")
    cursor.click_smooth(55, 230, duration=0.2)
    time.sleep(2.5)

    img = ImageGrab.grab()
    img.save("gmail_compose_opened.png")
    print("Saved 'gmail_compose_opened.png'.")

if __name__ == "__main__":
    main()
