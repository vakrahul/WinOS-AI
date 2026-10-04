import ctypes
import math
import time

user32 = ctypes.windll.user32

def mouse_down():
    user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.005)

def mouse_up():
    user32.mouse_event(4, 0, 0, 0, 0)
    time.sleep(0.008)

def move_to(x, y):
    user32.SetCursorPos(int(x), int(y))

def draw_natural_stroke(points, step_size=2, delay=0.003):
    """Draw a natural, continuous mouse stroke through key coordinate points."""
    if not points:
        return
    move_to(points[0][0], points[0][1])
    time.sleep(0.01)
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

def draw_bezier_curve(p0, p1, p2, num_points=35):
    """Draw smooth quadratic Bezier curve for aerodynamic contours."""
    pts = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
        y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]
        pts.append((x, y))
    draw_natural_stroke(pts)

def draw_cubic_bezier(p0, p1, p2, p3, num_points=40):
    """Draw smooth cubic Bezier curve for organic curves like flames and fins."""
    pts = []
    for i in range(num_points + 1):
        t = i / num_points
        x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
        y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
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
    # Cross
    draw_natural_stroke([(cx - r, cy), (cx + r, cy)])
    draw_natural_stroke([(cx, cy - r), (cx, cy + r)])
    # Diagonals
    dr = r * 0.45
    draw_natural_stroke([(cx - dr, cy - dr), (cx + dr, cy + dr)])
    draw_natural_stroke([(cx - dr, cy + dr), (cx + dr, cy - dr)])

def draw_saturn_planet(cx, cy, r=22):
    # Planet body
    draw_natural_circle(cx, cy, r)
    # Planetary ring ellipse
    ring_pts = []
    for i in range(36):
        theta = (2 * math.pi * i) / 35
        rx = cx + (r * 2.2) * math.cos(theta)
        ry = cy + (r * 0.55) * math.sin(theta)
        # tilt
        tilt_x = rx - (ry - cy) * 0.4
        tilt_y = ry + (rx - cx) * 0.2
        ring_pts.append((tilt_x, tilt_y))
    draw_natural_stroke(ring_pts)

def get_paint_hwnd() -> int:
    import subprocess
    cmd = ["powershell", "-NoProfile", "-Command", "(Get-Process mspaint -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return int(res.stdout.strip())
    except Exception:
        return 0

def main():
    hwnd = get_paint_hwnd()
    if not hwnd:
        print("[!] Paint not running.")
        return

    print(f"Bringing Paint (HWND: {hwnd}) to foreground...")
    user32.keybd_event(0x12, 0, 0, 0)
    user32.ShowWindow(hwnd, 3) # Maximize
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.keybd_event(0x12, 0, 2, 0)
    time.sleep(1.0)

    # Clear previous canvas
    print("Clearing canvas for fresh natural artwork...")
    VK_CONTROL = 0x11
    VK_A = 0x41
    VK_DELETE = 0x2E
    user32.keybd_event(VK_CONTROL, 0, 0, 0)
    user32.keybd_event(VK_A, 0, 0, 0)
    time.sleep(0.08)
    user32.keybd_event(VK_A, 0, 2, 0)
    user32.keybd_event(VK_CONTROL, 0, 2, 0)
    time.sleep(0.2)
    user32.keybd_event(VK_DELETE, 0, 0, 0)
    time.sleep(0.08)
    user32.keybd_event(VK_DELETE, 0, 2, 0)
    time.sleep(0.6)

    # Center origin
    cx = 760
    cy = 430

    print("Beginning natural hand-drawn rocket illustration...")

    # 1. Aerodynamic Curved Fuselage (Bézier curves for bulging organic walls)
    print("-> Drawing curved aerodynamic hull...")
    # Left curved contour from nose down to engine base
    draw_bezier_curve((cx, cy - 230), (cx - 75, cy - 80), (cx - 60, cy + 110))
    # Right curved contour from nose down to engine base
    draw_bezier_curve((cx, cy - 230), (cx + 75, cy - 80), (cx + 60, cy + 110))
    # Bottom curved fuselage hull rim
    draw_bezier_curve((cx - 60, cy + 110), (cx, cy + 125), (cx + 60, cy + 110))

    # 2. Nose Cone Dividing Seam
    print("-> Drawing nose cone separation seam...")
    draw_bezier_curve((cx - 45, cy - 110), (cx, cy - 95), (cx + 45, cy - 110))
    # Nose cone center reflection line
    draw_natural_stroke([(cx, cy - 230), (cx, cy - 100)])

    # 3. Dual Concentric Porthole Windows
    print("-> Drawing dual porthole viewports with reflection glints...")
    # Top Window
    draw_natural_circle(cx, cy - 35, radius=28)
    draw_natural_circle(cx, cy - 35, radius=22)
    # Glass glare line
    draw_natural_stroke([(cx - 12, cy - 45), (cx - 4, cy - 50)])
    draw_natural_stroke([(cx - 15, cy - 38), (cx - 12, cy - 42)])

    # Bottom Window
    draw_natural_circle(cx, cy + 40, radius=24)
    draw_natural_circle(cx, cy + 40, radius=18)
    draw_natural_stroke([(cx - 10, cy + 32), (cx - 3, cy + 28)])

    # Rivet dots around top window
    for ang in range(0, 360, 45):
        rad = math.radians(ang)
        rx = cx + 25 * math.cos(rad)
        ry = (cy - 35) + 25 * math.sin(rad)
        draw_natural_stroke([(rx, ry), (rx + 1, ry + 1)])

    # 4. Body Panel Seams & Rivet Detailing
    print("-> Drawing structural panel lines...")
    draw_bezier_curve((cx - 58, cy + 85), (cx, cy + 98), (cx + 58, cy + 85))

    # 5. Swept-Back Aerodynamic Delta Fins
    print("-> Drawing swept-back aerodynamic booster fins...")
    # Left Fin (curved organic sweep)
    draw_cubic_bezier(
        (cx - 50, cy + 15),
        (cx - 110, cy + 60),
        (cx - 165, cy + 145),
        (cx - 145, cy + 175)
    )
    # Left fin bottom sweep back to hull
    draw_cubic_bezier(
        (cx - 145, cy + 175),
        (cx - 105, cy + 150),
        (cx - 85, cy + 130),
        (cx - 55, cy + 115)
    )
    # Left fin inner rib
    draw_natural_stroke([(cx - 50, cy + 40), (cx - 130, cy + 155)])

    # Right Fin (symmetric curved sweep)
    draw_cubic_bezier(
        (cx + 50, cy + 15),
        (cx + 110, cy + 60),
        (cx + 165, cy + 145),
        (cx + 145, cy + 175)
    )
    # Right fin bottom sweep back to hull
    draw_cubic_bezier(
        (cx + 145, cy + 175),
        (cx + 105, cy + 150),
        (cx + 85, cy + 130),
        (cx + 55, cy + 115)
    )
    # Right fin inner rib
    draw_natural_stroke([(cx + 50, cy + 40), (cx + 130, cy + 155)])

    # 6. Rocket Engine Bell Nozzle
    print("-> Drawing flared engine bell nozzle...")
    draw_natural_stroke([(cx - 35, cy + 118), (cx - 48, cy + 148)])
    draw_natural_stroke([(cx + 35, cy + 118), (cx + 48, cy + 148)])
    draw_bezier_curve((cx - 48, cy + 148), (cx, cy + 158), (cx + 48, cy + 148))
    # Cooling ring line
    draw_bezier_curve((cx - 42, cy + 135), (cx, cy + 143), (cx + 42, cy + 135))

    # 7. Fiery Thrust Flames (Multilayer dynamic curves)
    print("-> Drawing fiery exhaust plume and flame tongues...")
    # Outer turbulent flame
    draw_cubic_bezier((cx - 42, cy + 150), (cx - 65, cy + 200), (cx - 45, cy + 235), (cx - 25, cy + 220))
    draw_cubic_bezier((cx - 25, cy + 220), (cx - 15, cy + 250), (cx, cy + 285), (cx, cy + 295)) # Long center flame tip
    draw_cubic_bezier((cx, cy + 295), (cx + 15, cy + 250), (cx + 25, cy + 220), (cx + 25, cy + 220))
    draw_cubic_bezier((cx + 25, cy + 220), (cx + 45, cy + 235), (cx + 65, cy + 200), (cx + 42, cy + 150))

    # Inner intense flame core
    draw_cubic_bezier((cx - 24, cy + 152), (cx - 32, cy + 195), (cx - 15, cy + 230), (cx, cy + 245))
    draw_cubic_bezier((cx, cy + 245), (cx + 15, cy + 230), (cx + 32, cy + 195), (cx + 24, cy + 152))

    # Center flame spear
    draw_natural_stroke([(cx, cy + 155), (cx, cy + 265)])

    # Exhaust sparks / ember particles
    ember_locs = [
        (cx - 35, cy + 260), (cx + 38, cy + 265),
        (cx - 18, cy + 310), (cx + 15, cy + 315),
        (cx, cy + 330), (cx - 50, cy + 280), (cx + 52, cy + 275)
    ]
    for ex, ey in ember_locs:
        draw_natural_stroke([(ex, ey), (ex + 2, ey + 3)])

    # 8. Billowing Launch Smoke Clouds
    print("-> Drawing billowing smoke plumes at launch base...")
    # Left puff
    draw_bezier_curve((cx - 70, cy + 210), (cx - 120, cy + 230), (cx - 85, cy + 265))
    draw_bezier_curve((cx - 85, cy + 265), (cx - 110, cy + 300), (cx - 60, cy + 310))
    # Right puff
    draw_bezier_curve((cx + 70, cy + 210), (cx + 120, cy + 230), (cx + 85, cy + 265))
    draw_bezier_curve((cx + 85, cy + 265), (cx + 110, cy + 300), (cx + 60, cy + 310))

    # 9. Deep Space Cosmic Details: Ringed Planet & Sparkling Stars
    print("-> Adding ringed Saturn planet and constellation sparkles...")
    # Ringed planet top-left
    draw_saturn_planet(cx - 240, cy - 140, r=20)

    # Crescent Moon top-right
    draw_bezier_curve((cx + 250, cy - 180), (cx + 220, cy - 140), (cx + 250, cy - 100))
    draw_bezier_curve((cx + 250, cy - 100), (cx + 235, cy - 140), (cx + 250, cy - 180))

    # Sparkling Stars of varied sizes
    star_coords = [
        (cx - 280, cy - 40, 16),
        (cx - 200, cy + 60, 12),
        (cx + 230, cy - 30, 15),
        (cx + 270, cy + 80, 14),
        (cx - 160, cy - 200, 14),
        (cx + 180, cy - 210, 13),
        (cx + 210, cy + 180, 10),
        (cx - 210, cy + 180, 10),
        (cx - 120, cy - 160, 8),
        (cx + 120, cy - 160, 8),
    ]
    for sx, sy, sr in star_coords:
        draw_sparkle_star(sx, sy, sr)

    print("\n[+] Natural hand-drawn rocket artwork completed in MS Paint!")

if __name__ == "__main__":
    main()
