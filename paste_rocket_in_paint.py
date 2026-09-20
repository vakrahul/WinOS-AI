import io
import ctypes
import subprocess
import time
from PIL import Image

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
    data = output.getvalue()[14:]  # Strip BITMAPFILEHEADER for CF_DIB

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

def main():
    print("[1/4] Copying searched high-res rocket image to clipboard...")
    copy_image_to_clipboard("high_res_rocket.png")

    hwnd = get_paint_hwnd()
    if not hwnd:
        print("[!] Paint is not running. Launching mspaint...")
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.0)
        hwnd = get_paint_hwnd()

    print(f"[2/4] Focusing MS Paint (HWND: {hwnd})...")
    user32.keybd_event(0x12, 0, 0, 0)  # ALT down
    user32.ShowWindow(hwnd, 3)         # SW_MAXIMIZE
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.keybd_event(0x12, 0, 2, 0)  # ALT up
    time.sleep(1.0)

    VK_CONTROL = 0x11
    VK_A = 0x41
    VK_V = 0x56
    VK_DELETE = 0x2E

    # [3/4] Clear old canvas: Ctrl + A -> Delete
    print("[3/4] Clearing previous canvas...")
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_A, 0, 0, 0)
    time.sleep(0.1)
    user32.keybd_event(VK_A, 0, 2, 0)
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.3)

    user32.keybd_event(VK_DELETE, 0, 0, 0)
    time.sleep(0.1)
    user32.keybd_event(VK_DELETE, 0, 2, 0)
    time.sleep(0.5)

    # [4/4] Paste searched reference rocket: Ctrl + V
    print("[4/4] Pasting exact searched rocket image onto canvas...")
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_V, 0, 0, 0)
    time.sleep(0.1)
    user32.keybd_event(VK_V, 0, 2, 0)
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.5)

    # Click outside to deselect
    user32.SetCursorPos(800, 300)
    user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.05)
    user32.mouse_event(4, 0, 0, 0, 0)

    print("\n[+] Exact searched rocket picture pasted and designed onto MS Paint canvas!")

if __name__ == "__main__":
    main()
