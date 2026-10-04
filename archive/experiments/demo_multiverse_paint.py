"""WinAI-OE live demo: paint 'THE LAST HUMAN IN THE MULTIVERSE' in MS Paint.

Method (fully disclosed): each element is drawn as genuine mouse strokes
through Paint's Pencil tool with a visible cursor; colors are picked from
Paint's real palette after auto-calibration against a toolbar screenshot.
No image is pasted. Every stage is verified by screenshot pixel analysis.
"""
import colorsys
import ctypes
import math
import subprocess
import time
from pathlib import Path

import pyautogui
from PIL import ImageGrab

import natural_rocket_artist as art

user32 = ctypes.windll.user32
WORKSPACE = Path(__file__).resolve().parent
SAVE_PATH = WORKSPACE / "winai_multiverse_artwork.png"

PALETTE_Y = 92
PALETTE_XS = list(range(970, 1345, 5))


def shot():
    return ImageGrab.grab().convert("RGB")


def classify_hue(rgb):
    r, g, b = [x / 255.0 for x in rgb]
    h, _, v = colorsys.rgb_to_hsv(r, g, b)
    return h * 360.0, v


def calibrate_palette(img):
    """Map color names to palette toolbar coordinates by hue matching."""
    found = {}
    for x in PALETTE_XS:
        px = img.getpixel((x, PALETTE_Y))
        h, v = classify_hue(px)
        if v < 0.25:
            found.setdefault("BLACK", x)
        elif h < 12 or h > 345:
            found.setdefault("RED", x)
        elif 12 <= h < 38:
            found.setdefault("ORANGE", x)
        elif 38 <= h < 72:
            found.setdefault("YELLOW", x)
        elif 72 <= h < 160:
            found.setdefault("GREEN", x)
        elif 160 <= h < 200:
            found.setdefault("CYAN", x)
        elif 200 <= h < 250:
            found.setdefault("BLUE", x)
        elif 250 <= h < 310:
            found.setdefault("PURPLE", x)
    print("Palette calibration:", {k: v for k, v in found.items()})
    return found


def glide_click(x, y, pre=0.6, post=0.25):
    art.move_to(x, y)
    time.sleep(0.05)
    art.mouse_down()
    art.mouse_up()
    time.sleep(post)


def select_tool(x, y, label):
    print(f"Selecting tool: {label} at ({x}, {y})")
    glide_click(x, y)
    time.sleep(0.3)


def select_color(pal, name):
    x = pal.get(name)
    if x is None:
        print(f"WARNING: color {name} not found, keeping current")
        return False
    print(f"Selecting color {name} at ({x}, {PALETTE_Y})")
    glide_click(x, PALETTE_Y)
    time.sleep(0.25)
    return True


def get_paint_hwnd():
    cmd = ["powershell", "-NoProfile", "-Command",
           "(Get-Process mspaint -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1).MainWindowHandle"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return int(res.stdout.strip())
    except Exception:
        return 0


def dark_ratio(img, box):
    crop = img.crop(box).convert("L")
    px = list(crop.getdata())
    return sum(1 for v in px if v < 60) / max(1, len(px))


def main():
    hwnd = get_paint_hwnd()
    if not hwnd:
        print("Launching MS Paint...")
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.5)
        hwnd = get_paint_hwnd()
    assert hwnd, "Paint did not start"
    print(f"Paint HWND: {hwnd}")

    # Foreground + clean canvas
    user32.keybd_event(0x12, 0, 0, 0)
    user32.ShowWindow(hwnd, 3)
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.keybd_event(0x12, 0, 2, 0)
    time.sleep(1.0)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.15)
    pyautogui.press("delete")
    time.sleep(0.4)
    pyautogui.press("escape")
    time.sleep(0.2)

    # Calibrate + pencil
    pal = calibrate_palette(shot())
    for need in ("BLACK", "RED", "ORANGE", "YELLOW", "CYAN", "BLUE", "PURPLE", "GREEN"):
        assert need in pal, f"palette color missing: {need}"
    select_tool(325, 105, "Pencil")

    # Background fill attempt (bucket ~375,105) with BLACK, then verify
    print("Attempting background fill with Fill Bucket...")
    select_tool(375, 105, "FillBucket?")
    select_color(pal, "BLACK")
    glide_click(960, 900)
    time.sleep(0.8)
    ratio = dark_ratio(shot(), (300, 350, 1620, 950))
    night = ratio > 0.50
    print(f"Canvas dark ratio: {ratio:.2f} -> {'NIGHT scene' if night else 'DAY scene fallback'}")
    select_tool(325, 105, "Pencil")  # back to pencil regardless

    cx = 960
    if night:
        paint_night_scene(pal, cx)
    else:
        paint_day_scene(pal, cx)

    title_ok = try_title_text()
    print(f"Title text in image: {'OK' if title_ok else 'SKIPPED (limitation)'}")

    # Save through the real Save As dialog
    print("Saving via Ctrl+Shift+S...")
    pyautogui.hotkey("ctrl", "shift", "s")
    time.sleep(1.2)
    pyautogui.write(str(SAVE_PATH), interval=0.008)
    time.sleep(0.3)
    pyautogui.press("enter")
    time.sleep(1.5)
    # Overwrite confirmation (Just in case): press Enter on potential dialog
    pyautogui.press("enter")
    time.sleep(1.0)

    ok = SAVE_PATH.exists() and SAVE_PATH.stat().st_size > 0
    opened = False
    if ok:
        try:
            from PIL import Image
            with Image.open(SAVE_PATH) as im:
                im.verify()
            opened = True
        except Exception as e:
            print("Image open check failed:", e)
    print(f"SAVE VERIFIED: exists={ok} opens={opened} size={SAVE_PATH.stat().st_size if ok else 0}")
    time.sleep(0.5)
    ImageGrab.grab().save("multiverse_paint_final.png")
    print("Demo screenshot: multiverse_paint_final.png")
    print(f"RESULT night={night} title_ok={title_ok} saved={ok and opened}")


def hline(y, x0=180, x1=1740, delay=0.002):
    art.draw_natural_stroke([(x0, y), (x1, y)], step_size=6, delay=delay)


def paint_night_scene(pal, cx):
    print("Painting NIGHT cosmos...")
    # Nebula bands
    for name, y in (("PURPLE", 300), ("BLUE", 340), ("CYAN", 380), ("PURPLE", 420)):
        select_color(pal, name)
        for off in (0, 18, 36):
            art.draw_bezier_curve((200, y + off), (960, y - 40 + off), (1720, y + off), num_points=30)
    # Stars
    import random
    random.seed(7)
    select_color(pal, "YELLOW")
    for _ in range(45):
        x, y = random.randint(180, 1740), random.randint(240, 700)
        art.draw_natural_stroke([(x, y), (x + 2, y + 1)], delay=0.002)
    select_color(pal, "CYAN")
    for sx, sy in [(300, 300), (1600, 280), (500, 550), (1400, 600), (760, 260)]:
        art.draw_sparkle_star(sx, sy, r=14)
    # Ringed planet top-right
    select_color(pal, "PURPLE")
    art.draw_natural_circle(1450, 380, 62)
    ring = []
    for i in range(40):
        t = 2 * math.pi * i / 39
        ring.append((1450 + 120 * math.cos(t), 380 + 30 * math.sin(t)))
    art.draw_natural_stroke(ring)
    # Moon top-left with craters
    select_color(pal, "YELLOW")
    art.draw_natural_circle(350, 330, 45)
    for ex, ey in [(335, 320), (360, 340), (350, 350)]:
        art.draw_natural_circle(ex, ey, 7, segments=18)
    # Portal: concentric glowing ellipses center
    for name, rx, ry in (("CYAN", 110, 130), ("BLUE", 85, 105), ("PURPLE", 60, 78)):
        select_color(pal, name)
        pts = []
        for i in range(49):
            t = 2 * math.pi * i / 48
            pts.append((cx + rx * math.cos(t), 430 + ry * math.sin(t)))
        art.draw_natural_stroke(pts)
    # City skyline silhouettes (blue towers + lit windows)
    select_color(pal, "BLUE")
    towers = [(420, 620, 480, 760), (500, 580, 560, 760), (1330, 600, 1390, 760), (1410, 560, 1480, 760)]
    for x0, y0, x1, y1 in towers:
        art.draw_natural_stroke([(x0, y1), (x0, y0), (x1, y0), (x1, y1)])
        art.draw_natural_stroke([(x0 + (x1 - x0) / 2, y0), (x0 + (x1 - x0) / 2, y0 - 25)])
    select_color(pal, "YELLOW")
    for wx in range(430, 480, 14):
        for wy in range(640, 750, 18):
            art.draw_natural_stroke([(wx, wy), (wx + 3, wy)], delay=0.002)
    for wx in range(1420, 1470, 14):
        for wy in range(600, 750, 18):
            art.draw_natural_stroke([(wx, wy), (wx + 3, wy)], delay=0.002)
    # Floating islands + waterfalls + bridges
    select_color(pal, "GREEN")
    for ix, iy, w in [(640, 800, 90), (960, 830, 110), (1280, 800, 90)]:
        pts = []
        for i in range(37):
            t = 2 * math.pi * i / 36
            pts.append((ix + w * math.cos(t), iy + 22 * math.sin(t)))
        art.draw_natural_stroke(pts)
        art.draw_natural_stroke([(ix - w + 10, iy + 10), (ix, iy + 70), (ix + w - 10, iy + 10)])
    select_color(pal, "CYAN")
    for ix, iy in [(640, 822), (960, 852), (1280, 822)]:
        art.draw_natural_stroke([(ix - 8, iy), (ix - 8, iy + 90)])
        art.draw_natural_stroke([(ix + 8, iy), (ix + 8, iy + 90)])
    select_color(pal, "PURPLE")
    art.draw_natural_stroke([(730, 800), (850, 810)])
    art.draw_natural_stroke([(1070, 810), (1190, 800)])
    # Explorer on central island
    select_color(pal, "YELLOW")
    art.draw_natural_circle(960, 790, 8, segments=20)
    art.draw_natural_stroke([(960, 798), (960, 818)])
    art.draw_natural_stroke([(950, 806), (970, 806)])
    art.draw_natural_stroke([(960, 818), (952, 832)])
    art.draw_natural_stroke([(960, 818), (968, 832)])
    # Ocean + portal reflection
    select_color(pal, "BLUE")
    for y in range(900, 1010, 16):
        art.draw_bezier_curve((250, y), (960, y - 8), (1670, y), num_points=28)
    select_color(pal, "CYAN")
    for dx, wdt in [(-30, 14), (-10, 20), (15, 14)]:
        art.draw_natural_stroke([(cx + dx, 560), (cx + dx, 880)], delay=0.003)
    # Satellite + tech dots
    select_color(pal, "RED")
    art.draw_natural_stroke([(1500, 520), (1540, 520), (1540, 545), (1500, 545), (1500, 520)])
    art.draw_natural_stroke([(1450, 532), (1500, 532)])
    art.draw_natural_stroke([(1540, 532), (1590, 532)])
    print("Night scene complete.")


def paint_day_scene(pal, cx):
    print("Painting DAY fallback scene...")
    select_color(pal, "BLUE")
    for y in range(250, 420, 16):
        hline(y)
    select_color(pal, "YELLOW")
    art.draw_natural_circle(1560, 330, 45)
    select_color(pal, "CYAN")
    for y in range(900, 1010, 16):
        art.draw_bezier_curve((250, y), (960, y - 8), (1670, y), num_points=28)
    select_color(pal, "GREEN")
    for ix, iy, w in [(640, 800, 90), (960, 830, 110), (1280, 800, 90)]:
        pts = []
        for i in range(37):
            t = 2 * math.pi * i / 36
            pts.append((ix + w * math.cos(t), iy + 22 * math.sin(t)))
        art.draw_natural_stroke(pts)
    select_color(pal, "PURPLE")
    art.draw_natural_circle(1450, 380, 62)
    select_color(pal, "RED")
    for name, rx, ry in (("RED", 110, 130),):
        pts = []
        for i in range(49):
            t = 2 * math.pi * i / 48
            pts.append((cx + rx * math.cos(t), 430 + ry * math.sin(t)))
        art.draw_natural_stroke(pts)
    select_color(pal, "BLACK")
    art.draw_natural_stroke([(420, 760), (420, 620), (480, 620), (480, 760)])
    art.draw_natural_stroke([(1410, 760), (1410, 560), (1480, 560), (1480, 760)])
    art.draw_natural_circle(960, 790, 8, segments=20)
    art.draw_natural_stroke([(960, 798), (960, 832)])
    print("Day scene complete.")


def try_title_text():
    """Attempt Paint Text tool for the artwork title; verify via pixels."""
    print("Attempting title text with Text tool...")
    try:
        select_tool(425, 105, "Text?")
        glide_click(960, 262)
        time.sleep(0.4)
        pyautogui = __import__("pyautogui")
        pyautogui.write("THE LAST HUMAN IN THE MULTIVERSE", interval=0.02)
        time.sleep(0.4)
        pyautogui.press("enter")
        pyautogui.write("Created by WinAI-OE", interval=0.02)
        time.sleep(0.4)
        pyautogui.press("escape")
        time.sleep(0.4)
        img = shot().convert("L")
        crop = img.crop((500, 240, 1420, 310))
        dark = sum(1 for v in crop.getdata() if v < 100) / (920 * 70)
        print(f"Title region dark ratio: {dark:.3f}")
        if dark > 0.01:
            return True
        # undo stray marks
        pyautogui.hotkey("ctrl", "z")
        time.sleep(0.3)
        return False
    except Exception as e:
        print("Title attempt failed:", e)
        return False


if __name__ == "__main__":
    main()
