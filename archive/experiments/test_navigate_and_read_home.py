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

def set_clipboard_text(text: str):
    CF_UNICODETEXT = 13
    user32.OpenClipboard(0)
    user32.EmptyClipboard()
    text_bytes = (text + "\0").encode("utf-16le")
    h_mem = kernel32.GlobalAlloc(0x0042, len(text_bytes))
    ptr = kernel32.GlobalLock(h_mem)
    ctypes.memmove(ptr, text_bytes, len(text_bytes))
    kernel32.GlobalUnlock(h_mem)
    user32.SetClipboardData(CF_UNICODETEXT, h_mem)
    user32.CloseClipboard()

hwnd = 30673418
user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
user32.BringWindowToTop(hwnd)
user32.SetForegroundWindow(hwnd)
time.sleep(0.8)

VK_CONTROL = 0x11
VK_L = 0x4C
VK_RETURN = 0x0D
VK_ESCAPE = 0x1B
VK_A = 0x41
VK_C = 0x43
VK_V = 0x56

# Focus address bar (Ctrl + L)
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_L, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_L, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)
time.sleep(0.3)

# Paste https://x.com/home and press Enter
set_clipboard_text("https://x.com/home")
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_V, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_V, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)
time.sleep(0.2)

user32.keybd_event(VK_RETURN, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_RETURN, 0, 2, 0)

print("Navigating to https://x.com/home... Waiting 4s for feed to render...")
time.sleep(4.0)

# Press Escape to exit address bar focus
user32.keybd_event(VK_ESCAPE, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_ESCAPE, 0, 2, 0)
time.sleep(0.3)

# Click on feed margin (x=450, y=450)
user32.SetCursorPos(450, 450)
user32.mouse_event(2, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(4, 0, 0, 0, 0)
time.sleep(0.5)

# Select all (Ctrl + A)
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_A, 0, 0, 0)
time.sleep(0.1)
user32.keybd_event(VK_A, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)
time.sleep(0.5)

# Copy (Ctrl + C)
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
for l in lines[:60]:
    safe = l.encode("ascii", "replace").decode("ascii")
    print(">>", safe)
