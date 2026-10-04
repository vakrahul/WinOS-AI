import ctypes
import time
from pathlib import Path

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

user32.GetClipboardData.restype = ctypes.c_void_p
user32.GetClipboardData.argtypes = [ctypes.c_uint]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]

def get_clipboard_text():
    CF_UNICODETEXT = 13
    if not user32.OpenClipboard(0):
        return ""
    try:
        h_clip = user32.GetClipboardData(CF_UNICODETEXT)
        if not h_clip:
            return ""
        ptr = kernel32.GlobalLock(h_clip)
        if not ptr:
            return ""
        text = ctypes.wstring_at(ptr)
        kernel32.GlobalUnlock(h_clip)
        return text
    finally:
        user32.CloseClipboard()

hwnd = 30673418

# Maximize and bring to foreground
user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
user32.BringWindowToTop(hwnd)
user32.SetForegroundWindow(hwnd)
time.sleep(1.0)

# Click on the center of the feed
user32.SetCursorPos(700, 400)
user32.mouse_event(2, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(4, 0, 0, 0, 0)
time.sleep(0.5)

VK_CONTROL = 0x11
VK_A = 0x41
VK_C = 0x43

# Select All
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_A, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_A, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)
time.sleep(0.5)

# Copy
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_C, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_C, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)
time.sleep(0.5)

clip = get_clipboard_text()
print(f"Captured text length: {len(clip)}")
Path("captured_x_feed.txt").write_text(clip, encoding="utf-8")

lines = [l.strip() for l in clip.splitlines() if l.strip()]
print(f"Captured {len(lines)} lines")
for l in lines[:50]:
    safe = l.encode("ascii", "replace").decode("ascii")
    print(">>", safe)
