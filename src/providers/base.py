"""Base abstractions for LLM providers (Zone 4 boundary)."""
from abc import ABC, abstractmethod
from typing import Any, AsyncIterator, Dict, List, Optional
from pydantic import BaseModel, Field


class ModelCapabilities(BaseModel):
    """Declared capabilities of an AI model."""
    provider_name: str
    model_name: str
    context_window: int = Field(default=8192, ge=1024)
    supports_streaming: bool = True
    supports_tools: bool = True
    supports_vision: bool = False


class ChatMessage(BaseModel):
    """Canonical chat message format across all providers."""
    role: str = Field(pattern="^(system|user|assistant|tool)$")
    content: str
    tool_call_id: Optional[str] = None
    name: Optional[str] = None


class ToolCallProposal(BaseModel):
    """Structured tool call proposed by a model (Untrusted Input)."""
    id: str
    tool_name: str
    arguments: Dict[str, Any]


class ProviderResponse(BaseModel):
    """Normalized response from any provider."""
    content: str
    model_name: str
    tool_calls: List[ToolCallProposal] = Field(default_factory=list)
    finish_reason: str = "stop"
    usage: Dict[str, int] = Field(default_factory=dict)


class BaseModelProvider(ABC):
    """Abstract base class for all AI provider adapters."""

    @abstractmethod
    async def complete(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> ProviderResponse:
        """Execute a complete inference request."""
        pass

    @abstractmethod
    async def stream(
        self,
        messages: List[ChatMessage],
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> AsyncIterator[str]:
        """Stream tokens asynchronously."""
        pass

    @abstractmethod
    def get_capabilities(self) -> ModelCapabilities:
        """Return declared capabilities."""
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Return True if provider endpoint is reachable and authenticated."""
        pass
