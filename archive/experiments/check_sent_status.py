import base64
import httpx
from src.storage.credential_vault import CredentialVault

v = CredentialVault()
key = v.get_credential("gemini")

with open("gmail_sent_confirmation.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={key}"
prompt = (
    "Look at this screenshot of Gmail. "
    "Has the email been sent? Look at the bottom left corner for the notification banner "
    "like 'Message sent' or 'Undo'. Describe the exact status and notification shown."
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
print("Status:", res.status_code)
if res.status_code == 200:
    print(res.json()["candidates"][0]["content"]["parts"][0]["text"])
else:
    print("Error:", res.text)
