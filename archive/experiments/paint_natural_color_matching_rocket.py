"""Visible Color-Matching Rocket Painting in MS Paint.

Shows the mouse cursor naturally gliding between the Color Palette
and the canvas, switching colors point-by-point:
1. Palette -> Red (1085, 92) -> Draws Crimson Nose Cone
2. Palette -> Orange (1120, 92) -> Draws Swept Delta Booster Wings
3. Palette -> Yellow (1155, 92) -> Draws Inner Plasma Flame Tongues
4. Palette -> Cyan (1225, 92) -> Draws Dual Portholes & Sparkling Stars
5. Palette -> Black (980, 92) -> Draws Structural Hull Seams, Nozzle & Embers
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
    user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.008)


def mouse_up():
    user32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(0.012)


def glide_cursor(x0, y0, x1, y1, duration=1.5):
    """Slow, smooth cubic easing glide so user sees cursor movement clearly."""
    steps = max(20, int(duration * 60))
    for s in range(1, steps + 1):
        t = s / steps
        ease_t = 3 * (t ** 2) - 2 * (t ** 3)
        cx = x0 + (x1 - x0) * ease_t
        cy = y0 + (y1 - y0) * ease_t
        move_to(cx, cy)
        time.sleep(duration / steps)


def get_pos():
    class POINT(ctypes.Structure):
        _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y


def select_color(color_name: str, palette_x: int, palette_y: int):
    """Visibly glides cursor up to the color palette and selects a color."""
    cur_x, cur_y = get_pos()
    print(f"\n[COLOR PALETTE] Gliding up to select {color_name} at ({palette_x}, {palette_y})...")
    glide_cursor(cur_x, cur_y, palette_x, palette_y, duration=1.5)
    time.sleep(0.2)
    # Click color circle
    mouse_down()
    mouse_up()
    time.sleep(0.3)
    print(f"               Selected {color_name}!")


def draw_natural_stroke(points, step_size=3, delay=0.006):
    if not points:
        return
    cur_x, cur_y = get_pos()
    # Glide smoothly to start point
    glide_cursor(cur_x, cur_y, points[0][0], points[0][1], duration=0.8)
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
    time.sleep(0.04)


def draw_bezier_curve(p0, p1, p2, num_points=35):
    pts = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    draw_natural_stroke(pts)


def draw_cubic_bezier(p0, p1, p2, p3, num_points=40):
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


def draw_circle(cx, cy, radius, segments=45):
    pts = []
    for i in range(segments + 1):
        theta = (2 * math.pi * i) / segments
        x = cx + radius * math.cos(theta)
        y = cy + radius * math.sin(theta)
        pts.append((x, y))
    draw_natural_stroke(pts)


def draw_star(cx, cy, r=16):
    draw_natural_stroke([(cx - r, cy), (cx + r, cy)])
    draw_natural_stroke([(cx, cy - r), (cx, cy + r)])
    dr = r * 0.45
    draw_natural_stroke([(cx - dr, cy - dr), (cx + dr, cy + dr)])
    draw_natural_stroke([(cx - dr, cy + dr), (cx + dr, cy - dr)])


# Paint Toolbar Palette Coordinates (on maximized 1920x1200)
PALETTE = {
    "BLACK": (980, 92),
    "RED": (1085, 92),
    "ORANGE": (1120, 92),
    "YELLOW": (1155, 92),
    "CYAN": (1225, 92),
    "BLUE": (1260, 92),
    "PURPLE": (1295, 92),
    "BRUSH_TOOL": (410, 95),
}


def main():
    hwnd = get_paint_hwnd()
    if not hwnd:
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.5)
        hwnd = get_paint_hwnd()

    force_paint_foreground(hwnd)
    time.sleep(1.0)

    # Clean canvas
    print("Clearing canvas...")
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.press("delete")
    time.sleep(0.4)

    # Center origin of rocket on canvas
    cx = 760
    cy = 430

    # Ensure Brush tool is active
    select_color("BRUSH TOOL", PALETTE["BRUSH_TOOL"][0], PALETTE["BRUSH_TOOL"][1])

    # -------------------------------------------------------------
    # 1. RED COLOR -> Nose Cone & Thermal Tip
    # -------------------------------------------------------------
    select_color("CRIMSON RED", PALETTE["RED"][0], PALETTE["RED"][1])
    print(">> Drawing Aerodynamic Crimson Nose Cone in RED...")
    # Nose cone triangle / curves
    draw_bezier_curve((cx, cy - 230), (cx - 30, cy - 160), (cx - 45, cy - 110))
    draw_bezier_curve((cx, cy - 230), (cx + 30, cy - 160), (cx + 45, cy - 110))
    draw_bezier_curve((cx - 45, cy - 110), (cx, cy - 95), (cx + 45, cy - 110))
    # Red fill hatching lines inside nose cone
    for h_offset in range(-200, -115, 12):
        span = int((h_offset + 230) * 0.40)
        draw_natural_stroke([(cx - span, cy + h_offset), (cx + span, cy + h_offset)], delay=0.004)

    # -------------------------------------------------------------
    # 2. ORANGE COLOR -> Swept Delta Booster Wings & Outer Flames
    # -------------------------------------------------------------
    select_color("VIBRANT ORANGE", PALETTE["ORANGE"][0], PALETTE["ORANGE"][1])
    print(">> Drawing Aerodynamic Delta Booster Wings in ORANGE...")
    # Left Fin Outline & Ribs
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
    draw_natural_stroke([(cx - 52, cy + 70), (cx - 115, cy + 150)])

    # Right Fin Outline & Ribs
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
    draw_natural_stroke([(cx + 52, cy + 70), (cx + 115, cy + 150)])

    # Outer Thruster Flame Plume
    print(">> Drawing Outer Thruster Flames in ORANGE...")
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

    # -------------------------------------------------------------
    # 3. YELLOW COLOR -> Intense Plasma Core & Glowing Flame Tongues
    # -------------------------------------------------------------
    select_color("INTENSE YELLOW", PALETTE["YELLOW"][0], PALETTE["YELLOW"][1])
    print(">> Drawing Inner Glowing Flame Core in YELLOW...")
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
    # Yellow Embers
    for ex, ey in [(cx - 30, cy + 270), (cx + 35, cy + 275), (cx - 12, cy + 315), (cx + 14, cy + 320), (cx, cy + 340)]:
        draw_circle(ex, ey, radius=4)

    # -------------------------------------------------------------
    # 4. CYAN COLOR -> Cockpit Porthole Windows & Sparkling Stars
    # -------------------------------------------------------------
    select_color("CYAN / LIGHT BLUE", PALETTE["CYAN"][0], PALETTE["CYAN"][1])
    print(">> Drawing Cockpit Porthole Glass & Stars in CYAN...")
    # Upper Porthole Viewport
    draw_circle(cx, cy - 35, radius=24)
    draw_circle(cx, cy - 35, radius=18)
    draw_natural_stroke([(cx - 10, cy - 43), (cx - 3, cy - 48)])

    # Lower Porthole Viewport
    draw_circle(cx, cy + 40, radius=20)
    draw_circle(cx, cy + 40, radius=14)
    draw_natural_stroke([(cx - 8, cy + 32), (cx - 2, cy + 28)])

    # Sparkling Stars around the rocket
    draw_star(cx - 120, cy - 190, r=16)
    draw_star(cx + 130, cy - 180, r=18)
    draw_star(cx - 200, cy + 20, r=14)
    draw_star(cx + 210, cy + 40, r=15)
    draw_star(cx - 160, cy + 180, r=16)
    draw_star(cx + 170, cy + 190, r=15)

    # -------------------------------------------------------------
    # 5. PURPLE COLOR -> Celestial Orbiting Saturn
    # -------------------------------------------------------------
    select_color("COSMIC PURPLE", PALETTE["PURPLE"][0], PALETTE["PURPLE"][1])
    print(">> Drawing Celestial Planet Saturn in PURPLE...")
    draw_circle(cx - 210, cy - 140, radius=22)
    # Ring
    ring_pts = []
    for i in range(36):
        theta = (2 * math.pi * i) / 35
        rx = (cx - 210) + 45 * math.cos(theta)
        ry = (cy - 140) + 12 * math.sin(theta)
        ring_pts.append((rx, ry))
    draw_natural_stroke(ring_pts)

    # -------------------------------------------------------------
    # 6. BLACK COLOR -> Structural Hull Outlines, Staging Seams & Engine Nozzle
    # -------------------------------------------------------------
    select_color("DEEP BLACK", PALETTE["BLACK"][0], PALETTE["BLACK"][1])
    print(">> Drawing Bold Structural Hull Outlines & Nozzle in BLACK...")
    # Main Fuselage Hull Walls
    draw_bezier_curve((cx - 45, cy - 110), (cx - 75, cy - 30), (cx - 60, cy + 110))
    draw_bezier_curve((cx + 45, cy - 110), (cx + 75, cy - 30), (cx + 60, cy + 110))
    draw_bezier_curve((cx - 60, cy + 110), (cx, cy + 125), (cx + 60, cy + 110))

    # Panel Staging Seams
    draw_bezier_curve((cx - 58, cy + 85), (cx, cy + 98), (cx + 58, cy + 85))
    draw_bezier_curve((cx - 54, cy + 30), (cx, cy + 40), (cx + 54, cy + 30))

    # Engine Bell Nozzle
    draw_natural_stroke([(cx - 35, cy + 118), (cx - 48, cy + 148)])
    draw_natural_stroke([(cx + 35, cy + 118), (cx + 48, cy + 148)])
    draw_bezier_curve((cx - 48, cy + 148), (cx, cy + 158), (cx + 48, cy + 148))
    draw_bezier_curve((cx - 42, cy + 135), (cx, cy + 143), (cx + 42, cy + 135))

    # Moon Outline
    draw_circle(cx + 210, cy - 150, radius=24)

    print("\n[SUCCESS] Natural color-matching rocket artwork completed in Paint!")
    time.sleep(1.0)
    img = ImageGrab.grab()
    img.save("paint_color_matched_artwork.png")
    print("Saved screenshot to 'paint_color_matched_artwork.png'.")


if __name__ == "__main__":
    main()
