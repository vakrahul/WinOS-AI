import ctypes
import time
import subprocess
import pyautogui

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

# Set file to clipboard as HDROP / FileDrop
pdf_path = r"C:\Users\RAHUL\Downloads\Rahul_vak_resume.pdf"
print(f"Copying {pdf_path} to clipboard as file object...")
subprocess.run([
    "powershell",
    "-NoProfile",
    "-Command",
    f"Set-Clipboard -Path '{pdf_path}'"
])
time.sleep(0.5)

# Click inside the email body text area (x=600, y=700) to ensure focus
print("Focusing email body...")
pyautogui.click(600, 700)
time.sleep(0.3)

# Paste file (Ctrl + V)
print("Pasting file to trigger Gmail attachment...")
pyautogui.hotkey("ctrl", "v")
time.sleep(3.0) # Wait for upload progress

# Capture screenshot to verify if attachment is now attached
from PIL import ImageGrab
img = ImageGrab.grab()
img.save("gmail_after_paste_attach.png")
print("Saved snapshot to gmail_after_paste_attach.png.")
