import time
import win32gui
import win32con
import ctypes
import pyautogui
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

RESUME_PATH = r"C:\Users\RAHUL\Downloads\Rahul_vak_resume.pdf"

def force_chrome_foreground():
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd).lower()
            if "gmail" in title or "chrome" in title:
                windows.append((hwnd, title))
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if hwnds:
        h = sorted(hwnds, key=lambda x: "gmail" in x[1], reverse=True)[0][0]
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
    print("[1] Bringing Gmail window to foreground...")
    force_chrome_foreground()
    cursor = HumanCursorController()

    # Step 1: Click the paperclip attachment icon at (246, 920)
    print("Gliding cursor to attachment paperclip icon (246, 920)...")
    cursor.move_smooth(246, 920, duration=2.5)
    time.sleep(0.3)
    print("Clicking attachment icon to open Windows File Picker...")
    cursor.click_smooth(246, 920, duration=0.2)
    time.sleep(2.0)

    # Step 2: In Windows File Picker, type full path to resume PDF and press Enter
    print(f"Typing resume file path: '{RESUME_PATH}'...")
    pyautogui.write(RESUME_PATH, interval=0.015)
    time.sleep(0.5)
    print("Submitting file selection (Enter)...")
    pyautogui.press("enter")

    # Step 3: Wait for upload to complete
    print("Waiting 4.0s for resume PDF upload to complete...")
    time.sleep(4.0)

    # Step 4: Glide to Send button at (145, 920)
    print("Gliding cursor to Send button (145, 920)...")
    cursor.move_smooth(145, 920, duration=2.5)
    time.sleep(0.4)

    # Step 5: Click Send
    print("Clicking Send button to dispatch email...")
    cursor.click_smooth(145, 920, duration=0.2)
    time.sleep(3.5)

    # Step 6: Capture confirmation screenshot
    img = ImageGrab.grab()
    img.save("gmail_confirmed_sent.png")
    print("Saved 'gmail_confirmed_sent.png'.")

if __name__ == "__main__":
    main()
