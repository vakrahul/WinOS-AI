import ctypes
import time
from PIL import ImageGrab

user32 = ctypes.windll.user32

# Click Pencil at (325, 90)
user32.SetCursorPos(325, 90)
time.sleep(0.1)
user32.mouse_event(2, 0, 0, 0, 0)
time.sleep(0.05)
user32.mouse_event(4, 0, 0, 0, 0)
time.sleep(0.5)

# Capture crop of the pencil tool to verify highlight
img = ImageGrab.grab()
crop = img.crop((280, 60, 480, 140))
crop.save("pencil_highlight_check.png")
print("Saved pencil_highlight_check.png")
