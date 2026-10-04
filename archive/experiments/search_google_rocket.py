import asyncio
import base64
import json
import re
from playwright.async_api import async_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def search_and_download_rocket():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-first-run", "--no-default-browser-check"],
        )
        page = await browser.new_page()
        # Search Google Images
        url = "https://www.google.com/search?q=rocket+drawing+clipart+transparent&tbm=isch"
        print(f"Searching Google Images for rocket drawings...")
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # Find image elements
        images = page.locator("img")
        count = await images.count()
        print(f"Found {count} image elements on Google Images.")

        saved = False
        for i in range(1, min(count, 20)):
            img = images.nth(i)
            src = await img.get_attribute("src") or ""
            if src.startswith("data:image/jpeg;base64,") or src.startswith("data:image/png;base64,"):
                header, encoded = src.split(",", 1)
                data = base64.b64decode(encoded)
                if len(data) > 3000: # Decent resolution thumbnail
                    with open("google_rocket_ref.png", "wb") as f:
                        f.write(data)
                    print(f"Saved reference image {i} ({len(data)} bytes) to google_rocket_ref.png")
                    saved = True
                    break
            elif src.startswith("http"):
                # Download
                try:
                    import httpx
                    r = httpx.get(src, timeout=5.0)
                    if r.status_code == 200 and len(r.content) > 3000:
                        with open("google_rocket_ref.png", "wb") as f:
                            f.write(r.content)
                        print(f"Downloaded HTTP image {i} ({len(r.content)} bytes)")
                        saved = True
                        break
                except Exception:
                    continue

        await browser.close()
        return saved

if __name__ == "__main__":
    asyncio.run(search_and_download_rocket())
