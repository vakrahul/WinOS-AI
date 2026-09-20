"""Controlled Windows Automation Task: Open Chrome, Navigate to X, Read First Tweet.

Executes under strict user authorization and security policy.
Summarizes the detected tweet using Gemini 3.1 Flash-Lite.
"""

import asyncio
from pathlib import Path

from src.providers.gemini_adapter import GeminiAdapter
from src.providers.base import ChatMessage
from src.security.policy_engine import SecurityPolicyEngine, PolicyDecision
from src.storage.credential_vault import CredentialVault
from src.windows_integration.browser_service import BrowserService


async def main():
    print("=" * 65)
    print("   WINDOWS AI OPERATING ENVIRONMENT — BROWSER TASK EXECUTION")
    print("   Task: Open Google Chrome -> Navigate to x.com -> Read First Tweet")
    print("=" * 65)

    # 1. Security Policy Evaluation
    policy_engine = SecurityPolicyEngine(workspace_root=Path.cwd().resolve(), require_approvals=True)
    eval_result = policy_engine.evaluate_action(
        tool_name="browser_open_x",
        arguments={"url": "https://x.com"},
        session_id="task_session",
        agent_id="agt_browser",
    )

    print("\n[SECURITY AUTHORIZATION REQUIRED]")
    print(f"  Tool:   browser_open_x")
    print(f"  Target: {eval_result.target_resource}")
    print(f"  Risk:   {eval_result.risk_tier.value}")
    print(f"  Reason: {eval_result.reason}")

    choice = input("\nAuthorize launching Google Chrome and navigating to X? [y/N]: ").strip().lower()
    if choice != "y":
        print("[-] Operation denied by user. Halting execution.")
        return

    print("\n[+] Authorization granted. Launching Google Chrome on your desktop...")
    browser = BrowserService()

    # Launch Chrome visibly so the user sees it open
    res = await browser.open_x_and_read_first_tweet(headless=False, timeout_ms=35000)

    print("\n" + "=" * 65)
    print("   TASK EXECUTION RESULTS")
    print("=" * 65)
    print(f"URL Visited: {res.url}")
    print(f"Page Title:  {res.page_title}")

    if res.first_post_text:
        print(f"\n[Author/Account]: {res.author or 'Unknown'}")
        print(f"[First Tweet Text]:\n{res.first_post_text}")

        # Send to Gemini 3.1 Flash-Lite for contextual explanation
        vault = CredentialVault()
        gemini_key = vault.get_credential("gemini")
        if gemini_key:
            print("\n[*] Sending extracted tweet to Gemini 3.1 Flash-Lite for analysis...")
            gemini = GeminiAdapter(api_key=gemini_key, model_name="gemini-3.1-flash-lite")
            prompt = (
                f"You are the Windows AI Operating Environment assistant. "
                f"The user tasked you to read the first tweet from X. Here is what was extracted:\n\n"
                f"Author: {res.author}\n"
                f"Content: {res.first_post_text}\n\n"
                f"Please provide a concise 2-sentence summary of this tweet for the user."
            )
            analysis = await gemini.complete([ChatMessage(role="user", content=prompt)])
            print(f"\nGemini 3.1 Flash-Lite Analysis:\n{analysis.content}")
    else:
        print(f"\n[Notice]: {res.notes}")
        if "login" in (res.notes or "").lower():
            print("Tip: X (Twitter) requested a login prompt. If you log into your X account in Chrome, future runs will read your personal feed directly.")


if __name__ == "__main__":
    asyncio.run(main())
