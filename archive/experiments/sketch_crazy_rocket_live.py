"""Draws a crazy point-to-point sketch of an aerodynamic rocket directly in MS Paint.

Shows the mouse cursor holding down left-click and gliding smoothly across
each curve, fin, porthole, engine bell, and flame tongue.
"""

import ctypes
import math
import subprocess
import time
from PIL import ImageGrab
import pyautogui
import win32con
import win32gui

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


def force_paint_foreground(hwnd):
    cur_thread = kernel32.GetCurrentThreadId()
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    user32.AttachThreadInput(cur_thread, fg_thread, True)
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    user32.ShowWindow(hwnd, win32con.SW_RESTORE)
    user32.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)
    time.sleep(1.0)


def get_paint_hwnd() -> int:
    cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-Process mspaint -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return int(res.stdout.strip())
    except Exception:
        return 0


def move_to(x, y):
    user32.SetCursorPos(int(x), int(y))


def mouse_down():
    user32.mouse_event(2, 0, 0, 0, 0)  # Left down
    time.sleep(0.008)


def mouse_up():
    user32.mouse_event(4, 0, 0, 0, 0)  # Left up
    time.sleep(0.012)


def draw_natural_stroke(points, step_size=3, delay=0.005):
    """Visible point-to-point drawing holding left-click with smooth human-speed gliding."""
    if not points:
        return
    move_to(points[0][0], points[0][1])
    time.sleep(0.02)
    mouse_down()

    for i in range(1, len(points)):
        x0, y0 = points[i - 1]
        x1, y1 = points[i]
        dist = math.hypot(x1 - x0, y1 - y0)
        steps = max(1, int(dist / step_size))
        for s in range(1, steps + 1):
            t = s / steps
            cx = x0 + (x1 - x0) * t
            cy = y0 + (y1 - y0) * t
            move_to(cx, cy)
            time.sleep(delay)

    mouse_up()
    time.sleep(0.03)


def draw_bezier_curve(p0, p1, p2, num_points=35):
    """Draw smooth quadratic Bezier curve for aerodynamic contours."""
    pts = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    draw_natural_stroke(pts)


def draw_cubic_bezier(p0, p1, p2, p3, num_points=40):
    """Draw smooth cubic Bezier curve for organic curves like flames and fins."""
    pts = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (
            (1 - t) ** 3 * p0[0]
            + 3 * (1 - t) ** 2 * t * p1[0]
            + 3 * (1 - t) * t ** 2 * p2[0]
            + t ** 3 * p3[0]
        )
        y = (
            (1 - t) ** 3 * p0[1]
            + 3 * (1 - t) ** 2 * t * p1[1]
            + 3 * (1 - t) * t ** 2 * p2[1]
            + t ** 3 * p3[1]
        )
        pts.append((x, y))
    draw_natural_stroke(pts)


def draw_natural_circle(cx, cy, radius, segments=45):
    pts = []
    for i in range(segments + 1):
        theta = (2 * math.pi * i) / segments
        x = cx + radius * math.cos(theta)
        y = cy + radius * math.sin(theta)
        pts.append((x, y))
    draw_natural_stroke(pts)


def draw_sparkle_star(cx, cy, r=18):
    draw_natural_stroke([(cx - r, cy), (cx + r, cy)])
    draw_natural_stroke([(cx, cy - r), (cx, cy + r)])
    dr = r * 0.45
    draw_natural_stroke([(cx - dr, cy - dr), (cx + dr, cy + dr)])
    draw_natural_stroke([(cx - dr, cy + dr), (cx + dr, cy - dr)])


def draw_saturn_planet(cx, cy, r=22):
    draw_natural_circle(cx, cy, r)
    ring_pts = []
    for i in range(36):
        theta = (2 * math.pi * i) / 35
        rx = cx + (r * 2.2) * math.cos(theta)
        ry = cy + (r * 0.55) * math.sin(theta)
        tilt_x = rx - (ry - cy) * 0.4
        tilt_y = ry + (rx - cx) * 0.2
        ring_pts.append((tilt_x, tilt_y))
    draw_natural_stroke(ring_pts)


def main():
    hwnd = get_paint_hwnd()
    if not hwnd:
        print("[*] Launching Microsoft Paint...")
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.5)
        hwnd = get_paint_hwnd()

    print(f"Bringing Paint (HWND: {hwnd}) to foreground...")
    force_paint_foreground(hwnd)
    time.sleep(1.0)

    # Clear canvas cleanly
    print("Clearing canvas with Ctrl+A, Delete...")
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.press("delete")
    time.sleep(0.5)

    # Canvas center origin on maximized screen
    cx = 760
    cy = 430

    print("Beginning visible point-to-point crazy rocket sketching...")

    # 1. Aerodynamic Curved Fuselage
    print(">> [1/8] Sketching aerodynamic curved hull...")
    draw_bezier_curve((cx, cy - 230), (cx - 75, cy - 80), (cx - 60, cy + 110))
    draw_bezier_curve((cx, cy - 230), (cx + 75, cy - 80), (cx + 60, cy + 110))
    draw_bezier_curve((cx - 60, cy + 110), (cx, cy + 125), (cx + 60, cy + 110))

    # 2. Nose Cone Separation Seam & Tip
    print(">> [2/8] Sketching nose cone seam & cockpit tip...")
    draw_bezier_curve((cx - 45, cy - 110), (cx, cy - 95), (cx + 45, cy - 110))
    draw_natural_stroke([(cx, cy - 230), (cx, cy - 100)])

    # 3. Dual Concentric Porthole Windows
    print(">> [3/8] Sketching dual concentric portholes and glass glints...")
    draw_natural_circle(cx, cy - 35, radius=28)
    draw_natural_circle(cx, cy - 35, radius=22)
    draw_natural_stroke([(cx - 12, cy - 45), (cx - 4, cy - 50)])
    draw_natural_stroke([(cx - 15, cy - 38), (cx - 12, cy - 42)])

    draw_natural_circle(cx, cy + 40, radius=24)
    draw_natural_circle(cx, cy + 40, radius=18)
    draw_natural_stroke([(cx - 10, cy + 32), (cx - 3, cy + 28)])

    # 4. Body Panel Seams & Staging Rings
    print(">> [4/8] Sketching body panel staging lines...")
    draw_bezier_curve((cx - 58, cy + 85), (cx, cy + 98), (cx + 58, cy + 85))
    draw_bezier_curve((cx - 54, cy + 30), (cx, cy + 40), (cx + 54, cy + 30))

    # 5. Swept-Back Aerodynamic Booster Fins
    print(">> [5/8] Sketching swept delta booster fins...")
    # Left Fin
    draw_cubic_bezier(
        (cx - 50, cy + 15),
        (cx - 110, cy + 60),
        (cx - 165, cy + 145),
        (cx - 145, cy + 175),
    )
    draw_cubic_bezier(
        (cx - 145, cy + 175),
        (cx - 105, cy + 150),
        (cx - 85, cy + 130),
        (cx - 55, cy + 115),
    )
    draw_natural_stroke([(cx - 50, cy + 40), (cx - 130, cy + 155)])

    # Right Fin
    draw_cubic_bezier(
        (cx + 50, cy + 15),
        (cx + 110, cy + 60),
        (cx + 165, cy + 145),
        (cx + 145, cy + 175),
    )
    draw_cubic_bezier(
        (cx + 145, cy + 175),
        (cx + 105, cy + 150),
        (cx + 85, cy + 130),
        (cx + 55, cy + 115),
    )
    draw_natural_stroke([(cx + 50, cy + 40), (cx + 130, cy + 155)])

    # Center Dorsal Fin
    draw_natural_stroke([(cx, cy + 85), (cx, cy + 125)])

    # 6. Rocket Engine Bell Nozzle
    print(">> [6/8] Sketching flared rocket engine bell nozzle...")
    draw_natural_stroke([(cx - 35, cy + 118), (cx - 48, cy + 148)])
    draw_natural_stroke([(cx + 35, cy + 118), (cx + 48, cy + 148)])
    draw_bezier_curve((cx - 48, cy + 148), (cx, cy + 158), (cx + 48, cy + 148))
    draw_bezier_curve((cx - 42, cy + 135), (cx, cy + 143), (cx + 42, cy + 135))

    # 7. Fiery Exhaust Flames & Plasma Tongues
    print(">> [7/8] Sketching multi-layered fiery plasma plumes...")
    draw_cubic_bezier(
        (cx - 42, cy + 150),
        (cx - 65, cy + 200),
        (cx - 45, cy + 235),
        (cx - 25, cy + 220),
    )
    draw_cubic_bezier(
        (cx - 25, cy + 220),
        (cx - 15, cy + 250),
        (cx, cy + 285),
        (cx, cy + 295),
    )
    draw_cubic_bezier(
        (cx, cy + 295),
        (cx + 15, cy + 250),
        (cx + 25, cy + 220),
        (cx + 25, cy + 220),
    )
    draw_cubic_bezier(
        (cx + 25, cy + 220),
        (cx + 45, cy + 235),
        (cx + 65, cy + 200),
        (cx + 42, cy + 150),
    )

    # Inner flame core
    draw_cubic_bezier(
        (cx - 24, cy + 152),
        (cx - 32, cy + 195),
        (cx - 15, cy + 230),
        (cx, cy + 245),
    )
    draw_cubic_bezier(
        (cx, cy + 245),
        (cx + 15, cy + 230),
        (cx + 32, cy + 195),
        (cx + 24, cy + 152),
    )
    draw_natural_stroke([(cx, cy + 155), (cx, cy + 265)])

    # 8. Billowing Launch Smoke Clouds & Cosmos
    print(">> [8/8] Sketching billowing smoke plumes, planets, and stars...")
    draw_bezier_curve((cx - 70, cy + 210), (cx - 120, cy + 230), (cx - 85, cy + 265))
    draw_bezier_curve((cx - 85, cy + 265), (cx - 110, cy + 300), (cx - 60, cy + 310))

    draw_bezier_curve((cx + 70, cy + 210), (cx + 120, cy + 230), (cx + 85, cy + 265))
    draw_bezier_curve((cx + 85, cy + 265), (cx + 110, cy + 300), (cx + 60, cy + 310))

    # Saturn Planet
    draw_saturn_planet(cx - 210, cy - 140, r=22)
    # Moon
    draw_natural_circle(cx + 210, cy - 150, radius=24)

    # Sparkling Stars
    draw_sparkle_star(cx - 120, cy - 190, r=16)
    draw_sparkle_star(cx + 130, cy - 180, r=18)
    draw_sparkle_star(cx - 200, cy + 20, r=14)
    draw_sparkle_star(cx + 210, cy + 40, r=15)
    draw_sparkle_star(cx - 160, cy + 180, r=16)
    draw_sparkle_star(cx + 170, cy + 190, r=15)

    print("\n[+] Point-to-point rocket sketch completed!")
    time.sleep(1.0)
    img = ImageGrab.grab()
    img.save("crazy_rocket_paint_live.png")
    print("Saved screenshot to 'crazy_rocket_paint_live.png'.")


if __name__ == "__main__":
    main()
