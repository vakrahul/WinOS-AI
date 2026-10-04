import base64
import httpx
from src.storage.credential_vault import CredentialVault

v = CredentialVault()
key = v.get_credential("gemini")

with open("linkedin_email_posts.png", "rb") as f:
    b64 = base64.b64encode(f.read()).decode("utf-8")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite:generateContent?key={key}"
prompt = (
    "Look at this screenshot of LinkedIn Posts search. "
    "Examine all visible hiring posts in the main feed: "
    "For each post: "
    "\n1. Poster Name & Company/Headline "
    "\n2. Role being hired (e.g. AI Intern, ML Engineer) "
    "\n3. Time posted (e.g. 1h, 1d) "
    "\n4. EXACT Recruiter or contact email address mentioned in the post (e.g. xxx@yyy.com) "
    "\n5. Short summary of the hiring requirements."
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
res = httpx.post(url, json=payload, timeout=30.0)
if res.status_code == 200:
    print(res.json()["candidates"][0]["content"]["parts"][0]["text"])
else:
    print("Error:", res.status_code, res.text[:200])
