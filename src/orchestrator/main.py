"""FastAPI AI Orchestrator service (Zone 2).

Provides loopback REST and WebSocket interfaces for desktop client communication,
mediating between UI, AI providers, and host security policies.
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from src.orchestrator.config import AppConfig, get_config
from src.providers.base import BaseModelProvider, ChatMessage, ProviderResponse
from src.providers.registry import ProviderRegistry
from src.security.policy_engine import (
    ActionEvaluationResult,
    PolicyDecision,
    SecurityPolicyEngine,
)
from src.storage.credential_vault import CredentialVault
from src.windows_integration.system_app_scanner import SystemAppScanner
from src.windows_integration.app_manager import AppManager
from src.orchestrator.task_dispatcher import AutonomousTaskDispatcher


class LaunchAppPayload(BaseModel):
    app_id: str


class TaskDispatchPayload(BaseModel):
    task: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    provider: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.7
    max_tokens: int = 1024


class ApprovalResponsePayload(BaseModel):
    approval_nonce: str
    user_decision: str = Field(pattern="^(APPROVED|DENIED)$")


def create_app(config: Optional[AppConfig] = None) -> FastAPI:
    """Application factory for FastAPI orchestrator."""
    app_config = config or get_config()
    app = FastAPI(
        title=app_config.app_name,
        version=app_config.app_version,
        docs_url="/docs",
    )

    # Initialize subsystems
    policy_engine = SecurityPolicyEngine(
        workspace_root=app_config.workspace_root,
        require_approvals=(app_config.security_level.value == "strict"),
    )
    
    vault = CredentialVault()
    provider_registry = ProviderRegistry(vault=vault)
    provider_registry.initialize_from_vault()

    def get_target_provider(requested_provider: Optional[str] = None) -> BaseModelProvider:
        if requested_provider:
            return provider_registry.get_provider(requested_provider)
        if app_config.environment == "testing":
            return provider_registry.get_provider(app_config.default_provider)
        if "gemini" in provider_registry._providers:
            return provider_registry.get_provider("gemini")
        return provider_registry.get_provider(app_config.default_provider)

    @app.get("/health")
    async def health_check():
        active_prov = get_target_provider()
        provider_healthy = await active_prov.health_check()
        return {
            "status": "healthy" if provider_healthy else "degraded",
            "app": app_config.app_name,
            "version": app_config.app_version,
            "environment": app_config.environment,
            "provider": active_prov.get_capabilities().provider_name,
            "provider_healthy": provider_healthy,
            "configured_providers": provider_registry.list_providers(),
        }

    app_scanner = SystemAppScanner()
    app_manager = AppManager()

    @app.get("/", response_class=HTMLResponse)
    @app.get("/dashboard", response_class=HTMLResponse)
    async def get_dashboard():
        html_path = Path(__file__).parent / "dashboard.html"
        if html_path.exists():
            return html_path.read_text(encoding="utf-8")
        return "<h1>WinAI Dashboard Active</h1>"

    @app.get("/api/v1/system/apps")
    async def get_system_apps():
        apps = app_scanner.scan_all_applications()
        stats = app_scanner.get_summary_stats()
        return {"stats": stats, "applications": [a.model_dump() for a in apps]}

    @app.post("/api/v1/system/apps/launch")
    async def launch_application(payload: LaunchAppPayload):
        try:
            pid = app_manager.launch_app(payload.app_id)
            return {"status": "success", "app_id": payload.app_id, "pid": pid}
        except Exception as e:
            import subprocess
            subprocess.run(["cmd", "/c", "start", payload.app_id], shell=False)
            return {"status": "dispatched", "app_id": payload.app_id}

    @app.get("/api/v1/config")
    async def get_system_config():
        return app_config.public_config_dict()

    dispatcher = AutonomousTaskDispatcher(workspace_root=app_config.workspace_root)

    @app.post("/api/v1/tasks/dispatch")
    async def dispatch_task(payload: TaskDispatchPayload):
        result = await dispatcher.execute_task(payload.task)
        return result.model_dump()

    @app.post("/api/v1/chat", response_model=ProviderResponse)
    async def complete_chat(request: ChatRequest):
        provider = get_target_provider(request.provider)
        response = await provider.complete(
            messages=request.messages,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return response

    @app.post("/api/v1/approval/respond")
    async def respond_to_approval(payload: ApprovalResponsePayload):
        pending = policy_engine.consume_approval(payload.approval_nonce)
        if not pending:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid or expired approval nonce",
            )
        return {
            "status": "processed",
            "decision": payload.user_decision,
            "action": pending,
        }

    @app.websocket("/ws/v1/stream")
    async def websocket_stream_endpoint(websocket: WebSocket):
        await websocket.accept()
        try:
            while True:
                data = await websocket.receive_text()
                message_json = json.loads(data)
                action = message_json.get("action")

                if action == "chat":
                    raw_messages = message_json.get("messages", [])
                    req_prov = message_json.get("provider")
                    provider = get_target_provider(req_prov)
                    messages = [ChatMessage(**m) for m in raw_messages]

                    # 1. Stream tokens
                    async for token in provider.stream(messages):
                        await websocket.send_json({
                            "event": "token",
                            "data": token,
                        })

                    # 2. Check if model proposes a tool
                    complete_resp = await provider.complete(messages)
                    if complete_resp.tool_calls:
                        for tool_call in complete_resp.tool_calls:
                            # Evaluate through Policy Engine
                            eval_result = policy_engine.evaluate_action(
                                tool_name=tool_call.tool_name,
                                arguments=tool_call.arguments,
                                session_id="ws_session",
                                agent_id="agent_stream",
                            )

                            await websocket.send_json({
                                "event": "tool_proposal",
                                "tool_call": tool_call.model_dump(),
                                "policy_decision": eval_result.model_dump(),
                            })

                    await websocket.send_json({"event": "done"})

                elif action == "cancel":
                    await websocket.send_json({"event": "cancelled"})

        except WebSocketDisconnect:
            pass

    return app


def list_registered_routes(app: FastAPI) -> list:
    """Return sorted (path, methods) pairs for the registered HTTP routes."""
    entries = []
    for route in app.routes:
        path = getattr(route, "path", "")
        methods = sorted(getattr(route, "methods", set()) or set())
        if path:
            entries.append((path, methods))
    return sorted(entries)


STARTUP_ORDER = (
    "config",
    "security_policy",
    "credential_vault",
    "provider_registry",
    "system_scanner",
    "app_manager",
    "routes",
    "task_dispatcher",
)


def describe_startup_order() -> tuple:
    """Return the normative subsystem initialization order (no side effects)."""
    return STARTUP_ORDER


app = create_app()
