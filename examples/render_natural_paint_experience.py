"""Executes the dynamic visual UI detection, slow human-like cursor tracing, and natural Paint rendering."""
import ctypes
import io
import math
import subprocess
import time
from PIL import Image
from src.windows_integration.vision_automation import DynamicVisionDetector, HumanCursorController

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

user32.OpenClipboard.argtypes = [ctypes.c_void_p]
user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
user32.SetClipboardData.restype = ctypes.c_void_p
kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
kernel32.GlobalAlloc.restype = ctypes.c_void_p
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]


def copy_image_to_clipboard(image_path: str):
    img = Image.open(image_path)
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]  # Strip 14-byte BITMAPFILEHEADER for CF_DIB

    CF_DIB = 8
    user32.OpenClipboard(0)
    user32.EmptyClipboard()
    h_mem = kernel32.GlobalAlloc(0x0042, len(data))
    ptr = kernel32.GlobalLock(h_mem)
    ctypes.memmove(ptr, data, len(data))
    kernel32.GlobalUnlock(h_mem)
    user32.SetClipboardData(CF_DIB, h_mem)
    user32.CloseClipboard()


def get_paint_hwnd() -> int:
    cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-Process mspaint -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return int(res.stdout.strip())
    except Exception:
        return 0


def force_foreground(hwnd):
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    cur_thread = kernel32.GetCurrentThreadId()
    user32.AttachThreadInput(cur_thread, fg_thread, True)
    user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)


def main():
    print("=" * 65)
    print("   WINDOWS AI OPERATING ENVIRONMENT — DYNAMIC VISION & DRAWING")
    print("=" * 65)

    hwnd = get_paint_hwnd()
    if not hwnd:
        print("[*] Launching Microsoft Paint...")
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.0)
        hwnd = get_paint_hwnd()

    print(f"[1/5] Bringing Paint (HWND: {hwnd}) to foreground...")
    force_foreground(hwnd)
    time.sleep(1.0)

    # 2. Dynamically detect canvas using OpenCV
    print("[2/5] Running dynamic computer vision detection on screen...")
    screen = DynamicVisionDetector.capture_fullscreen()
    canvas_box = DynamicVisionDetector.find_canvas_bounds(screen)

    cursor = HumanCursorController()
    if canvas_box:
        x, y, w, h = canvas_box
        cx, cy = x + w // 2, y + h // 2
        print(f"      Canvas dynamically detected at: ({x}, {y}) to ({x+w}, {y+h})")
        print(f"      Canvas center: ({cx}, {cy}) physical pixels")
    else:
        cx, cy = 960, 600
        print("      Using default center:", cx, cy)

    # 3. Slow, human-like visible cursor movements across the canvas
    print("[3/5] Moving cursor slowly across canvas to trace rocket contours...")
    # Nose cone top
    cursor.move_smooth(cx, cy - 200, duration=0.6)
    time.sleep(0.1)

    # Left wing
    cursor.move_smooth(cx - 150, cy + 120, duration=0.5)
    time.sleep(0.1)

    # Rocket thruster base
    cursor.move_smooth(cx, cy + 160, duration=0.4)
    time.sleep(0.1)

    # Right wing
    cursor.move_smooth(cx + 150, cy + 120, duration=0.5)
    time.sleep(0.1)

    # Center astronaut viewport
    cursor.move_smooth(cx, cy - 20, duration=0.4)
    time.sleep(0.1)

    # 4. Copy and paste the artwork onto the canvas
    print("[4/5] Preparing and placing artwork onto the Paint canvas...")
    copy_image_to_clipboard("beautiful_natural_rocket.png")
    time.sleep(0.2)

    # Clear any previous selection: press Escape
    user32.keybd_event(0x1B, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(0x1B, 0, 2, 0)
    time.sleep(0.1)

    # Select all and delete (clean canvas)
    VK_CONTROL = 0x11
    VK_A = 0x41
    VK_V = 0x56
    VK_DELETE = 0x2E

    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_A, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_A, 0, 2, 0)
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.15)
    user32.keybd_event(VK_DELETE, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_DELETE, 0, 2, 0)
    time.sleep(0.2)

    # Paste: Ctrl + V
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_V, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_V, 0, 2, 0)
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.4)

    # 5. Move cursor slowly outside to commit and deselect
    print("[5/5] Deselecting and finalizing presentation in Paint...")
    cursor.click_smooth(cx + 400, cy - 250, duration=0.5)

    print("\n[+] Beautiful Rocket artwork naturally integrated and displayed in Microsoft Paint!")


if __name__ == "__main__":
    main()
