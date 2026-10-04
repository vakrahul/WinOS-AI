import ctypes
import time

user32 = ctypes.windll.user32

hwnd = 2756398

# Force foreground
user32.keybd_event(0x12, 0, 0, 0) # ALT down
user32.ShowWindow(hwnd, 9)
user32.SetForegroundWindow(hwnd)
user32.keybd_event(0x12, 0, 2, 0) # ALT up

time.sleep(0.5)

VK_CONTROL = 0x11
VK_3 = 0x33

# Press Ctrl + 3
user32.keybd_event(VK_CONTROL, 0, 0, 0)
user32.keybd_event(VK_3, 0, 0, 0)
time.sleep(0.05)
user32.keybd_event(VK_3, 0, 2, 0)
user32.keybd_event(VK_CONTROL, 0, 2, 0)

time.sleep(1.0)

length = user32.GetWindowTextLengthW(hwnd)
buff = ctypes.create_unicode_buffer(length + 1)
user32.GetWindowTextW(hwnd, buff, length + 1)
print("Updated Window Title:", buff.value.encode('ascii', 'replace').decode('ascii'))
