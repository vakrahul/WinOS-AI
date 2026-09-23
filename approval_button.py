"""Launch the WinAI-OE on-screen approval button (always-on-top overlay).

Double-click this file (or run `python approval_button.py`) while the
orchestrator is running. A small badge stays visible on any screen and
turns red with a count whenever an approval is pending; click it to
Approve / Deny.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from src.windows_integration.approval_overlay import main

if __name__ == "__main__":
    main()
