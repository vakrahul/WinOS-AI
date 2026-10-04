import uiautomation as auto

paint_win = auto.WindowControl(searchDepth=1, ClassName="TopLevelWindowForOverflowList", SubName="Paint")
if not paint_win.Exists(1):
    paint_win = auto.WindowControl(searchDepth=1, SubName="Paint")

if paint_win.Exists(2):
    print("Found Paint Window:", paint_win.Name)
    # Search for buttons
    buttons = []
    for item in auto.WalkTree(paint_win):
        c = item[0]
        if c.ControlType == auto.ControlType.ButtonControl:
            name = c.Name or ""
            if name:
                buttons.append(name)
    print("Found Paint Buttons:", buttons[:25])
else:
    print("Paint window not found.")
