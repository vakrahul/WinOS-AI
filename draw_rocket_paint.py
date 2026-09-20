import ctypes
import math
import time

user32 = ctypes.windll.user32

def draw_stroke(points, delay=0.005):
    """Draw a smooth continuous stroke through a list of (x, y) points."""
    if not points:
        return
    x0, y0 = points[0]
    user32.SetCursorPos(x0, y0)
    time.sleep(0.02)
    user32.mouse_event(2, 0, 0, 0, 0) # Left mouse down
    time.sleep(0.01)

    for i in range(1, len(points)):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]
        dist = max(abs(x2 - x1), abs(y2 - y1))
        steps = max(1, dist // 3)
        for s in range(1, steps + 1):
            curr_x = int(x1 + (x2 - x1) * (s / steps))
            curr_y = int(y1 + (y2 - y1) * (s / steps))
            user32.SetCursorPos(curr_x, curr_y)
            time.sleep(delay)

    user32.mouse_event(4, 0, 0, 0, 0) # Left mouse up
    time.sleep(0.02)

def draw_line(x1, y1, x2, y2):
    draw_stroke([(x1, y1), (x2, y2)])

def draw_circle(cx, cy, radius, segments=36):
    pts = []
    for i in range(segments + 1):
        theta = (2 * math.pi * i) / segments
        x = int(cx + radius * math.cos(theta))
        y = int(cy + radius * math.sin(theta))
        pts.append((x, y))
    draw_stroke(pts)

def draw_star(cx, cy, size=15):
    draw_line(cx - size, cy, cx + size, cy)
    draw_line(cx, cy - size, cx, cy + size)
    d = int(size * 0.6)
    draw_line(cx - d, cy - d, cx + d, cy + d)
    draw_line(cx - d, cy + d, cx + d, cy - d)

def main():
    import subprocess
    cmd = ["powershell", "-NoProfile", "-Command", "(Get-Process mspaint -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        hwnd = int(res.stdout.strip())
    except Exception:
        hwnd = 0

    if not hwnd:
        print("MS Paint is not open. Launching mspaint...")
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.0)
        res = subprocess.run(cmd, capture_output=True, text=True)
        hwnd = int(res.stdout.strip())

    print(f"Bringing Paint (HWND: {hwnd}) to foreground...")
    user32.ShowWindow(hwnd, 3) # SW_MAXIMIZE
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    time.sleep(1.0)

    cx = 770
    cy = 440

    print("Designing Rocket in MS Paint...")

    # 1. Nose Cone
    print("[1/6] Drawing aerodynamic nose cone...")
    draw_line(cx, cy - 190, cx - 55, cy - 90)
    draw_line(cx, cy - 190, cx + 55, cy - 90)
    draw_line(cx - 55, cy - 90, cx + 55, cy - 90)
    # Nose cone highlight ridge
    draw_line(cx, cy - 190, cx, cy - 90)

    # 2. Main Rocket Fuselage
    print("[2/6] Drawing rocket fuselage...")
    draw_line(cx - 55, cy - 90, cx - 55, cy + 110)
    draw_line(cx + 55, cy - 90, cx + 55, cy + 110)
    draw_line(cx - 55, cy + 110, cx + 55, cy + 110)
    # Decorative stripes / bands
    draw_line(cx - 55, cy + 75, cx + 55, cy + 75)
    draw_line(cx - 55, cy + 90, cx + 55, cy + 90)

    # 3. Porthole Astronaut Window
    print("[3/6] Drawing astronaut porthole window...")
    draw_circle(cx, cy - 5, radius=30)
    draw_circle(cx, cy - 5, radius=23)
    # Window reflection glint
    draw_line(cx - 15, cy - 15, cx - 5, cy - 20)

    # 4. Wings & Fins
    print("[4/6] Drawing left and right booster fins...")
    # Left Fin
    draw_stroke([
        (cx - 55, cy + 30),
        (cx - 130, cy + 140),
        (cx - 100, cy + 155),
        (cx - 55, cy + 110)
    ])
    # Right Fin
    draw_stroke([
        (cx + 55, cy + 30),
        (cx + 130, cy + 140),
        (cx + 100, cy + 155),
        (cx + 55, cy + 110)
    ])
    # Center stabilizer
    draw_line(cx, cy + 60, cx, cy + 120)

    # 5. Engine Nozzle & Thruster Plume
    print("[5/6] Drawing rocket engine nozzle and fiery exhaust plume...")
    draw_stroke([
        (cx - 35, cy + 110),
        (cx - 45, cy + 135),
        (cx + 45, cy + 135),
        (cx + 35, cy + 110)
    ])

    # Big outer flame
    draw_stroke([
        (cx - 40, cy + 135),
        (cx - 55, cy + 190),
        (cx - 25, cy + 175),
        (cx, cy + 240),      # Center flame tip
        (cx + 25, cy + 175),
        (cx + 55, cy + 190),
        (cx + 40, cy + 135)
    ])

    # Inner core flame
    draw_stroke([
        (cx - 20, cy + 135),
        (cx - 15, cy + 175),
        (cx, cy + 205),
        (cx + 15, cy + 175),
        (cx + 20, cy + 135)
    ])

    # 6. Space Background: Sparkling Stars & Crescent Moon
    print("[6/6] Adding deep space stars and moon...")
    draw_star(cx - 220, cy - 120, size=18)
    draw_star(cx + 220, cy - 100, size=20)
    draw_star(cx - 200, cy + 80, size=14)
    draw_star(cx + 210, cy + 110, size=16)
    draw_star(cx - 140, cy - 20, size=10)
    draw_star(cx + 150, cy - 30, size=12)

    # Little crescent moon at top right
    draw_stroke([
        (cx + 280, cy - 160),
        (cx + 260, cy - 140),
        (cx + 260, cy - 100),
        (cx + 280, cy - 80),
        (cx + 270, cy - 100),
        (cx + 270, cy - 140),
        (cx + 280, cy - 160)
    ])

    print("\n[+] Beautiful Rocket successfully designed and drawn in MS Paint!")

if __name__ == "__main__":
    main()
