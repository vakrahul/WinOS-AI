import asyncio
import json
import re
from playwright.async_api import async_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

SEARCH_TARGETS = [
    ("AI Engineer Intern", "https://www.google.com/search?q=AI+Engineer+Intern+jobs+in+Hyderabad"),
    ("Machine Learning Intern", "https://www.google.com/search?q=Machine+Learning+Intern+jobs+in+Hyderabad"),
    ("Python Backend Intern", "https://www.google.com/search?q=Python+Backend+Intern+jobs+in+Hyderabad"),
    ("Remote AI/ML Intern", "https://www.google.com/search?q=Remote+AI+ML+Internship+jobs"),
]

async def collect_real_jobs():
    collected_jobs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-first-run", "--no-default-browser-check"],
        )
        page = await browser.new_page()

        for category, url in SEARCH_TARGETS:
            print(f"[*] Navigating to: {url}...")
            try:
                await page.goto(url, timeout=30000, wait_until="domcontentloaded")
                await page.wait_for_timeout(3000)

                # Look for Google Jobs widget or search organic job links
                # Google Jobs cards typically have role="treeitem" or class "Bj9Kyf" or "iFjolb"
                job_cards = page.locator('div[jscontroller="eIu7Db"], div.PwjeAc, div[data-share-url], a:has-text("Intern")')
                card_count = await job_cards.count()
                print(f"Found {card_count} potential job elements for {category}")

                # Also grab standard organic job listings (LinkedIn, Indeed, Glassdoor, Internshala)
                organic_links = page.locator('div.g a')
                link_count = await organic_links.count()
                for i in range(min(link_count, 10)):
                    el = organic_links.nth(i)
                    title = await el.inner_text()
                    href = await el.get_attribute("href") or ""
                    if any(w in title.lower() for w in ["intern", "hiring", "job", "career"]) and any(d in href for d in ["linkedin", "internshala", "naukri", "indeed", "glassdoor", "wellfound"]):
                        parent = el.locator("xpath=../..")
                        snippet = await parent.inner_text() if await parent.count() > 0 else ""
                        collected_jobs.append({
                            "category": category,
                            "raw_title": title.split("\n")[0],
                            "url": href,
                            "snippet": snippet.replace("\n", " ")[:300],
                            "source": "Google Search / Job Board",
                        })

            except Exception as e:
                print(f"Error scraping {category}: {e}")

        await browser.close()

    with open("scraped_job_opportunities.json", "w", encoding="utf-8") as f:
        json.dump(collected_jobs, f, indent=2)
    print(f"Total structured opportunities collected: {len(collected_jobs)}")

if __name__ == "__main__":
    asyncio.run(collect_real_jobs())
