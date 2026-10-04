import time
import pyautogui
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

cursor = HumanCursorController()
print("Gliding cursor to Chrome taskbar icon (522, 1180) over 2.0s...")
cursor.move_smooth(522, 1180, duration=2.0)
time.sleep(0.3)
print("Clicking Chrome taskbar icon...")
cursor.click_smooth(522, 1180, duration=0.2)
time.sleep(2.0)

img = ImageGrab.grab()
img.save("chrome_taskbar_clicked.png")
print("Saved chrome_taskbar_clicked.png")
