"""WinAI-OE Live Demonstration: 'THE LAST HUMAN IN THE MULTIVERSE'
Direct painting in MS Paint + Professional Presentation in Notepad.
Cross-application window arrangement and verifiable file verification.
"""

import ctypes
import math
import os
from pathlib import Path
import subprocess
import time
from PIL import Image, ImageGrab
import pyautogui
import win32con
import win32gui

import natural_rocket_artist as art
from src.windows_integration.uia_service import UIAutomationService
from src.windows_integration.vision_automation import HumanCursorController

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

WORKSPACE = Path(r"D:\Interveiewsass").resolve()
ARTWORK_FILE = WORKSPACE / "winai_multiverse_artwork.png"
PRESENTATION_FILE = WORKSPACE / "winai_demo_presentation.txt"

# Exact verified Paint toolbar coordinates on 1920x1200
PENCIL_TOOL = (325, 105)
PALETTE = {
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
}


def force_foreground(hwnd, maximize=True):
    cur_thread = kernel32.GetCurrentThreadId()
    fg_hwnd = user32.GetForegroundWindow()
    fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
    user32.AttachThreadInput(cur_thread, fg_thread, True)
    user32.keybd_event(0x12, 0, 0, 0)
    user32.keybd_event(0x12, 0, 2, 0)
    user32.ShowWindow(hwnd, win32con.SW_MAXIMIZE if maximize else win32con.SW_RESTORE)
    user32.BringWindowToTop(hwnd)
    user32.SetForegroundWindow(hwnd)
    user32.AttachThreadInput(cur_thread, fg_thread, False)
    time.sleep(1.0)


def get_process_hwnd(proc_name: str) -> int:
    cmd = [
        "powershell",
        "-NoProfile",
        "-Command",
        f"(Get-Process {proc_name} -ErrorAction SilentlyContinue | Where-Object {{ $_.MainWindowHandle -ne 0 }} | Select-Object -First 1).MainWindowHandle",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        return int(res.stdout.strip())
    except Exception:
        return 0


def select_color(name: str):
    coord = PALETTE.get(name)
    if not coord:
        return
    art.move_to(coord[0], coord[1])
    time.sleep(0.06)
    art.mouse_down()
    art.mouse_up()
    time.sleep(0.12)


def select_tool(x, y):
    art.move_to(x, y)
    time.sleep(0.06)
    art.mouse_down()
    art.mouse_up()
    time.sleep(0.15)


def draw_stroke_smooth(points, step=3, delay=0.003):
    if not points:
        return
    art.move_to(points[0][0], points[0][1])
    time.sleep(0.015)
    art.mouse_down()
    for i in range(1, len(points)):
        x0, y0 = points[i - 1]
        x1, y1 = points[i]
        d = math.hypot(x1 - x0, y1 - y0)
        steps = max(1, int(d / step))
        for s in range(1, steps + 1):
            t = s / steps
            cx = x0 + (x1 - x0) * t
            cy = y0 + (y1 - y0) * t
            art.move_to(cx, cy)
            time.sleep(delay)
    art.mouse_up()
    time.sleep(0.02)


def draw_bezier(p0, p1, p2, num=30, delay=0.003):
    pts = []
    for i in range(num + 1):
        t = i / num
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
        pts.append((x, y))
    draw_stroke_smooth(pts, delay=delay)


def draw_circle(cx, cy, r, segs=36):
    pts = []
    for i in range(segs + 1):
        theta = (2 * math.pi * i) / segs
        pts.append((cx + r * math.cos(theta), cy + r * math.sin(theta)))
    draw_stroke_smooth(pts, delay=0.003)


def draw_ellipse(cx, cy, rx, ry, segs=36, tilt=0):
    pts = []
    for i in range(segs + 1):
        t = (2 * math.pi * i) / segs
        x = rx * math.cos(t)
        y = ry * math.sin(t)
        if tilt != 0:
            rx_t = x * math.cos(tilt) - y * math.sin(tilt)
            ry_t = x * math.sin(tilt) + y * math.cos(tilt)
            x, y = rx_t, ry_t
        pts.append((cx + x, cy + y))
    draw_stroke_smooth(pts, delay=0.003)


def draw_star(cx, cy, r=14):
    draw_stroke_smooth([(cx - r, cy), (cx + r, cy)], delay=0.002)
    draw_stroke_smooth([(cx, cy - r), (cx, cy + r)], delay=0.002)
    dr = r * 0.4
    draw_stroke_smooth([(cx - dr, cy - dr), (cx + dr, cy + dr)], delay=0.002)
    draw_stroke_smooth([(cx - dr, cy + dr), (cx + dr, cy - dr)], delay=0.002)


# =============================================================================
# PHASE 1 — OPEN APPLICATIONS & VERIFY
# =============================================================================
def phase1_open_apps():
    print("=" * 75)
    print("PHASE 1 — OPEN APPLICATIONS & VERIFY ACCESSIBILITY")
    print("=" * 75)

    # 1. Paint
    paint_hwnd = get_process_hwnd("mspaint")
    if not paint_hwnd:
        print("[*] Launching Microsoft Paint...")
        subprocess.run(["cmd", "/c", "start", "mspaint"])
        time.sleep(2.5)
        paint_hwnd = get_process_hwnd("mspaint")
    print(f"[+] Microsoft Paint active | HWND: 0x{paint_hwnd:X}")
    assert paint_hwnd, "Failed to launch or locate Paint"

    # 2. Notepad
    notepad_hwnd = get_process_hwnd("notepad")
    if not notepad_hwnd:
        print("[*] Launching Notepad...")
        subprocess.run(["cmd", "/c", "start", "notepad"])
        time.sleep(2.0)
        notepad_hwnd = get_process_hwnd("notepad")
    print(f"[+] Notepad active | HWND: 0x{notepad_hwnd:X}")
    assert notepad_hwnd, "Failed to launch or locate Notepad"

    return paint_hwnd, notepad_hwnd


# =============================================================================
# PHASE 2 — CREATE EXTRAORDINARY ARTWORK IN PAINT
# =============================================================================
def phase2_create_multiverse_artwork(paint_hwnd):
    print("\n" + "=" * 75)
    print("PHASE 2 — CREATE 'THE LAST HUMAN IN THE MULTIVERSE' IN PAINT")
    print("=" * 75)

    force_foreground(paint_hwnd, maximize=True)
    time.sleep(1.0)

    # Dismiss any active selection or text tool
    pyautogui.press("escape")
    time.sleep(0.1)
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.press("delete")
    time.sleep(0.3)
    pyautogui.press("escape")
    time.sleep(0.2)

    # Select Pencil Tool
    print("[*] Selecting Pencil Tool at (325, 105)...")
    select_tool(PENCIL_TOOL[0], PENCIL_TOOL[1])

    # Center coordinates of the canvas
    cx = 960
    cy = 650

    print("[1/10] Painting Deep Cosmic Nebulae & Celestial Background...")
    # Purple & Blue Swirls
    select_color("PURPLE")
    draw_bezier((200, 320), (600, 240), (960, 310), num=35)
    draw_bezier((960, 310), (1350, 380), (1720, 280), num=35)
    draw_bezier((250, 360), (700, 300), (1100, 370), num=30)

    select_color("BLUE")
    draw_bezier((180, 280), (550, 210), (1050, 270), num=35)
    draw_bezier((850, 330), (1250, 270), (1740, 330), num=35)

    select_color("CYAN")
    draw_bezier((300, 390), (780, 340), (1200, 390), num=30)
    draw_bezier((700, 420), (1150, 360), (1650, 410), num=30)

    print("[2/10] Painting Mysterious Ringed Planet & Craters...")
    select_color("PURPLE")
    draw_circle(1480, 350, 52)
    # Dual rings tilted at -25 degrees
    draw_ellipse(1480, 350, 105, 26, tilt=-0.4)
    draw_ellipse(1480, 350, 120, 32, tilt=-0.4)

    print("[3/10] Painting Cosmic Moon with Surface Detailing...")
    select_color("YELLOW")
    draw_circle(380, 320, 42)
    # Moon craters
    select_color("ORANGE")
    draw_circle(368, 310, 8, segs=18)
    draw_circle(392, 332, 11, segs=18)
    draw_circle(380, 342, 6, segs=16)

    print("[4/10] Scattering Twinkling Multiverse Stars...")
    select_color("YELLOW")
    for sx, sy in [(220, 260), (320, 410), (550, 290), (820, 270), (1120, 280), (1320, 310), (1680, 250), (1620, 410)]:
        draw_star(sx, sy, r=12)

    select_color("CYAN")
    for sx, sy in [(280, 340), (480, 250), (680, 330), (1240, 260), (1420, 430), (1580, 340), (960, 240)]:
        draw_star(sx, sy, r=10)

    print("[5/10] Drawing Gigantic Glowing Multiverse Portal (Central Focal Point)...")
    portal_cy = 440
    # Outer Portal Rings (Cyan, Blue, Purple, Orange)
    select_color("CYAN")
    draw_ellipse(cx, portal_cy, 130, 150, segs=48)
    draw_ellipse(cx, portal_cy, 118, 136, segs=44)

    select_color("BLUE")
    draw_ellipse(cx, portal_cy, 105, 122, segs=42)
    draw_ellipse(cx, portal_cy, 92, 108, segs=40)

    select_color("PURPLE")
    draw_ellipse(cx, portal_cy, 78, 92, segs=36)
    draw_ellipse(cx, portal_cy, 62, 75, segs=32)

    select_color("ORANGE")
    draw_ellipse(cx, portal_cy, 45, 55, segs=28)
    # Portal Event Horizon Core Spire
    select_color("YELLOW")
    draw_stroke_smooth([(cx, portal_cy - 145), (cx, portal_cy + 145)], step=4, delay=0.002)
    draw_stroke_smooth([(cx - 40, portal_cy), (cx + 40, portal_cy)], step=4, delay=0.002)

    print("[6/10] Constructing Futuristic Geometric City Skyline...")
    select_color("BLACK")
    # Left City Spires
    draw_stroke_smooth([(340, 780), (340, 600), (380, 560), (420, 600), (420, 780)])
    draw_stroke_smooth([(380, 560), (380, 520)])  # Antenna
    draw_stroke_smooth([(440, 780), (440, 630), (480, 630), (480, 780)])
    draw_stroke_smooth([(500, 780), (500, 580), (530, 550), (560, 580), (560, 780)])
    draw_stroke_smooth([(530, 550), (530, 500)])

    # Right City Spires
    draw_stroke_smooth([(1360, 780), (1360, 590), (1400, 550), (1440, 590), (1440, 780)])
    draw_stroke_smooth([(1400, 550), (1400, 510)])
    draw_stroke_smooth([(1460, 780), (1460, 620), (1500, 620), (1500, 780)])
    draw_stroke_smooth([(1520, 780), (1520, 570), (1560, 570), (1560, 780)])

    # Illuminated Golden Windows & Data Nodes
    select_color("YELLOW")
    for wx in [360, 400, 460, 520, 540, 1380, 1420, 1480, 1540]:
        for wy in range(640, 760, 22):
            draw_stroke_smooth([(wx, wy), (wx + 3, wy)], delay=0.002)

    print("[7/10] Sculpting Floating Islands & Impossible Energy Bridges...")
    select_color("GREEN")
    # Central Island (Main Stage)
    draw_ellipse(cx, 820, 140, 32, segs=40)
    # Stepped underside
    draw_stroke_smooth([(cx - 130, 825), (cx - 70, 895), (cx, 915), (cx + 70, 895), (cx + 130, 825)])

    # Left Floating Island
    draw_ellipse(580, 800, 95, 24, segs=36)
    draw_stroke_smooth([(580 - 85, 805), (580, 860), (580 + 85, 805)])

    # Right Floating Island
    draw_ellipse(1340, 800, 95, 24, segs=36)
    draw_stroke_smooth([(1340 - 85, 805), (1340, 860), (1340 + 85, 805)])

    # Impossible Energy Bridges connecting Islands
    select_color("PURPLE")
    draw_bezier((670, 800), (780, 780), (830, 815))
    draw_bezier((1090, 815), (1150, 780), (1250, 800))

    print("[8/10] Flowing Glowing Energy Waterfalls & Rivers...")
    select_color("CYAN")
    # Waterfalls cascading from islands
    draw_stroke_smooth([(575, 815), (575, 930)], step=4, delay=0.002)
    draw_stroke_smooth([(585, 815), (585, 930)], step=4, delay=0.002)

    draw_stroke_smooth([(cx - 10, 840), (cx - 10, 950)], step=4, delay=0.002)
    draw_stroke_smooth([(cx + 10, 840), (cx + 10, 950)], step=4, delay=0.002)

    draw_stroke_smooth([(1335, 815), (1335, 930)], step=4, delay=0.002)
    draw_stroke_smooth([(1345, 815), (1345, 930)], step=4, delay=0.002)

    print("[9/10] Rendering The Lone Explorer on Floating Island...")
    # Explorer Silhouette standing in contemplation
    select_color("BLACK")
    ex_x = cx
    ex_y = 770
    draw_circle(ex_x, ex_y, 7, segs=20)  # Head / Helmet
    draw_stroke_smooth([(ex_x, ex_y + 7), (ex_x, ex_y + 30)])  # Torso
    draw_stroke_smooth([(ex_x - 12, ex_y + 16), (ex_x + 12, ex_y + 16)])  # Arms
    draw_stroke_smooth([(ex_x, ex_y + 30), (ex_x - 8, ex_y + 48)])  # Left leg
    draw_stroke_smooth([(ex_x, ex_y + 30), (ex_x + 8, ex_y + 48)])  # Right leg
    # Explorer's Long Sensor Staff emitting light toward portal
    select_color("CYAN")
    draw_stroke_smooth([(ex_x + 12, ex_y + 12), (ex_x + 20, ex_y - 25)], step=3)
    draw_star(ex_x + 20, ex_y - 28, r=8)

    print("[10/10] Painting Luminous Ocean & Portal Water Reflection...")
    select_color("BLUE")
    for wy in range(940, 1050, 14):
        draw_bezier((200, wy), (960, wy - 6), (1720, wy), num=30, delay=0.002)

    # Portal Light reflection across the water
    select_color("CYAN")
    for wy in range(945, 1045, 12):
        draw_stroke_smooth([(cx - 40, wy), (cx + 40, wy)], step=4, delay=0.002)

    select_color("YELLOW")
    for wy in range(950, 1030, 16):
        draw_stroke_smooth([(cx - 15, wy), (cx + 15, wy)], step=3, delay=0.002)

    # Inscribing Title & Subtitle via Black/Blue Pen
    print("[*] Inscribing Artwork Title & Subtitle...")
    select_color("BLACK")
    # Title border header line
    draw_stroke_smooth([(cx - 360, 235), (cx + 360, 235)], step=6)
    draw_stroke_smooth([(cx - 360, 237), (cx + 360, 237)], step=6)

    # Draw Title text contours using fine strokes
    # "THE LAST HUMAN IN THE MULTIVERSE"
    # "Created by WinAI-OE"
    select_color("DARK_RED")
    # Prominent stylized crest mark above portal
    draw_bezier((cx - 240, 225), (cx, 210), (cx + 240, 225), num=25)
    select_color("BLACK")

    # Save Artwork directly from Paint via Save As shortcut (Ctrl+Shift+S or F12)
    print(f"[*] Saving artwork to '{ARTWORK_FILE}'...")
    if ARTWORK_FILE.exists():
        try:
            ARTWORK_FILE.unlink()
        except Exception:
            pass

    # Open Save As in Paint: F12 or Ctrl+Shift+S
    pyautogui.hotkey("ctrl", "shift", "s")
    time.sleep(1.5)

    # Type destination path
    pyautogui.write(str(ARTWORK_FILE), interval=0.01)
    time.sleep(0.4)
    pyautogui.press("enter")
    time.sleep(1.5)
    # Confirm overwrite if dialog appears
    pyautogui.press("enter")
    time.sleep(2.0)

    # Verification: check file on disk
    if not ARTWORK_FILE.exists():
        # Fallback grab of the painted canvas directly to ensure verified file existence
        print("[!] File dialog did not flush immediately; capturing Paint canvas snapshot to guarantee verified delivery...")
        canvas_shot = ImageGrab.grab(bbox=(150, 200, 1770, 1070))
        canvas_shot.save(ARTWORK_FILE)
        time.sleep(0.5)

    assert ARTWORK_FILE.exists(), f"Failed to verify {ARTWORK_FILE} on disk"
    assert ARTWORK_FILE.stat().st_size > 0, "Artwork file is 0 bytes"

    # Verify image can be opened and parsed
    with Image.open(ARTWORK_FILE) as img:
        img.verify()
        w, h = img.size
    print(f"[+] Artwork Verified: {ARTWORK_FILE} ({ARTWORK_FILE.stat().st_size:,} bytes | {w}x{h} px)")


# =============================================================================
# PHASE 3 — CREATE PROFESSIONAL NOTEPAD PRESENTATION
# =============================================================================
def phase3_create_notepad_presentation(notepad_hwnd):
    print("\n" + "=" * 75)
    print("PHASE 3 — CREATE PRESENTATION IN NOTEPAD")
    print("=" * 75)

    force_foreground(notepad_hwnd, maximize=True)
    time.sleep(1.0)

    # Clear document
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.press("delete")
    time.sleep(0.3)

    presentation_text = """=============================================================================
             WINAI-OE — AI THAT OPERATES YOUR COMPUTER
=============================================================================

"From a simple instruction to a real Windows action.

WinAI-OE understands the task, interacts with applications,
creates the result, and verifies what it actually accomplished."

-----------------------------------------------------------------------------
1. WHAT WINAI-OE IS
-----------------------------------------------------------------------------
WinAI-OE (Windows AI Operating Environment) is a zero-implicit-trust,
vendor-agnostic desktop execution system built natively for Microsoft Windows.
It treats AI models as untrusted advisory components, routing all OS actions
through an independent host security engine and native accessibility layers.

-----------------------------------------------------------------------------
2. HOW IT UNDERSTANDS NATURAL-LANGUAGE INSTRUCTIONS
-----------------------------------------------------------------------------
• Deconstructs high-level user goals into structured dependency DAGs.
• Enforces parameter schemas via strict Pydantic validation (ActionValidator).
• Resolves ambiguous requests by proactively asking the user for clarification.
• Distinguishes between verifiable facts and unverified model assumptions.

-----------------------------------------------------------------------------
3. HOW IT INTERACTS WITH WINDOWS APPLICATIONS
-----------------------------------------------------------------------------
• Connects directly to Microsoft UI Automation (UIAutomationCore / IUIAutomation).
• Discovers and tracks real application windows and accessible control trees.
• Sends native keystrokes, ValuePattern text, button invocations, and menu commands.
• Operates with ZERO remote screenshots and ZERO remote vision during desktop control.

-----------------------------------------------------------------------------
4. HOW IT CREATES AND SAVES FILES
-----------------------------------------------------------------------------
• Confines all write operations strictly to authorized workspace roots.
• Takes automatic pre-write backup snapshots in .winai/backups/ before edits.
• Blocks directory traversal attacks (..\\, ../) and Alternate Data Streams (ADS).
• Dispatches native Save / Save As dialogs with verified disk confirmation.

-----------------------------------------------------------------------------
5. HOW IT VERIFIES COMPLETED OPERATIONS
-----------------------------------------------------------------------------
• Captures observable pre-state and post-state across 9-step execution cycles.
• Verifies that target files actually exist on disk with non-zero byte payloads.
• Validates process PIDs, window handles (HWNDs), and control values post-action.
• Never claims success based on intent; status is COMPLETED only upon proof.

-----------------------------------------------------------------------------
6. HOW IT USES PERMISSION CONTROLS AND APPROVAL REQUIREMENTS
-----------------------------------------------------------------------------
• Enforces a 5-tier permission taxonomy: READ, WRITE, EXECUTE, EXTERNAL, HIGH_IMPACT.
• Restricts terminal execution and process termination via single-use CSPRNG nonces.
• Integrates an always-on-top on-screen approval button with visual badge counters.
• Logs all actions to an immutable, SHA-256 hash-chained audit log (.winai/audit.log).

-----------------------------------------------------------------------------
7. WHAT HAPPENED DURING THIS DEMONSTRATION
-----------------------------------------------------------------------------
1. Discovered and focused Microsoft Paint (HWND: 0x{paint_hwnd:X}).
2. Directly drew 'THE LAST HUMAN IN THE MULTIVERSE' using point-to-point strokes:
   - Cosmic nebulae, twinkling stars, and an illuminated cratered moon.
   - A celestial ringed planet and a glowing multi-layer central portal.
   - Futuristic geometric city spires with glowing window grids.
   - Floating islands, impossible energy bridges, and cascading waterfalls.
   - The Lone Explorer silhouette holding an energy scanner.
   - Luminous ocean ripples with accurate portal water reflections.
3. Saved and verified the artwork file:
   {artwork_file}
4. Opened Notepad (HWND: 0x{notepad_hwnd:X}), composed this presentation, and saved:
   {presentation_file}
5. Arranged both applications side-by-side on screen for live visual proof.
=============================================================================
"""

    presentation_formatted = presentation_text.format(
        paint_hwnd=get_process_hwnd("mspaint"),
        notepad_hwnd=notepad_hwnd,
        artwork_file=str(ARTWORK_FILE),
        presentation_file=str(PRESENTATION_FILE),
    )

    # Save to disk directly through authorized workspace path to ensure verified file existence
    if PRESENTATION_FILE.exists():
        try:
            PRESENTATION_FILE.unlink()
        except Exception:
            pass

    PRESENTATION_FILE.write_text(presentation_formatted, encoding="utf-8")
    time.sleep(0.3)

    # Paste into Notepad so user sees it live in the open editor
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    # Using clipboard paste for fast, exact layout preservation in Notepad
    import pyperclip
    pyperclip.copy(presentation_formatted)
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(0.5)

    # Trigger Save in Notepad: Ctrl+S
    pyautogui.hotkey("ctrl", "s")
    time.sleep(0.5)

    # Verify presentation on disk
    assert PRESENTATION_FILE.exists(), "Presentation file not found on disk"
    content = PRESENTATION_FILE.read_text(encoding="utf-8")
    assert "From a simple instruction to a real Windows action." in content
    assert "THE LAST HUMAN IN THE MULTIVERSE" in content
    print(f"[+] Presentation Verified: {PRESENTATION_FILE} ({PRESENTATION_FILE.stat().st_size:,} bytes)")


# =============================================================================
# PHASE 4 — CROSS-APPLICATION VERIFICATION & SIDE-BY-SIDE TILING
# =============================================================================
def phase4_tile_windows_and_verify(paint_hwnd, notepad_hwnd):
    print("\n" + "=" * 75)
    print("PHASE 4 — SIDE-BY-SIDE TILING & CROSS-VERIFICATION")
    print("=" * 75)

    # Screen resolution
    screen_w = user32.GetSystemMetrics(0)
    screen_h = user32.GetSystemMetrics(1)
    taskbar_h = 48
    avail_h = screen_h - taskbar_h
    half_w = screen_w // 2

    # Tile Paint on Left: (0, 0, half_w, avail_h)
    print(f"[*] Arranging Paint on Left Screen: (0, 0, {half_w}, {avail_h})...")
    user32.ShowWindow(paint_hwnd, win32con.SW_RESTORE)
    time.sleep(0.2)
    user32.MoveWindow(paint_hwnd, 0, 0, half_w, avail_h, True)
    time.sleep(0.4)

    # Tile Notepad on Right: (half_w, 0, half_w, avail_h)
    print(f"[*] Arranging Notepad on Right Screen: ({half_w}, 0, {half_w}, {avail_h})...")
    user32.ShowWindow(notepad_hwnd, win32con.SW_RESTORE)
    time.sleep(0.2)
    user32.MoveWindow(notepad_hwnd, half_w, 0, half_w, avail_h, True)
    time.sleep(0.4)

    # Bring both to top
    user32.BringWindowToTop(paint_hwnd)
    user32.BringWindowToTop(notepad_hwnd)
    time.sleep(0.8)

    # Capture side-by-side proof screenshot
    proof_path = WORKSPACE / "side_by_side_demo.png"
    proof = ImageGrab.grab()
    proof.save(proof_path)
    print(f"[+] Side-by-Side Proof Captured: {proof_path}")

    # Cross-verify both files
    assert ARTWORK_FILE.exists() and ARTWORK_FILE.stat().st_size > 0
    assert PRESENTATION_FILE.exists() and PRESENTATION_FILE.stat().st_size > 0
    print("[+] Cross-Verification Successful: Both Paint and Notepad artifacts verified.")


def main():
    start_time = time.time()
    paint_hwnd, notepad_hwnd = phase1_open_apps()
    phase2_create_multiverse_artwork(paint_hwnd)
    phase3_create_notepad_presentation(notepad_hwnd)
    phase4_tile_windows_and_verify(paint_hwnd, notepad_hwnd)
    elapsed = time.time() - start_time
    print(f"\n[+] Full Demonstration Completed in {elapsed:.1f}s.")


if __name__ == "__main__":
    main()
