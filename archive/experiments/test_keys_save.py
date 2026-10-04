import subprocess
import time
import uiautomation as auto

proc = subprocess.Popen(["notepad.exe"])
time.sleep(2.0)

try:
    win = auto.WindowControl(searchDepth=3, RegexName="(?i).*notepad.*")
    win.SetActive()
    time.sleep(0.5)
    
    doc = win.DocumentControl(searchDepth=4)
    if not doc.Exists(0.5):
        doc = win.EditControl(searchDepth=4)
    doc.SetFocus()
    time.sleep(0.2)
    doc.SendKeys("Hello Rahul{Enter}")
    time.sleep(0.5)
    
    print("Sending Ctrl+s...")
    doc.SendKeys("{Ctrl}s")
    time.sleep(2.0)
    
    print("Enumerating top-level desktop windows:")
    for w in auto.GetRootControl().GetChildren():
        if w.ControlTypeName == "WindowControl":
            print("  Window:", w.Name, "| Class:", w.ClassName)
finally:
    proc.terminate()
