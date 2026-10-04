import time
import pyautogui
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

def main():
    cursor = HumanCursorController()
    print("Scrolling down to center the Ezora SDE Intern post...")
    cursor.move_smooth(300, 500, duration=1.5)
    pyautogui.scroll(-400)
    time.sleep(2.0)

    # Move cursor over to where '... more' typically sits on that post
    img = ImageGrab.grab()
    img.save("ezora_post_centered.png")
    print("Saved ezora_post_centered.png")

if __name__ == "__main__":
    main()
