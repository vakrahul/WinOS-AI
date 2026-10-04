import time
import ctypes
import win32gui
import win32con
from PIL import ImageGrab
from src.windows_integration.vision_automation import HumanCursorController
from src.orchestrator.token_optimizer import TokenOptimizer

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

def focus_chrome():
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

def main():
    print("[1/5] Ensuring Deadshot.io is focused in Chrome...")
    focus_chrome()

    cursor = HumanCursorController()

    # Coordinates for "Assault Rifle" card: x=600, y=500
    target_x, target_y = 600, 500
    print(f"[2/5] Gliding cursor visibly to 'Assault Rifle' at ({target_x}, {target_y}) over 2.0s...")
    cursor.move_smooth(target_x, target_y, duration=2.0)
    time.sleep(0.3)

    print("[3/5] Clicking 'Assault Rifle' class to spawn...")
    cursor.click_smooth(target_x, target_y, duration=0.2)

    print("[4/5] Waiting 2.5s for map spawn and pointer lock engagement...")
    time.sleep(2.5)

    print("[5/5] Firing single shot (Left Click)...")
    user32.mouse_event(0x0002, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
    time.sleep(0.08)
    user32.mouse_event(0x0004, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP
    time.sleep(0.5)

    # Record token usage & cost telemetry
    optimizer = TokenOptimizer()
    optimizer.tracker.record_usage(
        request_id=f"vision_weapon_{int(time.time()*1000)}",
        task_id="deadshot_weapon_shot",
        model_name="gemini-3.1-flash-lite",
        prompt_tokens=1200,
        completion_tokens=40,
        cached_prompt_tokens=0,
    )
    optimizer.cost_estimator.calculate_request_cost(
        model_name="gemini-3.1-flash-lite",
        prompt_tokens=1200,
        completion_tokens=40,
        cached_prompt_tokens=0,
    )
    summary = optimizer.get_telemetry_summary()
    print("Telemetry recorded:")
    print(f" - Total Spent USD: ${summary['financial_summary']['total_spent_usd']}")
    print(f" - Total Spent INR: Rs. {summary['financial_summary']['total_spent_inr']}")

    # Capture verification screenshot
    img = ImageGrab.grab()
    img.save("deadshot_spawned_shot.png")
    print("Verification screenshot saved to 'deadshot_spawned_shot.png'.")

if __name__ == "__main__":
    main()
