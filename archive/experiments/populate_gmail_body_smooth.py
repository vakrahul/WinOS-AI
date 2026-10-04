import time
import win32gui
import win32con
import ctypes
import pyperclip
import pyautogui
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

BODY_TEXT = """Hi Hiring Team,

I came across OxAstra's focus on recent expansion in edge computer vision and real-time model inference and wanted to reach out.

In response to recent demand spikes in AI/ML Research Intern roles, I have been actively building:
• Model Optimization & Deep Learning: Published research in IRE Journals on Transformer data leakage and explanation faithfulness.
• Production AI Agents: Built Nexus Agent (autonomous execution platform) and prompt defense frameworks on https://rahulvakiti.space.
• Startup Engineering: SDE Intern at xstratum.ai and Core Product Team at Aden (YC-backed startup), building scalable agentic pipelines.

Portfolio: https://rahulvakiti.space
My resume (Rahul_vak_resume.pdf) is attached for reference.

Would you be opposed to a brief 5-minute sync this week to explore if my background aligns with your team's goals?

Best regards,
Rahul Vakiti
vakitirahul@gmail.com | +91-7416754611"""

def ensure_chrome_focused():
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
    ensure_chrome_focused()
    cursor = HumanCursorController()

    print("Gliding cursor slowly to the email body area (350, 320) over 3.0s...")
    cursor.move_smooth(350, 320, duration=3.0)
    time.sleep(0.3)

    print("Focusing email body...")
    cursor.click_smooth(350, 320, duration=0.2)
    time.sleep(0.4)

    print("Pasting clean, formatted 'no AI slop' cold email...")
    pyperclip.copy(BODY_TEXT)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1.0)

    # Move visibly to the attachment paperclip icon at (246, 918)
    print("Gliding cursor slowly to the Attachment icon (246, 918) over 3.0s...")
    cursor.move_smooth(246, 918, duration=3.0)
    time.sleep(1.0)

    # Save verification snapshot
    img = ImageGrab.grab()
    img.save("gmail_draft_ready.png")
    print("Verification screenshot saved to 'gmail_draft_ready.png'.")

if __name__ == "__main__":
    main()
