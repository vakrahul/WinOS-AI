"""FastAPI AI Orchestrator service (Zone 2).

Provides loopback REST and WebSocket interfaces for desktop client communication,
mediating between UI, AI providers, and host security policies.
"""

import asyncio
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, status
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

    @app.get("/api/v1/config")
    async def get_system_config():
        return {
            "environment": app_config.environment,
            "security_level": app_config.security_level,
            "workspace_root": str(app_config.workspace_root),
            "default_provider": app_config.default_provider,
            "default_model": app_config.default_model,
        }

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


app = create_app()
