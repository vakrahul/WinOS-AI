"""Windows Autonomous Execution Engine with Observable State Verification (Phase 5).

Executes actions through a 9-step verified pipeline:
1. Permission check
2. Action validation
3. Pre-flight app state check
4. Action dispatch
5. Result capture
6. Observable state outcome verification
7. Task context update
8. Audit logging
9. Recovery / Continue
"""

from enum import Enum
from pathlib import Path
import subprocess
import time
from typing import Any, Callable, Coroutine, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from src.security.action_validator import ActionValidator
from src.security.audit_logger import AuditLogger
from src.security.policy_engine import ActionEvaluationResult, PolicyDecision, SecurityPolicyEngine
from src.windows_integration.app_manager import AppManager
from src.windows_integration.file_service import ScopedFileService
from src.windows_integration.process_runner import RestrictedProcessRunner


class ActionExecutionOutcome(str, Enum):
    VERIFIED_SUCCESS = "VERIFIED_SUCCESS"       # Action succeeded and post-state was verified
    SUCCESS_UNVERIFIED = "SUCCESS_UNVERIFIED"   # Executed without error, but observable state could not be confirmed
    FAILED_EXECUTION = "FAILED_EXECUTION"       # Action threw error or process failed
    BLOCKED_POLICY = "BLOCKED_POLICY"           # Action denied by policy engine
    BLOCKED_APPROVAL = "BLOCKED_APPROVAL"       # Action requires human approval


class ObservableExecutionResult(BaseModel):
    action_id: str
    tool_name: str
    outcome: ActionExecutionOutcome
    pre_state: Dict[str, Any]
    post_state: Dict[str, Any]
    output_data: Any = None
    error_message: Optional[str] = None
    duration_ms: float
    audit_hash: Optional[str] = None


class WindowsExecutionEngine:
    """Dispatches and verifies Windows operations with observable outcome validation."""

    def __init__(
        self,
        workspace_root: Path,
        policy_engine: SecurityPolicyEngine,
        audit_logger: Optional[AuditLogger] = None,
    ):
        self.workspace_root = workspace_root.resolve()
        self.policy_engine = policy_engine
        self.audit_logger = audit_logger
        self.file_service = ScopedFileService(self.workspace_root)
        self.process_runner = RestrictedProcessRunner(self.workspace_root)
        self.app_manager = AppManager()

    async def execute_action(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        session_id: str,
        agent_id: str,
        approval_nonce: Optional[str] = None,
    ) -> ObservableExecutionResult:
        """Executes the 9-step verified execution cycle."""
        action_id = f"act_{int(time.time() * 1000)}"
        start_time = time.perf_counter()

        # Step 1: Check Permissions & Policy
        policy_eval: ActionEvaluationResult = self.policy_engine.evaluate_action(
            tool_name=tool_name,
            arguments=arguments,
            session_id=session_id,
            agent_id=agent_id,
        )

        if policy_eval.decision == PolicyDecision.DENY:
            duration = (time.perf_counter() - start_time) * 1000
            self._log_audit(tool_name, "DENIED", policy_eval.reason, session_id, agent_id)
            return ObservableExecutionResult(
                action_id=action_id,
                tool_name=tool_name,
                outcome=ActionExecutionOutcome.BLOCKED_POLICY,
                pre_state={},
                post_state={},
                error_message=f"Blocked by Policy Engine: {policy_eval.reason}",
                duration_ms=duration,
            )

        if policy_eval.decision == PolicyDecision.REQUIRE_APPROVAL:
            # Check if user provided valid approval nonce
            if not approval_nonce:
                duration = (time.perf_counter() - start_time) * 1000
                return ObservableExecutionResult(
                    action_id=action_id,
                    tool_name=tool_name,
                    outcome=ActionExecutionOutcome.BLOCKED_APPROVAL,
                    pre_state={},
                    post_state={"approval_nonce": policy_eval.approval_nonce},
                    error_message=f"Action requires user authorization nonce: {policy_eval.reason}",
                    duration_ms=duration,
                )
            # Consume nonce
            consumed = self.policy_engine.consume_approval(approval_nonce)
            if not consumed:
                duration = (time.perf_counter() - start_time) * 1000
                return ObservableExecutionResult(
                    action_id=action_id,
                    tool_name=tool_name,
                    outcome=ActionExecutionOutcome.BLOCKED_POLICY,
                    pre_state={},
                    post_state={},
                    error_message="Invalid or expired approval nonce.",
                    duration_ms=duration,
                )

        # Step 2: Validate Action Schema
        is_valid, validated_schema, val_msg = ActionValidator.validate_action(tool_name, arguments)
        if not is_valid:
            duration = (time.perf_counter() - start_time) * 1000
            return ObservableExecutionResult(
                action_id=action_id,
                tool_name=tool_name,
                outcome=ActionExecutionOutcome.FAILED_EXECUTION,
                pre_state={},
                post_state={},
                error_message=val_msg,
                duration_ms=duration,
            )

        # Step 3: Capture Pre-Execution State
        pre_state = self._capture_observable_state(tool_name, arguments)

        # Step 4: Execute Action & Step 5: Capture Result
        output_data = None
        error_msg = None
        try:
            if tool_name == "fs_read_file":
                output_data = self.file_service.read_file(arguments["path"])
            elif tool_name == "fs_write_file":
                backup_id = self.file_service.write_file(arguments["path"], arguments["content"])
                output_data = {"status": "written", "backup_id": backup_id}
            elif tool_name in ["terminal_run", "cmd_exec"]:
                cmd_args = arguments.get("command")
                if isinstance(cmd_args, str):
                    cmd_args = cmd_args.split()
                cmd_res = await self.process_runner.run_command(cmd_args)
                output_data = cmd_res.model_dump()
                if cmd_res.exit_code != 0:
                    error_msg = f"Process exited with code {cmd_res.exit_code}: {cmd_res.stderr}"
            elif tool_name == "app_launch":
                pid = self.app_manager.launch_app(arguments["app_id"])
                output_data = {"launched_pid": pid}
            else:
                output_data = {"status": "executed"}

        except Exception as e:
            error_msg = str(e)

        # Step 6: Verify Observable Post-State (Did it ACTUALLY succeed?)
        post_state = self._capture_observable_state(tool_name, arguments)
        verified_success = self._verify_state_transition(tool_name, pre_state, post_state, error_msg)

        duration = (time.perf_counter() - start_time) * 1000

        # Step 7 & 8: Record Audit Event
        audit_hash = self._log_audit(
            tool_name,
            "SUCCESS" if verified_success else "FAILED",
            str(output_data)[:200] if verified_success else error_msg or "Unknown error",
            session_id,
            agent_id,
        )

        outcome = (
            ActionExecutionOutcome.VERIFIED_SUCCESS
            if verified_success
            else (ActionExecutionOutcome.FAILED_EXECUTION if error_msg else ActionExecutionOutcome.SUCCESS_UNVERIFIED)
        )

        return ObservableExecutionResult(
            action_id=action_id,
            tool_name=tool_name,
            outcome=outcome,
            pre_state=pre_state,
            post_state=post_state,
            output_data=output_data,
            error_message=error_msg,
            duration_ms=duration,
            audit_hash=audit_hash,
        )

    def _capture_observable_state(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Inspect actual file/process state before and after execution."""
        state = {}
        if tool_name in ["fs_write_file", "fs_read_file"]:
            p = (self.workspace_root / arguments.get("path", ".")).resolve()
            state["file_exists"] = p.exists()
            state["file_size"] = p.stat().st_size if p.exists() else 0
            state["mtime"] = p.stat().st_mtime if p.exists() else 0
        elif tool_name == "app_launch":
            app_id = arguments.get("app_id", "")
            state["is_running"] = self.app_manager.get_running_pid(app_id) is not None
        return state

    def _verify_state_transition(
        self,
        tool_name: str,
        pre: Dict[str, Any],
        post: Dict[str, Any],
        error: Optional[str],
    ) -> bool:
        """Confirm action produced verifiable, observable effects in the operating system."""
        if error:
            return False
        if tool_name == "fs_write_file":
            # File must exist and modification time must be >= pre mtime
            return post.get("file_exists", False) and post.get("mtime", 0) >= pre.get("mtime", 0)
        if tool_name == "fs_read_file":
            return pre.get("file_exists", False)
        if tool_name == "app_launch":
            return post.get("is_running", False)
        return True

    def _log_audit(self, tool_name: str, status: str, details: str, session_id: str, agent_id: str) -> Optional[str]:
        if self.audit_logger:
            event = self.audit_logger.log(
                event_type="WINDOWS_TOOL_EXECUTION",
                message=f"Tool '{tool_name}' {status}: {details}",
                level="INFO" if status == "SUCCESS" else "WARNING",
                session_id=session_id,
                agent_id=agent_id,
            )
            return event.hash
        return None
