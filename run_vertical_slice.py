"""Runnable entry point for testing the Phase 10 Vertical Slice directly."""
import asyncio
import httpx
from src.orchestrator.config import get_config
from src.orchestrator.main import create_app
import uvicorn


async def main():
    config = get_config()
    print(f"[*] Starting WinAI-OE Vertical Slice Orchestrator on {config.host}:{config.port}...")
    server = uvicorn.Server(
        config=uvicorn.Config(
            app=create_app(config),
            host=config.host,
            port=config.port,
            log_level="info",
        )
    )
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
