import asyncio
from pathlib import Path
import subprocess
import time
from src.orchestrator.task_dispatcher import AutonomousTaskDispatcher

# Clean any existing notepad
subprocess.run(["powershell", "-NoProfile", "-Command", "Stop-Process -Name notepad -Force -ErrorAction SilentlyContinue"])
time.sleep(1.0)

async def run_test():
    tmp_ws = Path("C:/Users/RAHUL/AppData/Local/Temp/test_diag_ws")
    tmp_ws.mkdir(parents=True, exist_ok=True)
    d = AutonomousTaskDispatcher(workspace_root=tmp_ws)
    save_file = "test_run_direct.txt"
    target = tmp_ws / save_file
    if target.exists():
        target.unlink()

    prompt = f"Open Notepad, type Hello Rahul, and save it as {save_file}."
    res = await d.execute_task(prompt)
    print("STATUS:", res.status)
    print("SUMMARY:", ascii(res.summary))
    print("EVIDENCE:")
    for e in res.observable_evidence:
        print("  -", e)
    print("FILE EXISTS:", target.exists())
    if target.exists():
        print("CONTENT:", target.read_text(encoding="utf-8"))

asyncio.run(run_test())
