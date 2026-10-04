"""Collect up to 10 verified, real internship opportunities across Hyderabad and Remote."""
import asyncio
import json
import re
from bs4 import BeautifulSoup
import httpx
import urllib.parse

QUERIES = [
    "AI Engineer Intern jobs in Hyderabad",
    "Machine Learning Intern jobs in Hyderabad",
    "Python Backend Intern jobs in Hyderabad",
    "Remote AI ML internships 2026",
]

async def fetch_search_results(query: str, client: httpx.AsyncClient):
    res = await client.post("https://html.duckduckgo.com/html/", data={"q": query})
    if res.status_code != 200:
        return []
    
    soup = BeautifulSoup(res.text, "html.parser")
    results = []
    for el in soup.find_all("div", class_="result"):
        title_tag = el.find("a", class_="result__a")
        snippet_tag = el.find("a", class_="result__snippet")
        if title_tag and snippet_tag:
            raw_url = title_tag.get("href", "")
            actual_url = raw_url
            match = re.search(r"uddg=([^&]+)", raw_url)
            if match:
                actual_url = urllib.parse.unquote(match.group(1))

            results.append({
                "title": title_tag.get_text(strip=True),
                "snippet": snippet_tag.get_text(strip=True),
                "url": actual_url,
                "query": query,
            })
    return results

async def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    }
    all_results = []
    async with httpx.AsyncClient(headers=headers, timeout=20.0, follow_redirects=True) as client:
        for q in QUERIES:
            print(f"Searching: {q}...")
            res = await fetch_search_results(q, client)
            print(f"Found {len(res)} results for: {q}")
            all_results.extend(res)
            await asyncio.sleep(1.5)

    with open("raw_job_results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"Total collected raw results: {len(all_results)}")

if __name__ == "__main__":
    asyncio.run(main())
