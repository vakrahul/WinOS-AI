import uiautomation as auto

chrome_win = auto.WindowControl(searchDepth=1, ClassName="Chrome_WidgetWin_1", SubName="Google Chrome")
if chrome_win.Exists(maxSearchSeconds=3):
    print("Chrome Window Title:", chrome_win.Name)
    # Find all TabItem controls
    tabs = chrome_win.GetChildren()
    for item in auto.WalkTree(chrome_win):
        c = item[0]
        if c.ControlType == auto.ControlType.TabItemControl or "Tab" in c.ClassName:
            print("Found Tab:", c.Name, "| ControlType:", c.ControlType)
