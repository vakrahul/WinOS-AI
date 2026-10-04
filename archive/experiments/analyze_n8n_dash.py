import base64
import httpx
from src.storage.credential_vault import CredentialVault

v = CredentialVault()
key = v.get_credential("gemini")

with open("n8n_workflows_page.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={key}"
prompt = (
    "Look at this screenshot of the n8n dashboard in Chrome. "
    "1. Is the n8n Workflows dashboard loaded and visible? "
    "2. What instance, workspace, or account name is shown on the top-left or sidebar? "
    "3. What buttons are visible (e.g. 'Create Workflow', 'Import from File', '+')? "
    "4. What workflows or folders are listed on the page?"
)

payload = {
    "contents": [{
        "role": "user",
        "parts": [
            {"text": prompt},
            {"inline_data": {"mime_type": "image/png", "data": b64}}
        ]
    }]
}
res = httpx.post(url, json=payload, timeout=25.0)
print(res.json()["candidates"][0]["content"]["parts"][0]["text"])
