"""Reads the first tweet from your existing, logged-in Google Chrome window and analyzes it with Gemini 3.1 Flash-Lite."""
import asyncio
import ctypes
from pathlib import Path
import subprocess
import time

from src.providers.base import ChatMessage
from src.providers.gemini_adapter import GeminiAdapter
from src.storage.credential_vault import CredentialVault

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# 64-bit Win32 API definitions
user32.GetClipboardData.restype = ctypes.c_void_p
user32.GetClipboardData.argtypes = [ctypes.c_uint]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]


def get_clipboard_text() -> str:
    CF_UNICODETEXT = 13
    if not user32.OpenClipboard(0):
        return ""
    try:
        h_clip = user32.GetClipboardData(CF_UNICODETEXT)
        if not h_clip:
            return ""
        ptr = kernel32.GlobalLock(h_clip)
        if not ptr:
            return ""
        text = ctypes.wstring_at(ptr)
        kernel32.GlobalUnlock(h_clip)
        return text
    finally:
        user32.CloseClipboard()


def get_chrome_hwnd() -> int:
    cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-Process chrome -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return int(res.stdout.strip())
    except Exception:
        return 0


def focus_window(hwnd: int):
    user32.keybd_event(0x12, 0, 0, 0)  # ALT down
    user32.ShowWindow(hwnd, 9)         # SW_RESTORE
    user32.SetForegroundWindow(hwnd)
    user32.keybd_event(0x12, 0, 2, 0)  # ALT up


async def main():
    print("=" * 65)
    print("   WINDOWS AI OPERATING ENVIRONMENT — ACTIVE BROWSER INSPECTION")
    print("   Target: Existing Logged-in Google Chrome (X / Twitter)")
    print("=" * 65)

    # 1. Bring Chrome into active tab with X home
    print("[1/3] Ensuring https://x.com/home is open in your existing Chrome...")
    subprocess.run(["cmd", "/c", "start", "chrome", "https://x.com/home"], shell=False)
    time.sleep(2.5)

    hwnd = get_chrome_hwnd()
    if not hwnd:
        print("[!] Could not obtain Chrome window handle.")
        return

    # 2. Focus and read content
    print(f"[2/3] Reading live feed from Chrome (Window Handle: {hwnd})...")
    focus_window(hwnd)
    time.sleep(1.0)

    VK_CONTROL = 0x11
    VK_A = 0x41
    VK_C = 0x43

    # Select All (Ctrl + A)
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_A, 0, 0, 0)
    time.sleep(0.1)
    user32.keybd_event(VK_A, 0, 2, 0)
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.4)

    # Copy (Ctrl + C)
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_C, 0, 0, 0)
    time.sleep(0.1)
    user32.keybd_event(VK_C, 0, 2, 0)
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.4)

    raw_text = get_clipboard_text()
    if not raw_text:
        print("[!] No text captured from browser.")
        return

    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]

    # Extract first post after timeline header
    author = "Unknown"
    handle = ""
    tweet_lines = []
    found_timeline = False

    for i, line in enumerate(lines):
        if "Your Home Timeline" in line or "For you" in line:
            found_timeline = True
            for j in range(i + 1, min(i + 25, len(lines))):
                curr = lines[j]
                if curr.startswith("@") and not handle:
                    handle = curr
                    author = lines[j - 1]
                    continue
                if handle and not any(k in curr for k in ["Kuberhunt", "@KuberHunt", "Ad", "Who to follow", "Follow"]):
                    if curr not in ["·", "1h", "2h", "3h", "4h", "5h", "now"]:
                        tweet_lines.append(curr)
                if len(tweet_lines) >= 3:
                    break
            if handle:
                break

    tweet_text = " ".join(tweet_lines).strip()

    print("\n" + "=" * 65)
    print("   FIRST TWEET DETECTED ON YOUR LIVE X FEED")
    print("=" * 65)
    print(f"Author: {author} ({handle})")
    print(f"Text:   {tweet_text}")

    # 3. Analyze with Gemini 3.1 Flash-Lite
    print("\n[3/3] Sending to Gemini 3.1 Flash-Lite for verification...")
    vault = CredentialVault()
    key = vault.get_credential("gemini")
    if key:
        gemini = GeminiAdapter(api_key=key, model_name="gemini-3.1-flash-lite")
        prompt = (
            f"The user's active Google Chrome browser was inspected on x.com. "
            f"Here is the first tweet seen on their feed:\n\n"
            f"Author: {author} ({handle})\n"
            f"Tweet: {tweet_text}\n\n"
            f"Please state clearly to the user what this tweet is about in 1-2 concise sentences."
        )
        resp = await gemini.complete([ChatMessage(role="user", content=prompt)])
        print("\nGemini 3.1 Flash-Lite:")
        print(resp.content)
    else:
        print("[!] Gemini API key not found in vault.")


if __name__ == "__main__":
    asyncio.run(main())
