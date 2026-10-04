import base64
import ctypes
import json
import time
from pathlib import Path
from PIL import ImageGrab
import httpx
from src.storage.credential_vault import CredentialVault

user32 = ctypes.windll.user32

def find_chrome_hwnd():
    hwnd = 0
    def check_win(h, _):
        nonlocal hwnd
        if user32.IsWindowVisible(h):
            length = user32.GetWindowTextLengthW(h)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(h, buff, length + 1)
                if "Google Chrome" in buff.value:
                    hwnd = h
                    return False
        return True

    CMPFUNC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(CMPFUNC(check_win), 0)
    return hwnd

hwnd = find_chrome_hwnd()
print("Found Chrome HWND:", hwnd)
if not hwnd:
    print("Chrome not running.")
    exit(1)

# Bring Chrome to the top and maximize
user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
user32.BringWindowToTop(hwnd)
user32.SetForegroundWindow(hwnd)
time.sleep(1.0)

# Capture screen now that Chrome is visible on top
img = ImageGrab.grab()
img.save("chrome_top_screen.png")
print("Captured Chrome screen to chrome_top_screen.png")

# Send to Gemini 3.1 Flash-Lite Vision
v = CredentialVault()
key = v.get_credential("gemini")

with open("chrome_top_screen.png", "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode("utf-8")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={key}"

payload = {
    "contents": [{
        "role": "user",
        "parts": [
            {
                "text": (
                    "Look at this screenshot of the user's active Google Chrome browser on X (Twitter). "
                    "Identify the first tweet visible in the feed. "
                    "Report: "
                    "1. Author Name "
                    "2. Handle (@...) "
                    "3. Time posted "
                    "4. Full text of the tweet "
                    "5. A concise 1-sentence summary."
                )
            },
            {"inline_data": {"mime_type": "image/png", "data": img_b64}}
        ]
    }]
}

print("Sending screenshot to Gemini 3.1 Flash-Lite...")
res = httpx.post(url, json=payload, timeout=30.0)
if res.status_code == 200:
    text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    Path("gemini_vision_output.txt").write_text(text, encoding="utf-8")
    print("Saved to gemini_vision_output.txt successfully.")
else:
    print("Error:", res.status_code, res.text)
