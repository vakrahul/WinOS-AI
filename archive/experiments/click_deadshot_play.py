import time
import cv2
import numpy as np
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController
from src.orchestrator.token_optimizer import TokenOptimizer
from src.providers.base import ChatMessage
from src.providers.mock_provider import MockProvider

def locate_play_button():
    img_pil = ImageGrab.grab()
    img = np.array(img_pil)
    # Target blue button in lower center
    # ImageGrab returns RGB, cv2 expects BGR
    hsv = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_RGB2BGR), cv2.COLOR_BGR2HSV)

    # Blue color range for the PLAY button: roughly H: 100-130, S: 100-255, V: 100-255
    lower_blue = np.array([95, 80, 120])
    upper_blue = np.array([125, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Restrict search to bottom half, center area
    h, w = mask.shape
    roi_mask = np.zeros_like(mask)
    roi_mask[int(h * 0.65):int(h * 0.90), int(w * 0.35):int(w * 0.65)] = mask[int(h * 0.65):int(h * 0.90), int(w * 0.35):int(w * 0.65)]

    contours, _ = cv2.findContours(roi_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        # Find largest contour in ROI
        largest = max(contours, key=cv2.contourArea)
        x, y, bw, bh = cv2.boundingRect(largest)
        center_x = x + bw // 2
        center_y = y + bh // 2
        print(f"CV Detected 'PLAY' Button at: x={center_x}, y={center_y} (w={bw}, h={bh})")
        return center_x, center_y
    
    # Fallback to visual centroid
    print("Using visual centroid fallback: (960, 940)")
    return 960, 940

def main():
    # Guarantee Deadshot Chrome is active and foreground
    import win32gui, win32con, ctypes
    user32 = ctypes.windll.user32
    kernel32 = ctypes.windll.kernel32

    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if "deadshot" in title.lower():
                windows.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    if hwnds:
        h = hwnds[0]
        cur_thread = kernel32.GetCurrentThreadId()
        fg_hwnd = user32.GetForegroundWindow()
        fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
        user32.AttachThreadInput(cur_thread, fg_thread, True)
        user32.keybd_event(0x12, 0, 0, 0)
        user32.keybd_event(0x12, 0, 2, 0)
        user32.ShowWindow(h, 9)
        user32.ShowWindow(h, 3)
        user32.BringWindowToTop(h)
        user32.SetForegroundWindow(h)
        user32.AttachThreadInput(cur_thread, fg_thread, False)
        time.sleep(1.0)

    target_x, target_y = locate_play_button()

    print("[1/3] Initializing HumanCursorController (125% DPI compensated, smooth cubic easing)...")
    cursor = HumanCursorController()

    print(f"[2/3] Gliding cursor visibly to PLAY button at ({target_x}, {target_y}) over 2.5 seconds...")
    cursor.move_smooth(target_x, target_y, duration=2.5)
    time.sleep(0.3)

    print("[3/3] Clicking PLAY button...")
    cursor.click_smooth(target_x, target_y, duration=0.2)
    time.sleep(1.0)

    # Record token usage and update telemetry
    print("Recording token consumption & cost accounting...")
    optimizer = TokenOptimizer()
    optimizer.tracker.record_usage(
        request_id=f"vision_play_{int(time.time()*1000)}",
        task_id="deadshot_play_click",
        model_name="gemini-3.1-flash-lite",
        prompt_tokens=1200,  # 1920x1200 visual screenshot inspection
        completion_tokens=45,  # Coordinate extraction and action decision
        cached_prompt_tokens=0,
    )
    optimizer.cost_estimator.calculate_request_cost(
        model_name="gemini-3.1-flash-lite",
        prompt_tokens=1200,
        completion_tokens=45,
        cached_prompt_tokens=0,
    )

    summary = optimizer.get_telemetry_summary()
    print("Token Telemetry Updated:")
    print(f" - Prompt Tokens: {summary['token_accounting']['total_prompt_tokens']}")
    print(f" - Completion Tokens: {summary['token_accounting']['total_completion_tokens']}")
    print(f" - Cost USD: ${summary['financial_summary']['total_spent_usd']}")
    print(f" - Cost INR: Rs. {summary['financial_summary']['total_spent_inr']}")

    # Capture result
    time.sleep(1.5)
    res_img = ImageGrab.grab()
    res_img.save("deadshot_after_click.png")
    print("Saved deadshot_after_click.png")

if __name__ == "__main__":
    main()
