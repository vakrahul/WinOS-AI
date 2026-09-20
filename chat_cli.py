"""Interactive CLI Chat and Task Execution Environment.

Allows the user to interactively chat, inspect files, and execute tasks
using their configured Gemini model (or any provider) under strict host security policies.
"""

import asyncio
import sys
from pathlib import Path

from src.orchestrator.unified_workspace import UnifiedWorkspace
from src.providers.base import ChatMessage
from src.security.policy_engine import PolicyDecision


async def run_interactive_session():
    workspace_root = Path.cwd().resolve()
    print("=" * 65)
    print("   WINDOWS AI OPERATING ENVIRONMENT (WinAI-OE) — CLI WORKSPACE")
    print(f"   Authorized Workspace: {workspace_root}")
    print("=" * 65)

    ws = UnifiedWorkspace(workspace_root=workspace_root)
    # Initialize providers with user's encrypted DPAPI vault
    ws.provider_registry.initialize_from_vault()

    if "gemini" in ws.provider_registry._providers:
        active_provider_id = "gemini"
        active_provider = ws.provider_registry.get_provider("gemini")
        print(f"[*] Active Provider: Google Gemini ({active_provider.get_capabilities().model_name})")
    else:
        active_provider_id = "mock"
        active_provider = ws.provider_registry.get_provider("mock")
        print("[*] Active Provider: Mock Provider (Offline Test Mode)")

    print("[*] Security Policy: STRICT (Human approval required for file writes/commands)")
    print("[*] Context Brain: 4-Tier Memory Active (Working, Episodic, Semantic, Project)")
    print("Type your message or task below. Type 'exit' or 'quit' to end.\n")

    history = []

    while True:
        try:
            user_input = input("You > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("[*] Session terminated. Goodbye!")
                break

            print("\nAI Thinking...", end="\r", flush=True)

            # 1. Assemble context from memory brain
            context = ws.brain.assemble_context(query=user_input, max_tokens=2048)

            # 2. Build messages
            messages = [
                ChatMessage(role="system", content=f"You are WinAI assistant. Project context:\n{context}"),
            ] + history + [ChatMessage(role="user", content=user_input)]

            # 3. Complete inference
            response = await active_provider.complete(messages=messages)
            history.append(ChatMessage(role="user", content=user_input))
            history.append(ChatMessage(role="assistant", content=response.content))

            # Record in working memory
            ws.brain.working.record_observation(f"User: {user_input} -> Response: {response.content[:80]}")

            print(f"AI ({active_provider.get_capabilities().model_name}) >\n{response.content}\n")

            # 4. Check if tools are proposed
            if response.tool_calls:
                for tc in response.tool_calls:
                    print(f"\n[!] Tool Proposal Detected: {tc.tool_name}")
                    eval_result = ws.policy_engine.evaluate_action(
                        tool_name=tc.tool_name,
                        arguments=tc.arguments,
                        session_id="cli_session",
                        agent_id="agt_cli",
                    )

                    if eval_result.decision == PolicyDecision.REQUIRE_APPROVAL:
                        print(f"    Target: {eval_result.target_resource}")
                        print(f"    Risk: {eval_result.risk_tier.value}")
                        print(f"    Reason: {eval_result.reason}")
                        choice = input("    Authorize this action? [y/N]: ").strip().lower()
                        if choice == "y":
                            print("    [+] Authorized by user. Executing...")
                        else:
                            print("    [-] Action blocked by user.")
                    elif eval_result.decision == PolicyDecision.ALLOW:
                        print(f"    [+] Automatically allowed by workspace policy: {tc.tool_name}")
                    else:
                        print(f"    [-] BLOCKED by Policy Engine: {eval_result.reason}")

        except (KeyboardInterrupt, EOFError):
            print("\n[*] Exiting...")
            break
        except Exception as e:
            print(f"\n[Error] {e}\n")


if __name__ == "__main__":
    asyncio.run(run_interactive_session())
