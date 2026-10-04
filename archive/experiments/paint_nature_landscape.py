"""Paints the lush nature landscape in MS Paint directly with genuine mouse brushwork.

Layers:
1. Sky & Billowing Clouds (Sky Blue & White)
2. Distant Snow-Capped Mountain Peak (Slate Gray & White)
3. Distant Forest Ridge (Dark Green)
4. Rolling Meadow & Grassy Hills (Lime Green & Emerald Green)
5. Tree Shadows across the field (Dark Green & Black)
6. Left Trees & Cypress Spires (Dark Green & Brown)
7. The Grand Foreground Oak Tree (Textured Bark & Multi-Tone Foliage)
8. Foreground Grass Blades & Wildflowers
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

# Verified maximized Paint color palette coordinates (1920x1200)
PALETTE = {
    # Row 1 (y=92)
    "BLACK": (980, 92),
    "DARK_GRAY": (1015, 92),
    "DARK_RED": (1050, 92),
    "RED": (1085, 92),
    "ORANGE": (1120, 92),
    "YELLOW": (1155, 92),
    "GREEN": (1190, 92),
    "CYAN": (1225, 92),
    "BLUE": (1260, 92),
    "PURPLE": (1295, 92),
    # Row 2 (y=122)
    "WHITE": (980, 122),
    "LIGHT_GRAY": (1015, 122),
    "BROWN": (1050, 122),
    "PINK": (1085, 122),
    "GOLD": (1120, 122),
    "LIGHT_YELLOW": (1155, 122),
    "LIME_GREEN": (1190, 122),
    "SKY_BLUE": (1225, 122),
    "STEEL_BLUE": (1260, 122),
    "LAVENDER": (1295, 122),
}

PENCIL_TOOL = (325, 105)
BRUSH_TOOL = (365, 105)


def force_foreground(hwnd):
    cur_thread = kernel32.GetCurrentThreadId()
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    user32.AttachThreadInput(cur_thread, fg_thread, True)
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
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
    time.sleep(0.005)


def mouse_up():
    user32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(0.008)


def select_color(name: str):
    coord = PALETTE.get(name)
    if not coord:
        return
    move_to(coord[0], coord[1])
    time.sleep(0.04)
    mouse_down()
    mouse_up()
    time.sleep(0.08)


def stroke(points, step=4, delay=0.001):
    if not points:
        return
    move_to(points[0][0], points[0][1])
    time.sleep(0.01)
    mouse_down()
    for i in range(1, len(points)):
        x0, y0 = points[i - 1]
        x1, y1 = points[i]
        d = math.hypot(x1 - x0, y1 - y0)
        steps = max(1, int(d / step))
        for s in range(1, steps + 1):
            t = s / steps
            move_to(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t)
            time.sleep(delay)
    mouse_up()


def bezier(p0, p1, p2, num=25, delay=0.001):
    pts = []
    for i in range(num + 1):
        t = i / num
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    stroke(pts, delay=delay)


def circle(cx, cy, r, segs=28):
    pts = []
    for i in range(segs + 1):
        theta = (2 * math.pi * i) / segs
        pts.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
    stroke(pts, delay=0.001)


def foliage_blob(cx, cy, rx, ry, color="GREEN", density=12):
    select_color(color)
    for i in range(density):
        ang = (2 * math.pi * i) / density
        rad_x = rx * (0.8 + 0.3 * math.sin(i * 3))
        rad_y = ry * (0.8 + 0.3 * math.cos(i * 2))
        px = cx + rad_x * math.cos(ang)
        py = cy + rad_y * math.sin(ang)
        circle(px, py, int(min(rx, ry) * 0.45), segs=16)


def main():
    hwnd = get_paint_hwnd()
    if not hwnd:
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.5)
        hwnd = get_paint_hwnd()

    force_foreground(hwnd)
    time.sleep(0.8)

    # Clear canvas cleanly
    pyautogui.press("escape")
    time.sleep(0.05)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.08)
    pyautogui.press("delete")
    time.sleep(0.2)
    pyautogui.press("escape")
    time.sleep(0.1)

    # Select Pencil Tool
    move_to(PENCIL_TOOL[0], PENCIL_TOOL[1])
    time.sleep(0.05)
    mouse_down()
    mouse_up()
    time.sleep(0.1)

    print("[1/8] Painting Sky & Clouds...")
    # 1. Sky Blue horizontal energetic brush strokes
    select_color("SKY_BLUE")
    for y in range(235, 460, 8):
        stroke([(160, y), (1750, y)], step=6, delay=0.0005)
    for y in range(240, 420, 14):
        select_color("CYAN")
        stroke([(200, y), (1700, y)], step=8, delay=0.0005)

    # Billowing White Clouds
    select_color("WHITE")
    cloud_centers = [
        (350, 270, 70, 35), (460, 285, 90, 45), (600, 290, 80, 40),
        (880, 300, 85, 40), (1020, 280, 100, 50), (1180, 290, 80, 40),
        (1400, 270, 90, 45), (1550, 285, 80, 38)
    ]
    for ccx, ccy, crx, cry in cloud_centers:
        for r in range(cry, 5, -8):
            circle(ccx, ccy, r, segs=20)
        # Highlight top rims
        bezier((ccx - crx, ccy), (ccx, ccy - cry), (ccx + crx, ccy), num=20)

    print("[2/8] Painting Distant Snow-Capped Mountain...")
    # Mountain base & slopes (Slate/Steel Blue)
    select_color("STEEL_BLUE")
    mtn_peak = (720, 390)
    mtn_left = (480, 520)
    mtn_right = (980, 520)

    # Fill mountain body
    for y in range(390, 520, 5):
        t = (y - 390) / (520 - 390)
        lx = int(mtn_peak[0] - (mtn_peak[0] - mtn_left[0]) * t)
        rx = int(mtn_peak[0] + (mtn_right[0] - mtn_peak[0]) * t)
        stroke([(lx, y), (rx, y)], step=5, delay=0.0005)

    # Mountain Outline
    select_color("DARK_GRAY")
    stroke([mtn_left, (560, 470), (640, 430), mtn_peak, (820, 440), (900, 480), mtn_right], step=4)

    # Snow Cap & Ridges in White
    select_color("WHITE")
    stroke([mtn_peak, (710, 420), (730, 440), (700, 460), (740, 480), (720, 500)], step=3)
    # Snow highlights
    for y in range(395, 450, 4):
        t = (y - 390) / (520 - 390)
        lx = int(mtn_peak[0] - (mtn_peak[0] - mtn_left[0]) * t * 0.7)
        rx = int(mtn_peak[0] + (mtn_right[0] - mtn_peak[0]) * t * 0.7)
        stroke([(lx, y), (rx, y)], step=4, delay=0.0005)

    print("[3/8] Painting Distant Forest Treeline...")
    select_color("GREEN")
    for x in range(160, 1750, 18):
        y_top = 505 + int(12 * math.sin(x * 0.03))
        stroke([(x, 525), (x, y_top)], step=3, delay=0.0005)
        circle(x, y_top, 10, segs=14)

    print("[4/8] Painting Rolling Grassy Meadow & Hill Slopes...")
    # Base Green Meadow
    select_color("GREEN")
    for y in range(525, 880, 8):
        stroke([(160, y), (1750, y)], step=8, delay=0.0005)

    # Vibrant Lime Green sunlit slopes (sweeping diagonally from right to left)
    select_color("LIME_GREEN")
    for y in range(530, 890, 6):
        # Rolling diagonal bands
        x_start = 160
        x_end = 1750
        bezier((x_start, y + 20), (900, y - 10), (x_end, y - 30), num=35, delay=0.0005)

    # Light Yellow-Green sunny highlights across the pasture
    select_color("LIGHT_YELLOW")
    for y in range(560, 850, 20):
        bezier((300, y + 10), (800, y), (1500, y - 25), num=25, delay=0.0005)

    # Textured grass grain strokes
    select_color("LIME_GREEN")
    for gy in range(540, 860, 15):
        for gx in range(180, 1720, 35):
            stroke([(gx, gy), (gx + 15, gy - 6)], step=3, delay=0.0005)

    print("[5/8] Painting Dramatic Tree Shadows across the Meadow...")
    # Long diagonal shadows stretching to the bottom-left
    select_color("BLACK")
    # Shadow of the big right tree
    shadow_base = (1240, 880)
    shadow_pts = [
        (1240, 860), (1050, 820), (850, 780), (600, 740), (450, 720),
        (350, 730), (500, 760), (750, 800), (1000, 850), (1200, 890)
    ]
    stroke(shadow_pts, step=4)
    # Fill shadow body with dense dark hatching
    for sy in range(730, 860, 6):
        sx0 = int(350 + (sy - 730) * 4.5)
        sx1 = int(500 + (sy - 730) * 5.2)
        stroke([(sx0, sy), (sx1, sy)], step=4, delay=0.0005)

    # Shadows of left trees
    for lx in [280, 420, 540]:
        stroke([(lx, 660), (lx - 120, 690), (lx - 220, 710)], step=3)
        stroke([(lx, 665), (lx - 110, 695), (lx - 200, 715)], step=3)

    print("[6/8] Painting Left Trees & Conical Cypress Spires...")
    # Distant mid-ground cypress trees
    select_color("GREEN")
    for cx_tree, cy_tree in [(400, 580), (520, 610), (1000, 540)]:
        # Cypress cone shape
        for h in range(0, 90, 4):
            w = int(h * 0.35)
            stroke([(cx_tree - w, cy_tree - h), (cx_tree + w, cy_tree - h)], step=3, delay=0.0005)
        # Cypress dark shading on left
        select_color("BLACK")
        stroke([(cx_tree, cy_tree), (cx_tree - 10, cy_tree - 45), (cx_tree, cy_tree - 90)], step=3)
        select_color("LIME_GREEN")
        # Sunlit highlights on right
        stroke([(cx_tree + 5, cy_tree - 10), (cx_tree + 15, cy_tree - 40), (cx_tree + 2, cy_tree - 85)], step=3)
        select_color("GREEN")

    # Left leafy tree
    select_color("BROWN")
    # Trunk
    stroke([(280, 660), (280, 520), (260, 480)], step=4)
    stroke([(290, 660), (290, 520), (310, 480)], step=4)
    select_color("BLACK")
    stroke([(285, 660), (285, 510)], step=3)
    # Foliage Canopy
    foliage_blob(275, 440, 75, 60, color="GREEN", density=16)
    foliage_blob(270, 430, 65, 50, color="LIME_GREEN", density=12)
    foliage_blob(260, 450, 55, 45, color="BLACK", density=10)

    print("[7/8] Painting The Grand Foreground Oak Tree (Center-Right)...")
    # Massive Rooted Trunk
    select_color("BLACK")
    # Trunk left contour
    stroke([(1200, 910), (1215, 850), (1230, 780), (1220, 700), (1180, 620), (1110, 560), (1040, 520)], step=3)
    # Trunk right contour
    stroke([(1350, 910), (1330, 850), (1305, 780), (1290, 700), (1310, 620), (1360, 550), (1420, 500)], step=3)
    # Main central branch split
    stroke([(1250, 660), (1245, 580), (1270, 530)], step=3)

    # Dense textured bark fill (Dark Brown & Black overlapping vertical ridges)
    select_color("BROWN")
    for tx in range(1220, 1340, 6):
        stroke([(tx, 905), (tx - 10, 830), (tx - 5, 750), (tx - 25, 670), (tx - 45, 590)], step=3, delay=0.0005)

    select_color("BLACK")
    for tx in range(1215, 1345, 8):
        stroke([(tx, 905), (tx - 8, 830), (tx - 2, 750), (tx - 22, 670)], step=3, delay=0.0005)

    # Giant Lush Canopy (Multi-layered: Dark Base -> Rich Green -> Golden Lime Crown)
    tree_cx = 1260
    tree_cy = 380

    # 1. Deep Shadow Layer
    select_color("BLACK")
    for off_x, off_y, r in [(-180, 40, 85), (-90, 60, 95), (0, 70, 100), (110, 50, 90), (210, 30, 80)]:
        circle(tree_cx + off_x, tree_cy + off_y, r, segs=22)
        for sub_r in range(r, 10, -12):
            circle(tree_cx + off_x, tree_cy + off_y, sub_r, segs=16)

    # 2. Main Body Emerald Green
    select_color("GREEN")
    for off_x, off_y, r in [(-220, 0, 90), (-120, -30, 110), (0, -40, 120), (130, -20, 105), (230, 10, 85)]:
        circle(tree_cx + off_x, tree_cy + off_y, r, segs=24)
        for sub_r in range(r, 10, -10):
            circle(tree_cx + off_x, tree_cy + off_y, sub_r, segs=18)

    # 3. Dense leaf clusters across the canopy
    for cy_leaf in range(260, 500, 22):
        for cx_leaf in range(950, 1550, 30):
            # Check if inside canopy ellipse
            dx = (cx_leaf - tree_cx) / 290.0
            dy = (cy_leaf - tree_cy) / 140.0
            if dx * dx + dy * dy <= 1.0:
                stroke([(cx_leaf, cy_leaf), (cx_leaf + 8, cy_leaf - 5), (cx_leaf + 16, cy_leaf)], step=2, delay=0.0005)

    # 4. Sun-kissed Lime Green Highlights on top canopy rims
    select_color("LIME_GREEN")
    for off_x, off_y, r in [(-190, -40, 75), (-90, -70, 85), (20, -80, 95), (120, -60, 80), (200, -30, 65)]:
        bezier(
            (tree_cx + off_x - r, tree_cy + off_y),
            (tree_cx + off_x, tree_cy + off_y - r),
            (tree_cx + off_x + r, tree_cy + off_y),
            num=20, delay=0.0005
        )
        for sub_r in range(r, 15, -12):
            circle(tree_cx + off_x, tree_cy + off_y, sub_r, segs=16)

    # Pale yellow leaf tips on the very crest
    select_color("LIGHT_YELLOW")
    for hx in range(1050, 1450, 35):
        stroke([(hx, 260 + int(20 * math.sin(hx * 0.05))), (hx + 12, 255)], step=2, delay=0.0005)

    print("[8/8] Painting Foreground Grass Tufts & Meadow Wildflowers...")
    # Foreground grass tufts (Dark Green & Black base)
    select_color("BLACK")
    for x in range(160, 1750, 12):
        stroke([(x, 920), (x - 6, 880 + int(15 * math.sin(x * 0.08)))], step=2, delay=0.0005)

    select_color("GREEN")
    for x in range(165, 1745, 8):
        stroke([(x, 920), (x + 8, 875 + int(18 * math.cos(x * 0.06)))], step=2, delay=0.0005)

    # Bright Lime Green upward blades
    select_color("LIME_GREEN")
    for x in range(170, 1740, 6):
        stroke([(x, 925), (x + 10, 870 + int(22 * math.sin(x * 0.04)))], step=2, delay=0.0005)

    # Sunlit blade highlights (White & Pale Yellow)
    select_color("WHITE")
    for x in range(180, 1720, 24):
        stroke([(x, 915), (x + 6, 880)], step=2, delay=0.0005)

    # Wildflowers scattered in the meadow (Yellow & Red specks)
    select_color("YELLOW")
    for fx, fy in [(620, 680), (660, 710), (740, 690), (820, 720), (910, 660), (1050, 690), (1120, 710), (1450, 740), (1520, 720)]:
        circle(fx, fy, 4, segs=10)
        circle(fx + 2, fy + 1, 2, segs=8)

    select_color("RED")
    for fx, fy in [(640, 700), (780, 715), (880, 680), (1080, 725), (1480, 730)]:
        circle(fx, fy, 3, segs=8)

    # Rest cursor peacefully at side
    move_to(1700, 300)
    time.sleep(1.0)

    # Save verification snapshot
    img = ImageGrab.grab()
    img.save("painted_nature_landscape.png")
    print("\n[SUCCESS] Authentic hand-drawn nature landscape completed in Paint!")
    print("Screenshot saved to 'painted_nature_landscape.png'.")


if __name__ == "__main__":
    main()
