"""Specialized Agent Registry and Role Definitions (Phases 45-46)."""
from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class AgentRole(str, Enum):
    RESEARCHER = "researcher"
    CODER = "coder"
    FILE_ANALYST = "file_analyst"
    TEST_RUNNER = "test_runner"
    COORDINATOR = "coordinator"


class SpecializedAgent(BaseModel):
    """Definition and permission envelope of an individual specialized agent."""
    role: AgentRole
    agent_id: str
    display_name: str
    system_prompt: str
    authorized_tools: List[str]
    max_tokens: int = 4096


class AgentRegistry:
    """Registry maintaining available specialized agent definitions."""

    def __init__(self):
        self._agents: Dict[str, SpecializedAgent] = {}
        self._register_default_agents()

    def _register_default_agents(self) -> None:
        # 1. Researcher (Read-only, no file modifications or command execution)
        self.register_agent(
            SpecializedAgent(
                role=AgentRole.RESEARCHER,
                agent_id="agt_researcher",
                display_name="Context Researcher",
                system_prompt="You are a research agent. Search facts and retrieve relevant background context.",
                authorized_tools=["fs_read_file", "fs_list_files", "web_search"],
            )
        )

        # 2. Coder (Workspace file modifications)
        self.register_agent(
            SpecializedAgent(
                role=AgentRole.CODER,
                agent_id="agt_coder",
                display_name="Code Engineer",
                system_prompt="You are a software engineer. Implement precise, minimal, and tested code changes.",
                authorized_tools=["fs_read_file", "fs_write_file"],
            )
        )

        # 3. File Analyst (Directory exploration and structural analysis)
        self.register_agent(
            SpecializedAgent(
                role=AgentRole.FILE_ANALYST,
                agent_id="agt_analyst",
                display_name="Repository Analyst",
                system_prompt="You analyze project structures, schemas, and dependencies.",
                authorized_tools=["fs_list_files", "fs_read_file"],
            )
        )

        # 4. Test Runner (Restricted execution of test harnesses)
        self.register_agent(
            SpecializedAgent(
                role=AgentRole.TEST_RUNNER,
                agent_id="agt_tester",
                display_name="Automated Test Runner",
                system_prompt="You execute test suites and analyze test outputs.",
                authorized_tools=["terminal_run", "fs_read_file"],
            )
        )

    def register_agent(self, agent: SpecializedAgent) -> None:
        self._agents[agent.agent_id] = agent

    def get_agent(self, agent_id: str) -> Optional[SpecializedAgent]:
        return self._agents.get(agent_id)

    def get_by_role(self, role: AgentRole) -> Optional[SpecializedAgent]:
        for agt in self._agents.values():
            if agt.role == role:
                return agt
        return None

    def list_agents(self) -> List[SpecializedAgent]:
        return list(self._agents.values())
