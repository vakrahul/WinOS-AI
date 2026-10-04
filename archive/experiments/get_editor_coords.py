import base64
import httpx
from src.storage.credential_vault import CredentialVault

v = CredentialVault()
key = v.get_credential("gemini")

with open("post_click_1789920699972.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={key}"
prompt = (
    "In this screenshot (post_click_1789920699972.png), look at the interface. "
    "Earlier you noted: 'You can switch to the actual canvas by clicking the Editor tab located at the top center of the screen'. "
    "What are the exact (X, Y) pixel coordinates of that 'Editor' tab? "
    "Also what are the coordinates of the large 'Add first step...' button?"
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
