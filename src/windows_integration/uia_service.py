"""Genuine Windows UI Automation and Accessibility Integration (Phase 64-66).

Connects directly to the Windows UI Automation subsystem (IUIAutomation / UIAutomationCore.dll)
via native accessibility wrappers. Provides real window discovery, accessible element inspection,
control pattern invocations (ValuePattern, InvokePattern, TextPattern), and keyboard dispatch.
Zero simulation, zero remote computer vision, zero mock data.
"""

import ctypes
import re
import time
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
import uiautomation as auto

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32


class UIElementInfo(BaseModel):
    name: str
    control_type: str
    automation_id: str
    is_enabled: bool = True
    value: Optional[str] = None
    bounding_rect: Optional[List[int]] = None  # [left, top, right, bottom]


class UIAutomationService:
    """Interfaces directly with real Windows UI Automation and accessibility element trees."""

    def __init__(self):
        # Configure uiautomation engine defaults
        auto.SetGlobalSearchTimeout(3.0)

    def find_window(
        self,
        window_title: str,
        class_name: Optional[str] = None,
        timeout_seconds: float = 5.0,
    ) -> Optional[auto.WindowControl]:
        """Locate an actual top-level application window on Windows desktop."""
        escaped_title = re.escape(window_title)
        regex_pattern = f"(?i).*{escaped_title}.*"

        # Search desktop windows (depth 3 to catch dialogs and child windows)
        if class_name:
            win = auto.WindowControl(
                searchDepth=3,
                ClassName=class_name,
                RegexName=regex_pattern,
            )
        else:
            win = auto.WindowControl(
                searchDepth=3,
                RegexName=regex_pattern,
            )

        if win.Exists(maxSearchSeconds=timeout_seconds):
            return win

        # Fallback: Check standard exact Name match
        win_exact = auto.WindowControl(searchDepth=3, Name=window_title)
        if win_exact.Exists(maxSearchSeconds=0.5):
            return win_exact

        return None

    def focus_window(self, window_title: str, timeout_seconds: float = 3.0) -> bool:
        """Bring target application window to foreground and assign active input focus."""
        win = self.find_window(window_title, timeout_seconds=timeout_seconds)
        if not win:
            return False

        try:
            hwnd = win.NativeWindowHandle
            if hwnd:
                cur_thread = kernel32.GetCurrentThreadId()
                fg_hwnd = user32.GetForegroundWindow()
                fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
                user32.AttachThreadInput(cur_thread, fg_thread, True)
                user32.keybd_event(0x12, 0, 0, 0)  # ALT down
                user32.keybd_event(0x12, 0, 2, 0)  # ALT up
                user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                user32.BringWindowToTop(hwnd)
                user32.SetForegroundWindow(hwnd)
                user32.AttachThreadInput(cur_thread, fg_thread, False)

            win.SetActive()
            win.SetFocus()
            time.sleep(0.2)
            return True
        except Exception:
            return False

    def wait_for_window(self, window_title: str, timeout_seconds: float = 5.0) -> bool:
        """Wait until an actual application window exists on the desktop."""
        win = self.find_window(window_title, timeout_seconds=timeout_seconds)
        return win is not None

    def inspect_window_elements(
        self,
        window_title: str,
        max_depth: int = 3,
        timeout_seconds: float = 3.0,
    ) -> List[UIElementInfo]:
        """Enumerate genuine accessible UI Automation elements for an active window."""
        win = self.find_window(window_title, timeout_seconds=timeout_seconds)
        if not win:
            return []

        elements: List[UIElementInfo] = []
        try:
            for child, depth in auto.WalkControl(win, maxDepth=max_depth):
                val = None
                try:
                    vp = child.GetValuePattern()
                    if vp:
                        val = vp.Value
                    elif child.GetTextPattern():
                        val = child.GetTextPattern().DocumentRange.GetText(-1)
                except Exception:
                    pass

                rect_list = None
                try:
                    r = child.BoundingRectangle
                    if r:
                        rect_list = [r.left, r.top, r.right, r.bottom]
                except Exception:
                    pass

                elements.append(
                    UIElementInfo(
                        name=child.Name or "",
                        control_type=child.ControlTypeName or "Unknown",
                        automation_id=child.AutomationId or "",
                        is_enabled=child.IsEnabled,
                        value=val,
                        bounding_rect=rect_list,
                    )
                )
        except Exception:
            pass

        return elements

    def locate_control(
        self,
        window_title: str,
        name: Optional[str] = None,
        control_type: Optional[str] = None,
        automation_id: Optional[str] = None,
        timeout_seconds: float = 3.0,
    ) -> Optional[auto.Control]:
        """Locate an actual accessible control within the window by name, type, or ID."""
        win = self.find_window(window_title, timeout_seconds=timeout_seconds)
        if not win:
            return None

        # Try direct search using uiautomation control queries
        for child, _ in auto.WalkControl(win, maxDepth=6):
            match = True
            if name is not None:
                child_name = child.Name or ""
                if name.lower() not in child_name.lower():
                    match = False
            if control_type is not None:
                ctype = child.ControlTypeName or ""
                # Match either "EditControl" or "Edit"
                norm_target = control_type.lower().replace("control", "")
                norm_actual = ctype.lower().replace("control", "")
                if norm_target != norm_actual:
                    match = False
            if automation_id is not None:
                if (child.AutomationId or "") != automation_id:
                    match = False

            if match:
                return child

        return None

    def read_text_value(
        self,
        window_title: str,
        automation_id: Optional[str] = None,
        name: Optional[str] = None,
        control_type: Optional[str] = None,
    ) -> Optional[str]:
        """Read real text from an accessible control or document editor."""
        win = self.find_window(window_title)
        if not win:
            return None

        target_control: Optional[auto.Control] = None

        if automation_id or name or control_type:
            target_control = self.locate_control(
                window_title=window_title,
                name=name,
                control_type=control_type,
                automation_id=automation_id,
            )

        if not target_control:
            # Check default DocumentControl / EditControl in window
            doc = win.DocumentControl(searchDepth=4)
            if doc.Exists(0.2):
                target_control = doc
            else:
                edit = win.EditControl(searchDepth=4)
                if edit.Exists(0.2):
                    target_control = edit

        if not target_control:
            return None

        try:
            vp = target_control.GetValuePattern()
            if vp and vp.Value:
                return vp.Value
        except Exception:
            pass

        try:
            tp = target_control.GetTextPattern()
            if tp:
                return tp.DocumentRange.GetText(-1)
        except Exception:
            pass

        # Fallback to Name property (e.g. for TextControls or Buttons)
        return target_control.Name

    def set_text_value(
        self,
        window_title: str,
        text: str,
        automation_id: Optional[str] = None,
        name: Optional[str] = None,
        control_type: Optional[str] = None,
        clear_first: bool = False,
    ) -> bool:
        """Set text into an accessible edit/document control using ValuePattern or SendKeys."""
        win = self.find_window(window_title)
        if not win:
            return False

        self.focus_window(window_title)

        target_control: Optional[auto.Control] = None
        if automation_id or name or control_type:
            target_control = self.locate_control(
                window_title=window_title,
                name=name,
                control_type=control_type,
                automation_id=automation_id,
            )

        if not target_control:
            # Fallback to primary editor
            doc = win.DocumentControl(searchDepth=4)
            if doc.Exists(0.2):
                target_control = doc
            else:
                edit = win.EditControl(searchDepth=4)
                if edit.Exists(0.2):
                    target_control = edit

        if not target_control:
            return False

        try:
            target_control.SetFocus()
            time.sleep(0.1)

            # 1. Attempt native ValuePattern SetValue
            try:
                vp = target_control.GetValuePattern()
                if vp:
                    vp.SetValue(text)
                    return True
            except Exception:
                pass

            # 2. Native keyboard dispatch
            if clear_first:
                target_control.SendKeys("{Ctrl}a{Delete}")
                time.sleep(0.05)

            target_control.SendKeys(text)
            return True
        except Exception:
            return False

    def send_keys_to_window(self, window_title: str, keys: str, wait_time: float = 0.05) -> bool:
        """Focus the application window and dispatch genuine keystrokes."""
        win = self.find_window(window_title)
        if not win:
            return False

        self.focus_window(window_title)
        try:
            win.SendKeys(keys, interval=wait_time)
            return True
        except Exception:
            return False

    def invoke_button(
        self,
        window_title: str,
        automation_id: Optional[str] = None,
        name: Optional[str] = None,
    ) -> bool:
        """Invoke or click a real Windows button via UIA InvokePattern or physical click."""
        control = self.locate_control(
            window_title=window_title,
            name=name,
            control_type="Button",
            automation_id=automation_id,
        )

        if not control:
            # Check without control_type constraint in case it's a ListItem or MenuItem
            control = self.locate_control(
                window_title=window_title,
                name=name,
                automation_id=automation_id,
            )

        if not control:
            return False

        try:
            ip = control.GetInvokePattern()
            if ip:
                ip.Invoke()
                return True
        except Exception:
            pass

        try:
            control.Click()
            return True
        except Exception:
            return False

    def click_control(
        self,
        window_title: str,
        name: Optional[str] = None,
        control_type: Optional[str] = None,
        automation_id: Optional[str] = None,
    ) -> bool:
        """Click an accessible UI control."""
        control = self.locate_control(
            window_title=window_title,
            name=name,
            control_type=control_type,
            automation_id=automation_id,
        )
        if not control:
            return False

        try:
            control.Click()
            return True
        except Exception:
            return False

    def select_menu_item(self, window_title: str, menu_path: str) -> bool:
        """Navigate and select real application menu hierarchy (e.g. 'File -> Save As...')."""
        win = self.find_window(window_title)
        if not win:
            return False

        self.focus_window(window_title)
        parts = [p.strip() for p in menu_path.split("->")]

        for part in parts:
            item = self.locate_control(window_title=window_title, name=part)
            if not item:
                # Try accelerator if common
                if part.lower() == "save":
                    win.SendKeys("{Ctrl}s")
                    return True
                elif part.lower() == "open":
                    win.SendKeys("{Ctrl}o")
                    return True
                return False

            try:
                ip = item.GetInvokePattern()
                if ip:
                    ip.Invoke()
                else:
                    item.Click()
                time.sleep(0.3)
            except Exception:
                item.Click()
                time.sleep(0.3)

        return True

    def wait_for_control(
        self,
        window_title: str,
        name: Optional[str] = None,
        control_type: Optional[str] = None,
        automation_id: Optional[str] = None,
        timeout_seconds: float = 5.0,
    ) -> bool:
        """Poll until an accessible control (or window) appears."""
        start = time.time()
        while time.time() - start < timeout_seconds:
            if name is None and control_type is None and automation_id is None:
                win = self.find_window(window_title, timeout_seconds=0.5)
                if win:
                    return True
            else:
                ctrl = self.locate_control(
                    window_title=window_title,
                    name=name,
                    control_type=control_type,
                    automation_id=automation_id,
                    timeout_seconds=0.5,
                )
                if ctrl:
                    return True
            time.sleep(0.2)
        return False
