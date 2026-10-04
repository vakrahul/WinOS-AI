import asyncio
from src.windows_integration.vision_automation import VisualButtonInteractor
from src.storage.credential_vault import CredentialVault

async def main():
    hwnd = 7735086
    v = CredentialVault()
    key = v.get_credential("gemini")
    interactor = VisualButtonInteractor()

    print("Locating and clicking 'Editor' tab button in n8n...")
    res = await interactor.identify_and_click_button(
        hwnd=hwnd,
        button_label="Editor",
        gemini_api_key=key,
    )
    print("Result:", res)

if __name__ == "__main__":
    asyncio.run(main())
