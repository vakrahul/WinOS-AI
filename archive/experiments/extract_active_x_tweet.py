import ctypes
import time
from pathlib import Path

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# 64-bit signatures
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

def force_foreground(hwnd):
    user32.keybd_event(0x12, 0, 0, 0) # ALT down
    user32.ShowWindow(hwnd, 9) # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    user32.keybd_event(0x12, 0, 2, 0) # ALT up

hwnd = 2756398
print(f"Bringing Chrome window (HWND: {hwnd}) to foreground...")
force_foreground(hwnd)
time.sleep(1.0)

VK_CONTROL = 0x11
VK_A = 0x41
VK_C = 0x43

# Press Ctrl + A
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_A, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_A, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)

time.sleep(0.5)

# Press Ctrl + C
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_C, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_C, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)

time.sleep(0.5)

clip_text = get_clipboard_text()
print(f"Captured {len(clip_text)} characters from webpage.")

if clip_text:
    Path("captured_page_text.txt").write_text(clip_text, encoding="utf-8")
    lines = [l.strip() for l in clip_text.splitlines() if l.strip()]
    print(f"Saved {len(lines)} lines to captured_page_text.txt")
    print("\n--- SAMPLE EXTRACTED LINES ---")
    for l in lines[:25]:
        safe = l.encode("ascii", "replace").decode("ascii")
        print(">>", safe)
