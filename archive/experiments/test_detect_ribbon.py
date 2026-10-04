import cv2
from src.windows_integration.vision_automation import DynamicVisionDetector

screen = DynamicVisionDetector.capture_fullscreen()
buttons = DynamicVisionDetector.find_toolbar_tools(screen, ribbon_y_max=200)

print(f"Detected {len(buttons)} button contours in the toolbar:")
# Sort by X coordinate
buttons.sort(key=lambda b: b["center_x"])
for b in buttons:
    x, y, w, h = b["box"]
    print(f"Tool at Physical ({b['center_x']}, {b['center_y']}) -> Size {w}x{h}")
