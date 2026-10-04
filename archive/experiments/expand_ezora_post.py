import time
import pyautogui
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

def main():
    cursor = HumanCursorController()
    print("Gliding cursor slowly to '... more' button at (217, 492) over 2.5s...")
    cursor.move_smooth(217, 492, duration=2.5)
    time.sleep(0.3)
    print("Clicking '... more' to expand full job details...")
    cursor.click_smooth(217, 492, duration=0.2)
    time.sleep(1.5)

    img1 = ImageGrab.grab()
    img1.save("ezora_expanded_1.png")
    print("Saved ezora_expanded_1.png")

    print("Scrolling down slightly to read full application details...")
    cursor.move_smooth(300, 600, duration=1.5)
    pyautogui.scroll(-350)
    time.sleep(2.0)

    img2 = ImageGrab.grab()
    img2.save("ezora_expanded_2.png")
    print("Saved ezora_expanded_2.png")

if __name__ == "__main__":
    main()
