import time
import pyautogui
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController

def main():
    cursor = HumanCursorController()
    
    # LinkedIn in-app search bar is at (240, 155)
    print("Gliding cursor to LinkedIn in-app search bar at (240, 155)...")
    cursor.move_smooth(240, 155, duration=2.5)
    time.sleep(0.3)
    cursor.click_smooth(240, 155, duration=0.2)
    time.sleep(0.4)

    # Select all and type new search
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.2)
    query = '"SDE intern" "send resume"'
    print(f"Typing in LinkedIn search: {query}...")
    pyautogui.write(query, interval=0.02)
    time.sleep(0.4)
    pyautogui.press("enter")
    print("Waiting 6.0s for feed to load...")
    time.sleep(6.0)

    # Click Posts filter (at 125, 218)
    img = ImageGrab.grab()
    img.save("linkedin_send_resume_search.png")
    print("Saved linkedin_send_resume_search.png")

if __name__ == "__main__":
    main()
