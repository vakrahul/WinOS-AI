"""Categorized Permission System and Action Risk Evaluator (Phase 10).

Enforces strict taxonomy across 5 operation classes:
- READ: Low risk, ambient permitted within workspace.
- WRITE: Medium risk, atomic backups enabled.
- EXECUTE: High risk, sub-process sandboxed.
- EXTERNAL: Critical risk, single-use CSPRNG approval mandatory.
- HIGH_IMPACT: Critical risk, permanent state warning.
"""

from enum import Enum
import fnmatch
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from src.security.policy_engine import ActionEvaluationResult, PolicyDecision, RiskTier


class OperationCategory(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    EXECUTE = "EXECUTE"
    EXTERNAL = "EXTERNAL"
    HIGH_IMPACT = "HIGH_IMPACT"


class CategorizedPermissionRule(BaseModel):
    category: OperationCategory
    tool_name: str
    target_pattern: str
    requires_human_approval: bool
    risk_tier: RiskTier
    description: str


class CategorizedPermissionManager:
    """Manages explicit permission categories and maps tool proposals to policy decisions."""

    DEFAULT_RULES: List[CategorizedPermissionRule] = [
        # READ
        CategorizedPermissionRule(
            category=OperationCategory.READ,
            tool_name="fs_read_file",
            target_pattern="*",
            requires_human_approval=False,
            risk_tier=RiskTier.LOW,
            description="Read file contents within workspace",
        ),
        CategorizedPermissionRule(
            category=OperationCategory.READ,
            tool_name="fs_list_files",
            target_pattern="*",
            requires_human_approval=False,
            risk_tier=RiskTier.LOW,
            description="List directory structure",
        ),
        CategorizedPermissionRule(
            category=OperationCategory.READ,
            tool_name="browser_read_page",
            target_pattern="*",
            requires_human_approval=False,
            risk_tier=RiskTier.LOW,
            description="Read visible text from accessible web page",
        ),
        # WRITE
        CategorizedPermissionRule(
            category=OperationCategory.WRITE,
            tool_name="fs_write_file",
            target_pattern="*",
            requires_human_approval=False,  # Within workspace with atomic rollback
            risk_tier=RiskTier.MEDIUM,
            description="Create or edit file in approved workspace",
        ),
        CategorizedPermissionRule(
            category=OperationCategory.WRITE,
            tool_name="create_project",
            target_pattern="*",
            requires_human_approval=False,
            risk_tier=RiskTier.MEDIUM,
            description="Scaffold new project directory",
        ),
        # EXECUTE
        CategorizedPermissionRule(
            category=OperationCategory.EXECUTE,
            tool_name="terminal_run",
            target_pattern="*",
            requires_human_approval=True,
            risk_tier=RiskTier.HIGH,
            description="Run command inside restricted subprocess",
        ),
        CategorizedPermissionRule(
            category=OperationCategory.EXECUTE,
            tool_name="app_launch",
            target_pattern="*",
            requires_human_approval=False,  # Whitelisted apps like chrome/notepad
            risk_tier=RiskTier.LOW,
            description="Launch approved Windows application",
        ),
        # EXTERNAL
        CategorizedPermissionRule(
            category=OperationCategory.EXTERNAL,
            tool_name="send_email",
            target_pattern="*",
            requires_human_approval=True,
            risk_tier=RiskTier.CRITICAL,
            description="Send an email via authenticated account",
        ),
        CategorizedPermissionRule(
            category=OperationCategory.EXTERNAL,
            tool_name="submit_application",
            target_pattern="*",
            requires_human_approval=True,
            risk_tier=RiskTier.CRITICAL,
            description="Submit web application form",
        ),
        CategorizedPermissionRule(
            category=OperationCategory.EXTERNAL,
            tool_name="deploy_project",
            target_pattern="*",
            requires_human_approval=True,
            risk_tier=RiskTier.CRITICAL,
            description="Deploy code to external server or preview host",
        ),
        # HIGH_IMPACT
        CategorizedPermissionRule(
            category=OperationCategory.HIGH_IMPACT,
            tool_name="fs_delete_file",
            target_pattern="*",
            requires_human_approval=True,
            risk_tier=RiskTier.CRITICAL,
            description="Delete file or directory",
        ),
        CategorizedPermissionRule(
            category=OperationCategory.HIGH_IMPACT,
            tool_name="modify_security_policy",
            target_pattern="*",
            requires_human_approval=True,
            risk_tier=RiskTier.CRITICAL,
            description="Change system permissions or security thresholds",
        ),
    ]

    def __init__(self, workspace_root: Path):
        self.workspace_root = workspace_root.resolve()
        self.rules = self.DEFAULT_RULES.copy()

    def classify_and_evaluate(
        self,
        tool_name: str,
        target_resource: str,
        session_tainted: bool = False,
    ) -> Tuple[OperationCategory, ActionEvaluationResult]:
        """Classify tool proposal into its permission category and evaluate policy."""
        # Match rule
        matched_rule = next((r for r in self.rules if r.tool_name == tool_name), None)

        if not matched_rule:
            return OperationCategory.HIGH_IMPACT, ActionEvaluationResult(
                decision=PolicyDecision.DENY,
                risk_tier=RiskTier.CRITICAL,
                reason=f"Unrecognized tool '{tool_name}' has no registered permission category (fail-closed).",
                target_resource=target_resource,
            )

        category = matched_rule.category

        # If session is tainted by untrusted inputs, escalate all WRITE/EXECUTE to REQUIRE_APPROVAL
        must_approve = matched_rule.requires_human_approval or (
            session_tainted and category in [OperationCategory.WRITE, OperationCategory.EXECUTE]
        )

        decision = PolicyDecision.REQUIRE_APPROVAL if must_approve else PolicyDecision.ALLOW
        reason = (
            f"Operation categorized as [{category.value}]. Human approval required."
            if must_approve
            else f"Operation categorized as [{category.value}]. Permitted under workspace ambient policy."
        )

        return category, ActionEvaluationResult(
            decision=decision,
            risk_tier=matched_rule.risk_tier,
            reason=reason,
            target_resource=target_resource,
        )
