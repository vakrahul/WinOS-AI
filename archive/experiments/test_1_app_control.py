import subprocess
import time
from src.windows_integration.app_manager import AppManager

manager = AppManager()
results = {}

# 1. Chrome
try:
    # Check if already running
    p = subprocess.run(["powershell", "-NoProfile", "-Command", "Get-Process chrome -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id"], capture_output=True, text=True)
    if p.stdout.strip():
        results["Google Chrome"] = f"Running (Existing PID: {p.stdout.strip()})"
    else:
        pid = manager.launch_app("chrome")
        results["Google Chrome"] = f"Launched Successfully (PID: {pid})"
except Exception as e:
    results["Google Chrome"] = f"Error: {e}"

# 2. Notepad
try:
    pid = manager.launch_app("notepad")
    time.sleep(1.0)
    results["Notepad"] = f"Launched Successfully (PID: {pid})"
except Exception as e:
    results["Notepad"] = f"Error: {e}"

# 3. VS Code
try:
    pid = manager.launch_app("vscode")
    time.sleep(2.0)
    results["VS Code"] = f"Launched Successfully (PID: {pid})"
except Exception as e:
    results["VS Code"] = f"Error: {e}"

print("=== TEST 1 APPLICATION CONTROL RESULTS ===")
for app, status in results.items():
    print(f"[*] {app}: {status}")
