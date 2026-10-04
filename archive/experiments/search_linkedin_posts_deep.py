"""Deep LinkedIn search for real SDE Intern posts with contact emails."""
import base64
import ctypes
import json
import time
from PIL import ImageGrab
import httpx
import pyautogui
import win32con
import win32gui

from src.storage.credential_vault import CredentialVault
from src.windows_integration.vision_automation import HumanCursorController

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

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

    print("[2] Gliding to address bar...")
    cursor.move_smooth(500, 65, duration=2.0)
    cursor.click_smooth(500, 65, duration=0.2)
    time.sleep(0.3)

    # Search specifically for SDE intern posts with emails
    query = "https://www.linkedin.com/search/results/content/?keywords=SDE%20intern%20email%20apply&sortBy=%22date_posted%22"
    print(f"[3] Navigating to: {query}...")
    pyautogui.write(query, interval=0.008)
    pyautogui.press("enter")
    print("Waiting 6.0s for feed to load...")
    time.sleep(6.0)

    # Scroll down slowly through multiple posts, saving snapshots
    for scroll_idx in range(1, 4):
        print(f"[4.{scroll_idx}] Scrolling feed down (position {scroll_idx})...")
        pyautogui.scroll(-450)
        time.sleep(2.5)
        # Move cursor visibly to the post content area
        cursor.move_smooth(960, 500, duration=1.5)
        time.sleep(1.0)
        
        shot_path = f"linkedin_feed_scroll_{scroll_idx}.png"
        ImageGrab.grab().save(shot_path)
        print(f"Saved snapshot to '{shot_path}'.")

if __name__ == "__main__":
    main()
