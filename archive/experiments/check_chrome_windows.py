import win32gui
import win32con
import pyautogui
import time

pyautogui.press("esc")
time.sleep(0.5)

def callback(hwnd, extra):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:
            extra.append((hwnd, title, win32gui.GetWindowPlacement(hwnd)))
    return True

windows = []
win32gui.EnumWindows(callback, windows)
for h, t, p in windows:
    if "chrome" in t.lower() or "google" in t.lower() or "linkedin" in t.lower():
        print(f"HWND: {h} | Title: '{t}' | Placement: {p}")
