import base64
import httpx
from src.storage.credential_vault import CredentialVault

v = CredentialVault()
key = v.get_credential("gemini")

with open("paint_toolbar.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={key}"
prompt = (
    "Look at this paint_toolbar.png image (dimensions 1400x160). "
    "Find the button that has the label 'Brushes' with a brush icon. "
    "What are the exact (X, Y) integer coordinates of the center of this button? "
    "Also find the (X, Y) of the 'Pencil' icon. Return both exact (X, Y)."
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
