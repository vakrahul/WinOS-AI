import time
import pyautogui
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

def main():
    cursor = HumanCursorController()
    
    for i in range(1, 5):
        print(f"Gliding cursor and scrolling down (Scroll {i})...")
        cursor.move_smooth(300, 500, duration=1.5)
        pyautogui.scroll(-550)
        time.sleep(2.5)
        
        img = ImageGrab.grab()
        filename = f"feed_post_scroll_{i}.png"
        img.save(filename)
        print(f"Captured {filename}")

if __name__ == "__main__":
    main()
