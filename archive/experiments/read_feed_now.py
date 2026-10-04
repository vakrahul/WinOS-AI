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

# Find chrome window
hwnd = 0
def check_win(h, _):
    global hwnd
    if user32.IsWindowVisible(h):
        length = user32.GetWindowTextLengthW(h)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(h, buff, length + 1)
            if "Google Chrome" in buff.value:
                hwnd = h
                return False
    return True

CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
user32.EnumWindows(CMPFUNC(check_win), 0)
print("Found Chrome HWND:", hwnd)

user32.ShowWindow(hwnd, 9) # Restore
user32.BringWindowToTop(hwnd)
user32.SetForegroundWindow(hwnd)
time.sleep(1.0)

# Press Page Up then Down to ensure we are at the top of the feed
user32.keybd_event(0x21, 0, 0, 0) # Page Up
time.sleep(0.05)
user32.keybd_event(0x21, 0, 2, 0)
time.sleep(0.5)

# Click on feed margin
user32.SetCursorPos(600, 300)
user32.mouse_event(2, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(4, 0, 0, 0, 0)
time.sleep(0.5)

VK_CONTROL = 0x11
VK_A = 0x41
VK_C = 0x43

# Ctrl + A
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_A, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_A, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)
time.sleep(0.5)

# Ctrl + C
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_C, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_C, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)
time.sleep(0.5)

clip = get_clipboard_text()
print(f"Captured text length: {len(clip)}")
Path("captured_feed_now.txt").write_text(clip, encoding="utf-8")

lines = [l.strip() for l in clip.splitlines() if l.strip()]
print(f"Total lines: {len(lines)}")
for idx, l in enumerate(lines[:60]):
    safe = l.encode("ascii", "replace").decode("ascii")
    print(f"[{idx}] {safe}")
