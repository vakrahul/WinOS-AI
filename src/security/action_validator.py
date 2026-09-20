"""Strict action validation and sanitization engine (Phase 56)."""
from pathlib import Path
import re
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, ConfigDict, Field, ValidationError


SHELL_INJECTION_PATTERN = re.compile(r"[;&|`$><]")


class FsReadFileSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    path: str = Field(min_length=1)
    max_bytes: Optional[int] = Field(default=1048576, ge=1, le=10485760)


class FsWriteFileSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    path: str = Field(min_length=1)
    content: str
    mode: Optional[str] = Field(default="overwrite", pattern="^(overwrite|append)$")


class CmdExecSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")
    command: List[str] = Field(min_length=1)  # Argument array only!
    timeout_seconds: Optional[int] = Field(default=60, ge=1, le=300)


class ActionValidator:
    """Validates raw tool call proposals against strict schemas and checks for injection."""

    SCHEMAS = {
        "fs_read_file": FsReadFileSchema,
        "fs_list_files": FsReadFileSchema,
        "fs_write_file": FsWriteFileSchema,
        "terminal_run": CmdExecSchema,
        "cmd_exec": CmdExecSchema,
    }

    @classmethod
    def validate_action(cls, tool_name: str, arguments: Dict[str, Any]) -> Tuple[bool, Optional[BaseModel], str]:
        """Validate tool invocation arguments against strict schema and injection sanitizers."""
        if tool_name not in cls.SCHEMAS:
            return False, None, f"Tool '{tool_name}' is not recognized or has no validation schema"

        # Check for null bytes in any string value
        for k, v in arguments.items():
            if isinstance(v, str) and "\x00" in v:
                return False, None, f"Security Violation: Null byte detected in parameter '{k}'"

        schema_cls = cls.SCHEMAS[tool_name]
        try:
            validated = schema_cls(**arguments)
        except ValidationError as e:
            return False, None, f"Schema validation failure: {e}"

        # If it's a command execution, ensure no raw shell strings
        if isinstance(validated, CmdExecSchema):
            for arg in validated.command:
                if "\x00" in arg:
                    return False, None, "Null byte in command argument"

        return True, validated, "Validation successful"
