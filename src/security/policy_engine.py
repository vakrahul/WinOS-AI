"""Independent Host-Side Security Core & Policy Engine (Zone 1).

Evaluates untrusted model tool proposals deterministically.
Enforces workspace path confinement, blocked system locations, and human approval gates.
"""

from enum import Enum
import os
from pathlib import Path
import re
import secrets
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field


class PolicyDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


class RiskTier(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ActionEvaluationResult(BaseModel):
    decision: PolicyDecision
    risk_tier: RiskTier
    reason: str
    target_resource: Optional[str] = None
    approval_nonce: Optional[str] = None


class SecurityPolicyEngine:
    """Independent policy engine running in host execution space."""

    FORBIDDEN_SYSTEM_PATHS = [
        Path(os.environ.get("SystemRoot", "C:\\Windows")).resolve(),
        Path(os.environ.get("ProgramFiles", "C:\\Program Files")).resolve(),
        Path(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")).resolve(),
    ]

    def __init__(self, workspace_root: Path, require_approvals: bool = True):
        self.workspace_root = workspace_root.resolve()
        self.require_approvals = require_approvals
        # Pending approval nonces mapped to action details: {nonce: (tool_name, target_resource)}
        self._pending_approvals: Dict[str, Dict[str, Any]] = {}

    def is_path_confined(self, target_path: Path) -> Tuple[bool, str]:
        """Verify that target_path is canonicalized and resides strictly within workspace_root."""
        try:
            canonical_target = target_path.resolve()
        except Exception as e:
            return False, f"Failed to resolve canonical path: {e}"

        # Check for Windows Alternate Data Streams (ADS)
        raw_str = str(target_path)
        without_drive = re.sub(r"^[a-zA-Z]:", "", raw_str)
        if ":" in without_drive:
            return False, f"Alternate Data Stream (ADS) injection blocked: '{raw_str}'"

        # Check forbidden system directories
        for forbidden in self.FORBIDDEN_SYSTEM_PATHS:
            if canonical_target == forbidden or forbidden in canonical_target.parents:
                return False, f"Target path lies within forbidden system directory: '{forbidden}'"

        # Check workspace confinement
        if canonical_target != self.workspace_root and self.workspace_root not in canonical_target.parents:
            return False, f"Path traversal violation: '{canonical_target}' escapes workspace '{self.workspace_root}'"

        return True, "Path successfully verified inside workspace"

    def evaluate_action(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        session_id: str,
        agent_id: str,
    ) -> ActionEvaluationResult:
        """Deterministic policy evaluation of proposed tool invocation."""

        # 1. Inspect Filesystem Tools
        if tool_name in ["fs_read_file", "fs_list_files"]:
            rel_path = arguments.get("path") or arguments.get("file_path", ".")
            target_path = (self.workspace_root / rel_path).resolve()
            confined, reason = self.is_path_confined(target_path)
            if not confined:
                return ActionEvaluationResult(
                    decision=PolicyDecision.DENY,
                    risk_tier=RiskTier.CRITICAL,
                    reason=reason,
                    target_resource=str(target_path),
                )
            # Read-only within workspace is ALLOW
            return ActionEvaluationResult(
                decision=PolicyDecision.ALLOW,
                risk_tier=RiskTier.LOW,
                reason="Read operation confined to workspace",
                target_resource=str(target_path),
            )

        elif tool_name in ["fs_write_file", "fs_delete_file"]:
            rel_path = arguments.get("path") or arguments.get("file_path")
            if not rel_path:
                return ActionEvaluationResult(
                    decision=PolicyDecision.DENY,
                    risk_tier=RiskTier.HIGH,
                    reason="Missing target file path parameter",
                )
            target_path = (self.workspace_root / rel_path).resolve()
            confined, reason = self.is_path_confined(target_path)
            if not confined:
                return ActionEvaluationResult(
                    decision=PolicyDecision.DENY,
                    risk_tier=RiskTier.CRITICAL,
                    reason=reason,
                    target_resource=str(target_path),
                )

            if self.require_approvals:
                nonce = secrets.token_hex(32)
                self._pending_approvals[nonce] = {
                    "tool_name": tool_name,
                    "target": str(target_path),
                    "session_id": session_id,
                }
                return ActionEvaluationResult(
                    decision=PolicyDecision.REQUIRE_APPROVAL,
                    risk_tier=RiskTier.HIGH,
                    reason="File write/delete requires explicit user confirmation",
                    target_resource=str(target_path),
                    approval_nonce=nonce,
                )
            return ActionEvaluationResult(
                decision=PolicyDecision.ALLOW,
                risk_tier=RiskTier.MEDIUM,
                reason="File modification approved by ambient policy",
                target_resource=str(target_path),
            )

        # 2. Command / Terminal Execution
        elif tool_name in ["cmd_exec", "terminal_run"]:
            command = arguments.get("command") or arguments.get("cmd")
            if not command:
                return ActionEvaluationResult(
                    decision=PolicyDecision.DENY,
                    risk_tier=RiskTier.HIGH,
                    reason="No command specified",
                )

            # Command execution always requires approval
            nonce = secrets.token_hex(32)
            self._pending_approvals[nonce] = {
                "tool_name": tool_name,
                "command": command,
                "session_id": session_id,
            }
            return ActionEvaluationResult(
                decision=PolicyDecision.REQUIRE_APPROVAL,
                risk_tier=RiskTier.CRITICAL,
                reason="Terminal execution requires explicit human review",
                target_resource=str(command),
                approval_nonce=nonce,
            )

        # 3. Browser Automation Tools
        elif tool_name in ["browser_open_x", "browser_navigate"]:
            url = arguments.get("url", "https://x.com")
            if self.require_approvals:
                nonce = secrets.token_hex(32)
                self._pending_approvals[nonce] = {
                    "tool_name": tool_name,
                    "target": url,
                    "session_id": session_id,
                }
                return ActionEvaluationResult(
                    decision=PolicyDecision.REQUIRE_APPROVAL,
                    risk_tier=RiskTier.MEDIUM,
                    reason="Browser automation requires user confirmation to launch window",
                    target_resource=url,
                    approval_nonce=nonce,
                )
            return ActionEvaluationResult(
                decision=PolicyDecision.ALLOW,
                risk_tier=RiskTier.LOW,
                reason="Browser automation permitted by policy",
                target_resource=url,
            )

        # 4. Windows Desktop Application & Control Tools
        elif tool_name == "app_launch":
            app_id = arguments.get("app_id", "")
            approved_apps = {"notepad", "calc", "chrome", "vscode", "edge"}
            if app_id not in approved_apps:
                return ActionEvaluationResult(
                    decision=PolicyDecision.DENY,
                    risk_tier=RiskTier.CRITICAL,
                    reason=f"Application '{app_id}' is not in approved application whitelist.",
                    target_resource=app_id,
                )
            if self.require_approvals:
                nonce = secrets.token_hex(32)
                self._pending_approvals[nonce] = {
                    "tool_name": tool_name,
                    "target": app_id,
                    "session_id": session_id,
                }
                return ActionEvaluationResult(
                    decision=PolicyDecision.REQUIRE_APPROVAL,
                    risk_tier=RiskTier.LOW,
                    reason=f"Application launch '{app_id}' requires confirmation",
                    target_resource=app_id,
                    approval_nonce=nonce,
                )
            return ActionEvaluationResult(
                decision=PolicyDecision.ALLOW,
                risk_tier=RiskTier.LOW,
                reason=f"Application launch '{app_id}' approved by policy",
                target_resource=app_id,
            )

        elif tool_name in ["window_find", "window_focus", "window_wait_for_control"]:
            target_win = arguments.get("window_title", "")
            return ActionEvaluationResult(
                decision=PolicyDecision.ALLOW,
                risk_tier=RiskTier.LOW,
                reason="Window query/focus permitted by ambient policy",
                target_resource=target_win,
            )

        elif tool_name in [
            "window_type_text",
            "window_send_keys",
            "window_click_control",
            "window_invoke_control",
            "window_select_menu",
            "browser_select_tab",
        ]:
            target_win = arguments.get("window_title", "")
            if self.require_approvals:
                nonce = secrets.token_hex(32)
                self._pending_approvals[nonce] = {
                    "tool_name": tool_name,
                    "target": target_win,
                    "session_id": session_id,
                }
                return ActionEvaluationResult(
                    decision=PolicyDecision.REQUIRE_APPROVAL,
                    risk_tier=RiskTier.MEDIUM,
                    reason=f"Desktop UI interaction '{tool_name}' on '{target_win}' requires approval",
                    target_resource=target_win,
                    approval_nonce=nonce,
                )
            return ActionEvaluationResult(
                decision=PolicyDecision.ALLOW,
                risk_tier=RiskTier.MEDIUM,
                reason=f"Desktop UI interaction '{tool_name}' permitted by ambient policy",
                target_resource=target_win,
            )

        # 5. Windows System Intelligence & Process Management Tools
        elif tool_name in [
            "system_get_overview",
            "system_get_memory_status",
            "process_list",
            "process_get_top_consumers",
            "process_get_info",
            "window_list",
            "window_get_foreground",
            "browser_get_url",
            "browser_get_heading",
            "window_get_text",
        ]:
            return ActionEvaluationResult(
                decision=PolicyDecision.ALLOW,
                risk_tier=RiskTier.LOW,
                reason="System intelligence inspection permitted by ambient policy",
                target_resource="system",
            )

        elif tool_name == "process_close":
            pid = arguments.get("pid")
            app_name = (arguments.get("app_name") or "").lower()
            critical_names = {
                "system",
                "system idle process",
                "csrss.exe",
                "lsass.exe",
                "smss.exe",
                "services.exe",
                "explorer.exe",
                "dwm.exe",
                "wininit.exe",
            }
            if (pid is not None and pid <= 4) or app_name in critical_names:
                return ActionEvaluationResult(
                    decision=PolicyDecision.DENY,
                    risk_tier=RiskTier.CRITICAL,
                    reason="Termination of critical Windows system processes is strictly prohibited.",
                    target_resource=str(pid or app_name),
                )
            if self.require_approvals:
                nonce = secrets.token_hex(32)
                self._pending_approvals[nonce] = {
                    "tool_name": tool_name,
                    "target": str(pid or app_name),
                    "session_id": session_id,
                }
                return ActionEvaluationResult(
                    decision=PolicyDecision.REQUIRE_APPROVAL,
                    risk_tier=RiskTier.HIGH,
                    reason=f"Closing application '{app_name or pid}' requires confirmation",
                    target_resource=str(pid or app_name),
                    approval_nonce=nonce,
                )
            return ActionEvaluationResult(
                decision=PolicyDecision.ALLOW,
                risk_tier=RiskTier.MEDIUM,
                reason=f"Closing application '{app_name or pid}' permitted by policy",
                target_resource=str(pid or app_name),
            )

        # 6. Default Fail-Closed
        return ActionEvaluationResult(
            decision=PolicyDecision.DENY,
            risk_tier=RiskTier.HIGH,
            reason=f"Unrecognized or unauthorized tool: '{tool_name}'",
        )

    def consume_approval(self, nonce: str) -> Optional[Dict[str, Any]]:
        """Validate and immediately consume an approval nonce (single use)."""
        return self._pending_approvals.pop(nonce, None)

    def pending_approvals_summary(self) -> List[Dict[str, Any]]:
        """Display-safe snapshot of awaiting approvals for the local overlay UI.

        Nonces are included because the overlay (same user, loopback only) must
        present them back to /api/v1/approval/respond. Never expose this
        endpoint beyond 127.0.0.1.
        """
        summary = []
        for nonce, info in self._pending_approvals.items():
            summary.append({
                "approval_nonce": nonce,
                "tool_name": info.get("tool_name", ""),
                "target": str(info.get("target", info.get("command", ""))),
                "session_id": info.get("session_id", ""),
            })
        return summary
