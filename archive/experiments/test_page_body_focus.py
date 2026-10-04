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

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

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

def get_chrome_hwnd() -> int:
    import subprocess
    cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return int(res.stdout.strip())
    except Exception:
        return 0

hwnd = get_chrome_hwnd()
print("Target Chrome HWND:", hwnd)
if not hwnd:
    exit(1)

# Bring to foreground
user32.keybd_event(0x12, 0, 0, 0)
user32.ShowWindow(hwnd, 9)
user32.SetForegroundWindow(hwnd)
user32.keybd_event(0x12, 0, 2, 0)
time.sleep(0.8)

# Get window position and click inside page body
rect = RECT()
user32.GetWindowRect(hwnd, ctypes.byref(rect))
center_x = rect.left + (rect.right - rect.left) // 2
center_y = rect.top + 350 # Click below toolbar in the feed area
print(f"Clicking at ({center_x}, {center_y}) to focus page contents...")

user32.SetCursorPos(center_x, center_y)
user32.mouse_event(2, 0, 0, 0, 0) # Left down
time.sleep(0.05)
user32.mouse_event(4, 0, 0, 0, 0) # Left up
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
print(f"Clipboard length: {len(clip)} characters")
Path("captured_page_text.txt").write_text(clip, encoding="utf-8")

lines = [l.strip() for l in clip.splitlines() if l.strip()]
print(f"Captured {len(lines)} lines")
for l in lines[:40]:
    print(">>", l.encode('ascii', 'replace').decode('ascii'))
