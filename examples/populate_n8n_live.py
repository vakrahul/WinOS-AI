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
    user32.ShowWindow(hwnd, 3) # Maximize
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)

hwnd = 2754762
print(f"[1/5] Bringing n8n canvas (HWND: {hwnd}) to foreground...")
force_foreground(hwnd)
time.sleep(1.0)

# 2. Read workflow JSON and copy to clipboard as CF_UNICODETEXT
print("[2/5] Reading AI_Environment_Sample_Automation.json and copying to clipboard...")
wf_path = Path("AI_Environment_Sample_Automation.json")
wf_text = wf_path.read_text(encoding="utf-8")

user32.OpenClipboard(0)
user32.EmptyClipboard()
text_bytes = (wf_text + "\0").encode("utf-16le")
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
time.sleep(0.5)

# 3. Click canvas center to ensure focus, then paste
cursor = HumanCursorController()
print("[3/5] Moving to canvas center and pasting workflow nodes (Ctrl + V)...")
# Canvas center in physical is roughly (960, 560), convert to logical:
cursor.click_smooth(960, 560, duration=0.6)
time.sleep(0.3)

pyautogui.hotkey("ctrl", "v")
print("Pasted nodes! Waiting 3s for n8n to render nodes...")
time.sleep(3.0)

# 4. Execute Workflow (Ctrl + Enter in n8n runs the workflow)
print("[4/5] Triggering workflow execution via Manual Trigger (Ctrl + Enter)...")
pyautogui.hotkey("ctrl", "enter")
time.sleep(3.5)

# 5. Save Workflow (Ctrl + S)
print("[5/5] Saving workflow (Ctrl + S)...")
pyautogui.hotkey("ctrl", "s")
time.sleep(1.5)

# Capture verification screenshot
img = ImageGrab.grab()
img.save("n8n_executed_canvas_snapshot.png")
print("Saved execution verification snapshot to n8n_executed_canvas_snapshot.png.")
