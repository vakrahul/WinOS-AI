import ctypes
import time
from PIL import ImageGrab
import pyautogui
from src.windows_integration.vision_automation import HumanCursorController

user32 = ctypes.windll.user32

cursor = HumanCursorController()

# Click Pencil at (325, 105)
print("Selecting Pencil at (325, 105)...")
cursor.move_smooth(325, 105, duration=1.0)
cursor.click_smooth(325, 105, duration=0.2)
time.sleep(0.3)

# Click Red color at (1085, 92)
print("Selecting Red color at (1085, 92)...")
cursor.move_smooth(1085, 92, duration=1.0)
cursor.click_smooth(1085, 92, duration=0.2)
time.sleep(0.3)

# Draw a red stroke on canvas from (960, 500) to (960, 650)
print("Drawing test stroke on canvas...")
cursor.move_smooth(960, 500, duration=0.8)
time.sleep(0.05)
user32.mouse_event(2, 0, 0, 0, 0)
time.sleep(0.01)
cursor.move_smooth(960, 650, duration=0.8)
time.sleep(0.01)
user32.mouse_event(4, 0, 0, 0, 0)
time.sleep(0.5)

img = ImageGrab.grab()
img.save("pencil_red_test.png")
print("Saved pencil_red_test.png")
