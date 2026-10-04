"""Direct point-to-point drawing of a colorful aerodynamic rocket in MS Paint.

Zero boxes, zero text tool, zero copy-paste.
100% direct strokes using the Pencil tool and color palette:
1. Pencil selection -> Black outlines (Hull, Fins, Nozzle, Portholes)
2. Red palette -> Nose cone
3. Orange palette -> Delta wings & outer flames
4. Yellow palette -> Inner plasma core
5. Cyan palette -> Viewport glints & cosmic stars
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


def force_foreground(hwnd):
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


def move_to(x, y):
    user32.SetCursorPos(int(x), int(y))


def mouse_down():
    user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.008)


def mouse_up():
    user32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(0.012)


def glide_to(x1, y1, duration=0.8):
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    x0, y0 = pt.x, pt.y

    steps = max(15, int(duration * 60))
    for s in range(1, steps + 1):
        t = s / steps
        ease = 3 * (t ** 2) - 2 * (t ** 3)
        cx = x0 + (x1 - x0) * ease
        cy = y0 + (y1 - y0) * ease
        move_to(cx, cy)
        time.sleep(duration / steps)


def click_at(x, y, duration=0.5):
    glide_to(x, y, duration=duration)
    time.sleep(0.08)
    mouse_down()
    mouse_up()
    time.sleep(0.15)


def draw_stroke(points, step_size=3, delay=0.005):
    if not points:
        return
    # Glide visibly to start point
    glide_to(points[0][0], points[0][1], duration=0.4)
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


def draw_bezier(p0, p1, p2, num_points=30):
    pts = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    draw_stroke(pts)


def draw_cubic(p0, p1, p2, p3, num_points=35):
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
    draw_stroke(pts)


def draw_circle(cx, cy, r, segments=40):
    pts = []
    for i in range(segments + 1):
        theta = (2 * math.pi * i) / segments
        pts.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
    draw_stroke(pts)


# Exact Coordinates in maximized MS Paint
PENCIL_TOOL = (325, 105)
PALETTE_BLACK = (980, 92)
PALETTE_RED = (1085, 92)
PALETTE_ORANGE = (1120, 92)
PALETTE_YELLOW = (1155, 92)
PALETTE_CYAN = (1225, 92)
PALETTE_PURPLE = (1295, 92)


def main():
    hwnd = get_paint_hwnd()
    if not hwnd:
        print("[*] Launching MS Paint...")
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.5)
        hwnd = get_paint_hwnd()

    print(f"[1] Bringing Paint (HWND: {hwnd}) to foreground...")
    force_foreground(hwnd)
    time.sleep(1.0)

    # Dismiss any active text box / selection box with Escape
    print("[2] Pressing Escape and clearing canvas cleanly...")
    pyautogui.press("escape")
    time.sleep(0.1)
    pyautogui.press("escape")
    time.sleep(0.1)

    # Select all and delete to guarantee blank white canvas
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyautogui.press("escape")
    time.sleep(0.2)

    # Click directly on the Pencil tool to guarantee NO text boxes!
    print("[3] Clicking PENCIL TOOL at (325, 105)...")
    click_at(PENCIL_TOOL[0], PENCIL_TOOL[1], duration=1.2)
    time.sleep(0.3)

    # Rocket Center on Canvas
    cx = 760
    cy = 450

    # =========================================================================
    # 1. BLACK OUTLINE: Hull, Fins, Nozzle, Portholes
    # =========================================================================
    print("[4] Selecting BLACK color at (980, 92)...")
    click_at(PALETTE_BLACK[0], PALETTE_BLACK[1], duration=1.2)
    time.sleep(0.3)

    print(">> Drawing structural rocket hull and delta wings in BLACK...")
    # Fuselage main contours
    draw_bezier((cx - 45, cy - 110), (cx - 75, cy - 30), (cx - 60, cy + 110))
    draw_bezier((cx + 45, cy - 110), (cx + 75, cy - 30), (cx + 60, cy + 110))
    draw_bezier((cx - 60, cy + 110), (cx, cy + 125), (cx + 60, cy + 110))

    # Staging seams
    draw_bezier((cx - 58, cy + 85), (cx, cy + 98), (cx + 58, cy + 85))
    draw_bezier((cx - 54, cy + 30), (cx, cy + 40), (cx + 54, cy + 30))

    # Left delta fin
    draw_cubic(
        (cx - 50, cy + 15),
        (cx - 110, cy + 60),
        (cx - 165, cy + 145),
        (cx - 145, cy + 175),
    )
    draw_cubic(
        (cx - 145, cy + 175),
        (cx - 105, cy + 150),
        (cx - 85, cy + 130),
        (cx - 55, cy + 115),
    )

    # Right delta fin
    draw_cubic(
        (cx + 50, cy + 15),
        (cx + 110, cy + 60),
        (cx + 165, cy + 145),
        (cx + 145, cy + 175),
    )
    draw_cubic(
        (cx + 145, cy + 175),
        (cx + 105, cy + 150),
        (cx + 85, cy + 130),
        (cx + 55, cy + 115),
    )

    # Engine Bell Nozzle
    draw_stroke([(cx - 35, cy + 118), (cx - 48, cy + 148)])
    draw_stroke([(cx + 35, cy + 118), (cx + 48, cy + 148)])
    draw_bezier((cx - 48, cy + 148), (cx, cy + 158), (cx + 48, cy + 148))

    # =========================================================================
    # 2. RED: Nose Cone & Aerodynamic Tip
    # =========================================================================
    print("[5] Selecting RED color at (1085, 92)...")
    click_at(PALETTE_RED[0], PALETTE_RED[1], duration=1.2)
    time.sleep(0.3)

    print(">> Drawing Aerodynamic Crimson Nose Cone in RED...")
    draw_bezier((cx, cy - 230), (cx - 30, cy - 160), (cx - 45, cy - 110))
    draw_bezier((cx, cy - 230), (cx + 30, cy - 160), (cx + 45, cy - 110))
    draw_bezier((cx - 45, cy - 110), (cx, cy - 95), (cx + 45, cy - 110))

    # Red inner color fill lines
    for h in range(-205, -115, 10):
        span = int((h + 230) * 0.40)
        draw_stroke([(cx - span, cy + h), (cx + span, cy + h)], delay=0.003)

    # =========================================================================
    # 3. ORANGE: Fin Fill Ribs & Outer Thrust Flames
    # =========================================================================
    print("[6] Selecting ORANGE color at (1120, 92)...")
    click_at(PALETTE_ORANGE[0], PALETTE_ORANGE[1], duration=1.2)
    time.sleep(0.3)

    print(">> Drawing Fin Internal Shading & Flame Plume in ORANGE...")
    # Left fin shading lines
    draw_stroke([(cx - 50, cy + 40), (cx - 130, cy + 155)])
    draw_stroke([(cx - 52, cy + 65), (cx - 120, cy + 155)])
    draw_stroke([(cx - 54, cy + 90), (cx - 100, cy + 145)])

    # Right fin shading lines
    draw_stroke([(cx + 50, cy + 40), (cx + 130, cy + 155)])
    draw_stroke([(cx + 52, cy + 65), (cx + 120, cy + 155)])
    draw_stroke([(cx + 54, cy + 90), (cx + 100, cy + 145)])

    # Outer fire tongues
    draw_cubic(
        (cx - 42, cy + 150),
        (cx - 65, cy + 200),
        (cx - 45, cy + 235),
        (cx - 25, cy + 220),
    )
    draw_cubic(
        (cx - 25, cy + 220),
        (cx - 15, cy + 250),
        (cx, cy + 285),
        (cx, cy + 295),
    )
    draw_cubic(
        (cx, cy + 295),
        (cx + 15, cy + 250),
        (cx + 25, cy + 220),
        (cx + 25, cy + 220),
    )
    draw_cubic(
        (cx + 25, cy + 220),
        (cx + 45, cy + 235),
        (cx + 65, cy + 200),
        (cx + 42, cy + 150),
    )

    # =========================================================================
    # 4. YELLOW: Inner Plasma Fire Core & Glowing Embers
    # =========================================================================
    print("[7] Selecting YELLOW color at (1155, 92)...")
    click_at(PALETTE_YELLOW[0], PALETTE_YELLOW[1], duration=1.2)
    time.sleep(0.3)

    print(">> Drawing Inner Plasma Core & Embers in YELLOW...")
    draw_cubic(
        (cx - 24, cy + 152),
        (cx - 32, cy + 195),
        (cx - 15, cy + 230),
        (cx, cy + 245),
    )
    draw_cubic(
        (cx, cy + 245),
        (cx + 15, cy + 230),
        (cx + 32, cy + 195),
        (cx + 24, cy + 152),
    )
    draw_stroke([(cx, cy + 155), (cx, cy + 265)])
    # Embers
    for ex, ey in [(cx - 25, cy + 270), (cx + 28, cy + 275), (cx - 10, cy + 310), (cx + 12, cy + 315), (cx, cy + 335)]:
        draw_circle(ex, ey, r=3)

    # =========================================================================
    # 5. CYAN: Dual Concentric Porthole Windows & Sparkling Stars
    # =========================================================================
    print("[8] Selecting CYAN color at (1225, 92)...")
    click_at(PALETTE_CYAN[0], PALETTE_CYAN[1], duration=1.2)
    time.sleep(0.3)

    print(">> Drawing Concentric Portholes & Stars in CYAN...")
    # Upper Porthole
    draw_circle(cx, cy - 35, r=24)
    draw_circle(cx, cy - 35, r=18)
    draw_stroke([(cx - 10, cy - 43), (cx - 3, cy - 48)])

    # Lower Porthole
    draw_circle(cx, cy + 40, r=20)
    draw_circle(cx, cy + 40, r=14)
    draw_stroke([(cx - 8, cy + 32), (cx - 2, cy + 28)])

    # 4-pointed cyan stars
    for sx, sy in [(cx - 120, cy - 190), (cx + 130, cy - 180), (cx - 200, cy + 20), (cx + 210, cy + 40), (cx - 160, cy + 180), (cx + 170, cy + 190)]:
        draw_stroke([(sx - 14, sy), (sx + 14, sy)])
        draw_stroke([(sx, sy - 14), (sx, sy + 14)])

    # Move cursor peacefully away to rest position
    glide_to(cx + 400, cy, duration=1.0)
    time.sleep(1.0)

    # Save screenshot
    img = ImageGrab.grab()
    img.save("direct_rocket_paint_drawn.png")
    print("\n[SUCCESS] Direct colorful rocket drawing complete in Paint!")
    print("Screenshot saved to 'direct_rocket_paint_drawn.png'.")


if __name__ == "__main__":
    main()
