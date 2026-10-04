"""Accurately reads the visible X (Twitter) feed from your active Chrome window using Gemini 3.1 Flash-Lite Vision."""
import asyncio
import base64
import ctypes
import json
from pathlib import Path
import time

from PIL import ImageGrab
import httpx
from src.storage.credential_vault import CredentialVault

user32 = ctypes.windll.user32


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


def find_chrome_window():
    found_hwnd = 0

    def check_win(hwnd, _):
        nonlocal found_hwnd
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buff, length + 1)
                if "Google Chrome" in buff.value:
                    found_hwnd = hwnd
                    return False
        return True

    CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(CMPFUNC(check_win), 0)
    return found_hwnd


def focus_window(hwnd: int):
    user32.keybd_event(0x12, 0, 0, 0)  # ALT down
    user32.ShowWindow(hwnd, 9)         # SW_RESTORE
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.keybd_event(0x12, 0, 2, 0)  # ALT up


async def main():
    print("=" * 65)
    print("   WINDOWS AI OPERATING ENVIRONMENT — VISUAL BROWSER INSPECTION")
    print("   Target: Active Logged-in Google Chrome (X / Twitter)")
    print("=" * 65)

    hwnd = find_chrome_window()
    if not hwnd:
        print("[!] No active Google Chrome window found.")
        return

    print(f"[1/3] Bringing your Chrome window (HWND: {hwnd}) to foreground...")
    focus_window(hwnd)
    time.sleep(1.0)

    # Capture window bounds or full screen
    rect = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))

    print("[2/3] Capturing high-resolution visual snapshot of your active Chrome window...")
    # Grab the window region
    if rect.right > rect.left and rect.bottom > rect.top:
        bbox = (max(0, rect.left), max(0, rect.top), rect.right, rect.bottom)
        screenshot = ImageGrab.grab(bbox=bbox)
    else:
        screenshot = ImageGrab.grab()

    screenshot_path = Path("active_x_feed.png")
    screenshot.save(screenshot_path)
    print(f"      Snapshot saved to {screenshot_path.name}")

    # Step 3: Run through Gemini 3.1 Flash-Lite Multimodal Vision
    print("\n[3/3] Inspecting feed with Gemini 3.1 Flash-Lite Vision...")
    vault = CredentialVault()
    key = vault.get_credential("gemini")
    if not key:
        print("[!] Gemini API key not found in vault.")
        return

    img_b64 = base64.b64encode(screenshot_path.read_bytes()).decode("utf-8")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={key}"

    prompt = (
        "Examine this screenshot of Google Chrome showing the X (Twitter) timeline. "
        "Locate the very first post/tweet in the main feed column under 'What's happening?'. "
        "Extract and report: "
        "\n1. Author / Account Name "
        "\n2. Handle (@username) "
        "\n3. Timestamp (e.g. 18m, 1h) "
        "\n4. Exact Tweet Text "
        "\n5. Attached Media/Image Description (if any) "
        "\n6. Concise 1-sentence summary of the post."
    )

    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/png", "data": img_b64}},
            ],
        }]
    }

    async with httpx.AsyncClient(timeout=40.0) as client:
        res = await client.post(url, json=payload)
        if res.status_code == 200:
            content = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            print("\n" + "=" * 65)
            print("   DETECTION REPORT FROM GEMINI 3.1 FLASH-LITE")
            print("=" * 65)
            # Write to file to ensure clean UTF-8 rendering
            Path("detected_tweet_report.txt").write_text(content, encoding="utf-8")
            # Print with ASCII-safe replacement for standard Windows cmd
            safe_content = content.encode("ascii", "replace").decode("ascii")
            print(safe_content)
            print("\n[+] Full report saved to 'detected_tweet_report.txt' (UTF-8).")
        else:
            print("[!] API Error:", res.status_code, res.text)


if __name__ == "__main__":
    asyncio.run(main())
