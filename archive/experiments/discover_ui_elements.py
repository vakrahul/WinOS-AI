import uiautomation as auto

win = auto.ControlFromHandle(15076238)
print("Paint Window by Handle:", win.Name, win.ClassName)
count = 0
for item in auto.WalkTree(win):
    c = item[0]
    name = c.Name or ""
    rect = c.BoundingRectangle
    if name and rect.width() > 0:
        print(f"[{c.ControlType}] '{name}' -> ({rect.left}, {rect.top}, {rect.right}, {rect.bottom})")
        count += 1
        if count >= 30:
            break
print(f"Total controls listed: {count}")
