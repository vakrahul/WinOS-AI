"""Packaged WinAI-OE Windows service entry point.

This module is the main entry for the PyInstaller-packaged WinAI-OE
executable (WinAI-OE.exe). It boots the FastAPI orchestrator — policy
engine, execution engine, UI Automation, system intelligence — in the
executable's own process and serves the loopback API.
"""

import asyncio
import sys
from pathlib import Path

# When frozen, project modules are bundled; ensure local tree resolves.
if getattr(sys, "frozen", False):
    _base = Path(sys.executable).resolve().parent
    for _candidate in (_base, _base / "_internal"):
        if str(_candidate) not in sys.path:
            sys.path.insert(0, str(_candidate))
else:
    _root = Path(__file__).resolve().parent
    if str(_root) not in sys.path:
        sys.path.insert(0, str(_root))

from src.orchestrator.config import get_config  # noqa: E402
from src.orchestrator.main import create_app  # noqa: E402
import uvicorn  # noqa: E402


def main() -> None:
    config = get_config()
    print(f"[*] WinAI-OE packaged service starting on {config.host}:{config.port} ...")
    print(f"[*] Executable: {sys.executable}")
    server_config = uvicorn.Config(
        app=create_app(config),
        host=config.host,
        port=config.port,
        log_level="info",
    )
    server = uvicorn.Server(server_config)
    asyncio.run(server.serve())


if __name__ == "__main__":
    main()
