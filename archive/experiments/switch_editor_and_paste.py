import ctypes
import json
from pathlib import Path
import time
from PIL import ImageGrab
import pyautogui
from src.windows_integration.vision_automation import HumanCursorController

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def force_foreground(hwnd):
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    cur_thread = kernel32.GetCurrentThreadId()
    user32.AttachThreadInput(cur_thread, fg_thread, True)
    user32.ShowWindow(hwnd, 3)
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)

hwnd = 7735086
force_foreground(hwnd)
time.sleep(1.0)

cursor = HumanCursorController()

# [1/4] Click "Editor" tab at (565, 318) physical
print("[1/4] Gliding smoothly to 'Editor' tab at (565, 318)...")
cursor.move_smooth(565, 318, duration=0.8)
time.sleep(0.1)
pyautogui.click()
print("Switched to Editor canvas. Waiting 2s...")
time.sleep(2.0)

# [2/4] Copy workflow JSON to clipboard
print("[2/4] Copying AI_Environment_Sample_Automation.json to clipboard...")
wf_json = Path("AI_Environment_Sample_Automation.json").read_text(encoding="utf-8")

user32.OpenClipboard(0)
user32.EmptyClipboard()
text_bytes = (wf_json + "\0").encode("utf-16le")
kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
kernel32.GlobalAlloc.restype = ctypes.c_void_p
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
h_mem = kernel32.GlobalAlloc(0x0042, len(text_bytes))
ptr = kernel32.GlobalLock(h_mem)
ctypes.memmove(ptr, text_bytes, len(text_bytes))
kernel32.GlobalUnlock(h_mem)
user32.SetClipboardData(13, h_mem)
user32.CloseClipboard()

# [3/4] Click canvas center (700, 500) and Paste (Ctrl + V)
print("[3/4] Pasting full 5-node workflow onto canvas...")
cursor.move_smooth(700, 500, duration=0.6)
time.sleep(0.2)
pyautogui.click()
time.sleep(0.3)
pyautogui.hotkey("ctrl", "v")
time.sleep(2.5)

# Save (Ctrl + S)
print("[4/4] Saving workflow (Ctrl + S)...")
pyautogui.hotkey("ctrl", "s")
time.sleep(1.5)

# Capture verification snapshot
img = ImageGrab.grab()
img.save("n8n_canvas_populated.png")
print("Saved snapshot to n8n_canvas_populated.png.")
