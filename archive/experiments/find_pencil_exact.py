import ctypes
import time
from PIL import ImageGrab
import win32gui

user32 = ctypes.windll.user32

# Bring Paint to foreground
def callback(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd) and "paint" in win32gui.GetWindowText(hwnd).lower():
        extra.append(hwnd)
    return True
hwnds = []
win32gui.EnumWindows(callback, hwnds)
if hwnds:
    user32.ShowWindow(hwnds[0], 3)
    user32.SetForegroundWindow(hwnds[0])
time.sleep(1.0)

# Let's test clicking at (170, 95) vs (220, 95) vs (325, 105)
# In maximized Paint, where is the Tools group?
# Let's crop the toolbar x=100 to 500, y=60 to 150
img = ImageGrab.grab()
crop = img.crop((100, 60, 500, 150))
crop.save("tools_ribbon_now.png")
print("Cropped tools_ribbon_now.png")
