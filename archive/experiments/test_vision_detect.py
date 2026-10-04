import cv2
import ctypes
import time
from src.windows_integration.vision_automation import DynamicVisionDetector, HumanCursorController

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

import subprocess
cmd = ["powershell", "-NoProfile", "-Command", "(Get-Process mspaint -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle"]
res = subprocess.run(cmd, capture_output=True, text=True)
hwnd = int(res.stdout.strip()) if res.stdout.strip() else 0

if not hwnd:
    print("Paint not running.")
    exit(1)

force_foreground(hwnd)
time.sleep(1.0)

# Capture screen
screen = DynamicVisionDetector.capture_fullscreen()
print(f"Captured screen size: {screen.shape[1]}x{screen.shape[0]}")

# Detect canvas
canvas_box = DynamicVisionDetector.find_canvas_bounds(screen)
print("Detected Canvas Bounding Box:", canvas_box)

cursor = HumanCursorController()
print("Display scale factor:", cursor.scale_factor)

if canvas_box:
    x, y, w, h = canvas_box
    cx = x + w // 2
    cy = y + h // 2
    print(f"Canvas Center in Physical Pixels: ({cx}, {cy})")
    lx, ly = cursor.physical_to_logical(cx, cy)
    print(f"Canvas Center in Logical Pixels: ({lx}, {ly})")
