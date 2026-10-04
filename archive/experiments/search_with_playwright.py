import asyncio
import json
from playwright.async_api import async_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

QUERIES = [
    "AI Engineer Intern jobs Hyderabad linkedin",
    "Machine Learning Intern jobs Hyderabad indeed",
    "Python Backend Intern jobs Hyderabad internshala",
    "Remote AI ML internships 2026 wellfound",
]

async def search_bing():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-first-run", "--no-default-browser-check"],
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        for query in QUERIES:
            print(f"Searching Bing for: '{query}'...")
            try:
                await page.goto(f"https://www.bing.com/search?q={query}", timeout=25000, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)

                # Extract search result items
                items = page.locator("li.b_algo")
                count = await items.count()
                print(f"Found {count} results for {query}")

                for i in range(min(count, 5)):
                    item = items.nth(i)
                    title_loc = item.locator("h2 a")
                    snippet_loc = item.locator(".b_caption p, .b_snippet")
                    
                    if await title_loc.count() > 0:
                        title = await title_loc.first.inner_text()
                        url = await title_loc.first.get_attribute("href") or ""
                        snippet = ""
                        if await snippet_loc.count() > 0:
                            snippet = await snippet_loc.first.inner_text()
                        
                        results.append({
                            "query": query,
                            "title": title,
                            "url": url,
                            "snippet": snippet,
                        })
            except Exception as e:
                print(f"Error on query {query}: {e}")

        await browser.close()
    
    with open("verified_search_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Total verified search results collected: {len(results)}")

if __name__ == "__main__":
    asyncio.run(search_bing())
