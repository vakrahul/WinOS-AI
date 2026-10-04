import ctypes

user32 = ctypes.windll.user32

class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]

def check_window(hwnd, _):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if "Google Chrome" in title:
                rect = RECT()
                user32.GetWindowRect(hwnd, ctypes.byref(rect))
                safe_title = title.encode("ascii", "replace").decode("ascii")
                print(f"HWND {hwnd}: '{safe_title}' -> left={rect.left}, top={rect.top}, right={rect.right}, bottom={rect.bottom}")
    return True

CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
user32.EnumWindows(CMPFUNC(check_window), 0)
