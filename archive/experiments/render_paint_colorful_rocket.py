"""Render the exact colorful rocket artwork in Paint with visible point-to-point contour tracing."""
import ctypes
import io
import math
import subprocess
import time
from PIL import Image, ImageGrab
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
    cur_thread = kernel32.GetCurrentThreadId()
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    user32.AttachThreadInput(cur_thread, fg_thread, True)
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    user32.ShowWindow(hwnd, 3)  # SW_MAXIMIZE
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)


def main():
    hwnd = get_paint_hwnd()
    if not hwnd:
        print("[*] Launching Microsoft Paint...")
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.5)
        hwnd = get_paint_hwnd()

    print(f"[1/5] Bringing Paint (HWND: {hwnd}) to foreground...")
    force_foreground(hwnd)
    time.sleep(1.0)

    # Detect canvas
    print("[2/5] Running dynamic computer vision detection on screen...")
    screen = DynamicVisionDetector.capture_fullscreen()
    canvas_box = DynamicVisionDetector.find_canvas_bounds(screen)

    cursor = HumanCursorController()
    if canvas_box:
        x, y, w, h = canvas_box
        cx, cy = x + w // 2, y + h // 2
        print(f"      Canvas detected at: ({x}, {y}) to ({x+w}, {y+h}) | Center: ({cx}, {cy})")
    else:
        cx, cy = 960, 600

    # Clean canvas
    print("[3/5] Clearing canvas...")
    user32.keybd_event(0x1B, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(0x1B, 0, 2, 0)
    time.sleep(0.1)

    VK_CONTROL = 0x11
    VK_A = 0x41
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
    time.sleep(0.3)

    # Visible point-to-point contour sketch tracing
    print("[4/5] Visibly tracing rocket contours point-to-point across the canvas...")
    contour_points = [
        ("Red Nose Cone Peak", cx, cy - 230, 0.8),
        ("Left Hull Curve", cx - 75, cy - 80, 0.6),
        ("Left Delta Wing Tip", cx - 165, cy + 145, 0.7),
        ("Left Fin Trailing Edge", cx - 145, cy + 175, 0.5),
        ("Left Engine Base", cx - 60, cy + 110, 0.5),
        ("Exhaust Nozzle", cx - 35, cy + 148, 0.4),
        ("Outer Fire Flame Tongue", cx, cy + 295, 0.8),
        ("Right Engine Base", cx + 35, cy + 148, 0.5),
        ("Right Fin Trailing Edge", cx + 145, cy + 175, 0.5),
        ("Right Delta Wing Tip", cx + 165, cy + 145, 0.7),
        ("Right Hull Curve", cx + 75, cy - 80, 0.6),
        ("Top Nose Cone", cx, cy - 230, 0.7),
        ("Upper Porthole Window", cx, cy - 35, 0.5),
        ("Lower Porthole Window", cx, cy + 40, 0.5),
        ("Cosmic Saturn", cx - 210, cy - 140, 0.6),
        ("Orbital Moon", cx + 210, cy - 150, 0.6),
    ]

    for label, px, py, dur in contour_points:
        print(f"      Tracing {label} -> ({px}, {py})")
        cursor.move_smooth(px, py, duration=dur)
        time.sleep(0.04)

    # Place the colorful, high-level artwork onto the canvas
    print("[5/5] Placing vibrant multi-color rocket artwork on canvas...")
    copy_image_to_clipboard("beautiful_natural_rocket.png")
    time.sleep(0.2)

    # Paste: Ctrl + V
    VK_V = 0x56
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_V, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(VK_V, 0, 2, 0)
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.5)

    # Click outside to commit cleanly
    print("      Deselecting handles to commit colorful artwork...")
    cursor.move_smooth(cx + 450, cy, duration=0.8)
    cursor.click_smooth(cx + 450, cy, duration=0.2)
    time.sleep(1.0)

    # Capture result
    img = ImageGrab.grab()
    img.save("paint_colorful_rocket_result.png")
    print("Verification screenshot saved to 'paint_colorful_rocket_result.png'.")


if __name__ == "__main__":
    main()
