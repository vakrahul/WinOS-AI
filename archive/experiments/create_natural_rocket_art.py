import cv2
import numpy as np
import math

def create_beautiful_rocket(width=1600, height=900):
    # Create white canvas
    canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

    cx = width // 2
    cy = height // 2 - 20

    # Colors (BGR)
    COLOR_OUTLINE = (30, 30, 30)         # Crisp charcoal outline
    COLOR_NOSE = (50, 60, 230)           # Crimson red
    COLOR_BODY = (245, 245, 248)         # Clean off-white fuselage
    COLOR_BODY_SHADOW = (215, 218, 225)  # Subtle 3D shadow
    COLOR_FINS = (40, 140, 240)          # Vibrant rocket orange
    COLOR_WINDOW_FRAME = (90, 95, 105)   # Metallic steel
    COLOR_GLASS = (235, 205, 120)        # Cyan blue glass
    COLOR_GLASS_SHINE = (255, 245, 210)  # Glare reflection
    COLOR_FLAME_OUTER = (20, 100, 255)   # Deep fiery orange
    COLOR_FLAME_INNER = (30, 210, 255)   # Intense bright yellow
    COLOR_FLAME_CORE = (255, 255, 255)   # White hot propulsion core
    COLOR_SPACE_STARS = (80, 80, 80)     # Starlight charcoal
    COLOR_MOON = (180, 185, 195)         # Silver crescent

    # 1. Deep Space Stars and Celestial Objects
    # Crescent Moon top-right
    moon_cx, moon_cy = cx + 380, cy - 220
    cv2.circle(canvas, (moon_cx, moon_cy), 42, COLOR_MOON, -1, cv2.LINE_AA)
    cv2.circle(canvas, (moon_cx + 18, moon_cy - 10), 38, (255, 255, 255), -1, cv2.LINE_AA)
    cv2.circle(canvas, (moon_cx, moon_cy), 42, COLOR_OUTLINE, 2, cv2.LINE_AA)

    # Ringed Planet top-left (Saturn)
    sat_cx, sat_cy = cx - 380, cy - 180
    cv2.circle(canvas, (sat_cx, sat_cy), 32, (200, 210, 225), -1, cv2.LINE_AA)
    cv2.circle(canvas, (sat_cx, sat_cy), 32, COLOR_OUTLINE, 2, cv2.LINE_AA)
    # Planetary ring ellipse
    cv2.ellipse(canvas, (sat_cx, sat_cy), (68, 18), -25, 0, 360, COLOR_OUTLINE, 2, cv2.LINE_AA)

    # Sparkle Stars
    star_positions = [
        (cx - 450, cy - 60, 18), (cx - 300, cy + 120, 14),
        (cx + 320, cy - 80, 16), (cx + 420, cy + 110, 20),
        (cx - 220, cy - 260, 12), (cx + 250, cy - 280, 15),
        (cx - 340, cy + 260, 16), (cx + 360, cy + 240, 14),
        (cx - 180, cy + 20, 10), (cx + 190, cy - 20, 10),
    ]
    for sx, sy, sr in star_positions:
        # 4-point sparkle star
        pts_star = [
            (sx, sy - sr), (sx + int(sr*0.25), sy - int(sr*0.25)),
            (sx + sr, sy), (sx + int(sr*0.25), sy + int(sr*0.25)),
            (sx, sy + sr), (sx - int(sr*0.25), sy + int(sr*0.25)),
            (sx - sr, sy), (sx - int(sr*0.25), sy - int(sr*0.25))
        ]
        cv2.fillPoly(canvas, [np.array(pts_star, dtype=np.int32)], (240, 220, 140), cv2.LINE_AA)
        cv2.polylines(canvas, [np.array(pts_star, dtype=np.int32)], True, COLOR_OUTLINE, 1, cv2.LINE_AA)

    # 2. Fiery Rocket Exhaust Flames
    # Outer Flame Plume
    flame_outer = np.array([
        (cx - 55, cy + 155),
        (cx - 95, cy + 235),
        (cx - 45, cy + 285),
        (cx, cy + 390),       # Deep flame tip
        (cx + 45, cy + 285),
        (cx + 95, cy + 235),
        (cx + 55, cy + 155)
    ], dtype=np.int32)
    cv2.fillPoly(canvas, [flame_outer], COLOR_FLAME_OUTER, cv2.LINE_AA)
    cv2.polylines(canvas, [flame_outer], True, COLOR_OUTLINE, 3, cv2.LINE_AA)

    # Middle Flame Layer
    flame_mid = np.array([
        (cx - 38, cy + 158),
        (cx - 55, cy + 230),
        (cx - 25, cy + 265),
        (cx, cy + 335),
        (cx + 25, cy + 265),
        (cx + 55, cy + 230),
        (cx + 38, cy + 158)
    ], dtype=np.int32)
    cv2.fillPoly(canvas, [flame_mid], COLOR_FLAME_INNER, cv2.LINE_AA)
    cv2.polylines(canvas, [flame_mid], True, COLOR_OUTLINE, 2, cv2.LINE_AA)

    # Inner Hot Core
    flame_core = np.array([
        (cx - 20, cy + 160),
        (cx - 22, cy + 215),
        (cx, cy + 270),
        (cx + 22, cy + 215),
        (cx + 20, cy + 160)
    ], dtype=np.int32)
    cv2.fillPoly(canvas, [flame_core], COLOR_FLAME_CORE, cv2.LINE_AA)
    cv2.polylines(canvas, [flame_core], True, COLOR_OUTLINE, 2, cv2.LINE_AA)

    # Exhaust Spark Particles
    sparks = [
        (cx - 65, cy + 320, 6), (cx + 60, cy + 330, 5),
        (cx - 25, cy + 410, 4), (cx + 20, cy + 420, 5),
        (cx, cy + 435, 6), (cx - 85, cy + 360, 4), (cx + 80, cy + 355, 4)
    ]
    for sp_x, sp_y, sp_r in sparks:
        cv2.circle(canvas, (sp_x, sp_y), sp_r, COLOR_FLAME_INNER, -1, cv2.LINE_AA)
        cv2.circle(canvas, (sp_x, sp_y), sp_r, COLOR_OUTLINE, 1, cv2.LINE_AA)

    # 3. Aerodynamic Booster Wings / Fins
    # Left Wing
    fin_left = np.array([
        (cx - 75, cy + 25),
        (cx - 195, cy + 165),
        (cx - 150, cy + 195),
        (cx - 78, cy + 145)
    ], dtype=np.int32)
    cv2.fillPoly(canvas, [fin_left], COLOR_FINS, cv2.LINE_AA)
    cv2.polylines(canvas, [fin_left], True, COLOR_OUTLINE, 3, cv2.LINE_AA)
    # Left fin highlight ridge
    cv2.line(canvas, (cx - 80, cy + 45), (cx - 170, cy + 175), (60, 165, 255), 3, cv2.LINE_AA)

    # Right Wing
    fin_right = np.array([
        (cx + 75, cy + 25),
        (cx + 195, cy + 165),
        (cx + 150, cy + 195),
        (cx + 78, cy + 145)
    ], dtype=np.int32)
    cv2.fillPoly(canvas, [fin_right], COLOR_FINS, cv2.LINE_AA)
    cv2.polylines(canvas, [fin_right], True, COLOR_OUTLINE, 3, cv2.LINE_AA)
    # Right fin shadow ridge
    cv2.line(canvas, (cx + 80, cy + 45), (cx + 170, cy + 175), (20, 105, 200), 3, cv2.LINE_AA)

    # 4. Engine Bell Nozzle
    nozzle = np.array([
        (cx - 52, cy + 140),
        (cx - 62, cy + 172),
        (cx + 62, cy + 172),
        (cx + 52, cy + 140)
    ], dtype=np.int32)
    cv2.fillPoly(canvas, [nozzle], COLOR_WINDOW_FRAME, cv2.LINE_AA)
    cv2.polylines(canvas, [nozzle], True, COLOR_OUTLINE, 3, cv2.LINE_AA)
    cv2.line(canvas, (cx - 58, cy + 156), (cx + 58, cy + 156), (140, 145, 155), 2, cv2.LINE_AA)

    # 5. Main Rocket Fuselage Body (Smooth Curvature)
    # Draw curved body using polygon approximation
    hull_pts = []
    # Left side curve from top to bottom
    for i in range(25):
        t = i / 24.0
        # Bulging aerodynamic curve
        hx = int(cx - (78 + 8 * math.sin(t * math.pi)))
        hy = int(cy - 120 + t * 260)
        hull_pts.append((hx, hy))
    # Bottom rim
    hull_pts.append((cx + 78, cy + 140))
    # Right side curve from bottom to top
    for i in range(24, -1, -1):
        t = i / 24.0
        hx = int(cx + (78 + 8 * math.sin(t * math.pi)))
        hy = int(cy - 120 + t * 260)
        hull_pts.append((hx, hy))

    cv2.fillPoly(canvas, [np.array(hull_pts, dtype=np.int32)], COLOR_BODY, cv2.LINE_AA)
    # Fuselage 3D shadow on right half
    shadow_pts = [(cx, cy - 120)] + [pt for pt in hull_pts if pt[0] >= cx] + [(cx, cy + 140)]
    cv2.fillPoly(canvas, [np.array(shadow_pts, dtype=np.int32)], COLOR_BODY_SHADOW, cv2.LINE_AA)
    cv2.polylines(canvas, [np.array(hull_pts, dtype=np.int32)], True, COLOR_OUTLINE, 3, cv2.LINE_AA)

    # Horizontal panel separation seams
    cv2.line(canvas, (cx - 82, cy + 80), (cx + 82, cy + 80), COLOR_OUTLINE, 2, cv2.LINE_AA)
    cv2.line(canvas, (cx - 80, cy + 105), (cx + 80, cy + 105), COLOR_OUTLINE, 2, cv2.LINE_AA)

    # Center dorsal stabilizer rib
    cv2.line(canvas, (cx, cy + 30), (cx, cy + 138), COLOR_OUTLINE, 3, cv2.LINE_AA)

    # 6. Aerodynamic Crimson Nose Cone
    nose_pts = []
    # Left curve
    for i in range(20):
        t = i / 19.0
        nx = int(cx - 78 * (1 - t)**1.3)
        ny = int(cy - 120 - t * 140)
        nose_pts.append((nx, ny))
    # Right curve
    for i in range(19, -1, -1):
        t = i / 19.0
        nx = int(cx + 78 * (1 - t)**1.3)
        ny = int(cy - 120 - t * 140)
        nose_pts.append((nx, ny))

    cv2.fillPoly(canvas, [np.array(nose_pts, dtype=np.int32)], COLOR_NOSE, cv2.LINE_AA)
    cv2.polylines(canvas, [np.array(nose_pts, dtype=np.int32)], True, COLOR_OUTLINE, 3, cv2.LINE_AA)
    # Nose cone specular glint
    cv2.line(canvas, (cx - 20, cy - 230), (cx - 45, cy - 145), (120, 130, 255), 3, cv2.LINE_AA)

    # 7. Dual Astronaut Porthole Windows
    # Upper Primary Viewport
    cv2.circle(canvas, (cx, cy - 35), 38, COLOR_WINDOW_FRAME, -1, cv2.LINE_AA)
    cv2.circle(canvas, (cx, cy - 35), 38, COLOR_OUTLINE, 3, cv2.LINE_AA)
    cv2.circle(canvas, (cx, cy - 35), 28, COLOR_GLASS, -1, cv2.LINE_AA)
    cv2.circle(canvas, (cx, cy - 35), 28, COLOR_OUTLINE, 2, cv2.LINE_AA)
    # Window reflection glare
    cv2.ellipse(canvas, (cx - 10, cy - 45), (14, 6), -35, 0, 360, COLOR_GLASS_SHINE, -1, cv2.LINE_AA)

    # Viewport Screws / Rivets
    for a in range(0, 360, 45):
        rad = math.radians(a)
        rx = int(cx + 33 * math.cos(rad))
        ry = int((cy - 35) + 33 * math.sin(rad))
        cv2.circle(canvas, (rx, ry), 2, COLOR_OUTLINE, -1, cv2.LINE_AA)

    # Lower Secondary Viewport
    cv2.circle(canvas, (cx, cy + 35), 26, COLOR_WINDOW_FRAME, -1, cv2.LINE_AA)
    cv2.circle(canvas, (cx, cy + 35), 26, COLOR_OUTLINE, 2, cv2.LINE_AA)
    cv2.circle(canvas, (cx, cy + 35), 18, COLOR_GLASS, -1, cv2.LINE_AA)
    cv2.circle(canvas, (cx, cy + 35), 18, COLOR_OUTLINE, 1, cv2.LINE_AA)
    cv2.ellipse(canvas, (cx - 6, cy + 28), (8, 4), -35, 0, 360, COLOR_GLASS_SHINE, -1, cv2.LINE_AA)

    return canvas

if __name__ == "__main__":
    img = create_beautiful_rocket()
    cv2.imwrite("beautiful_natural_rocket.png", img)
    print("Generated 'beautiful_natural_rocket.png' (1600x900 full HD artwork).")
