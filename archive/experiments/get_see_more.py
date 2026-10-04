import base64
import httpx
from src.storage.credential_vault import CredentialVault

v = CredentialVault()
key = v.get_credential("gemini")

with open("oxastra_post_area.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={key}"
prompt = "In this cropped post image (750x500), where is the '...see more' text located? Give its exact X, Y coordinates within this 750x500 image."

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
