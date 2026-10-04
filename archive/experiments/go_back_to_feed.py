import time
import pyautogui
from PIL import ImageGrab

print("Pressing Alt + Left Arrow to go back to search feed...")
pyautogui.hotkey("alt", "left")
time.sleep(3.5)

img = ImageGrab.grab()
img.save("returned_to_feed.png")
print("Saved returned_to_feed.png")
