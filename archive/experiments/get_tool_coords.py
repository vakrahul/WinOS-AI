import base64
import httpx
from src.storage.credential_vault import CredentialVault

v = CredentialVault()
key = v.get_credential("gemini")

with open("paint_toolbar.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={key}"
prompt = (
    "In this Paint toolbar image (1400x160), look closely at the ribbon. "
    "List the (X, Y) pixel coordinates of: "
    "1. The Pencil tool (it looks like a classic pencil). "
    "2. The Brushes tool (it looks like paint brushes in a holder with text 'Brushes'). "
    "3. The Eraser tool. "
    "Be precise with the horizontal X pixel location."
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
