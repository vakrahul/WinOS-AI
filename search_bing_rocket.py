import asyncio
import base64
import httpx
from playwright.async_api import async_playwright

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

async def search_bing_rocket():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
            args=["--no-first-run", "--no-default-browser-check"],
        )
        page = await browser.new_page()
        url = "https://www.bing.com/images/search?q=cartoon+rocket+drawing+clipart+isolated"
        print("Searching Bing Images for rocket drawings...")
        await page.goto(url, timeout=30000, wait_until="domcontentloaded")
        await page.wait_for_timeout(3000)

        # In Bing Images, thumbnails are in .mimg or img.mimg
        images = page.locator("img.mimg")
        count = await images.count()
        print(f"Found {count} rocket image thumbnails on Bing Images.")

        saved = False
        for i in range(min(count, 10)):
            img = images.nth(i)
            src = await img.get_attribute("src") or ""
            if not src:
                src = await img.get_attribute("data-src") or ""
            
            if src.startswith("data:image/"):
                header, encoded = src.split(",", 1)
                data = base64.b64decode(encoded)
                with open("reference_rocket.png", "wb") as f:
                    f.write(data)
                print(f"Saved base64 rocket reference ({len(data)} bytes).")
                saved = True
                break
            elif src.startswith("http"):
                try:
                    res = httpx.get(src, timeout=10.0)
                    if res.status_code == 200 and len(res.content) > 2000:
                        with open("reference_rocket.png", "wb") as f:
                            f.write(res.content)
                        print(f"Downloaded HTTP rocket reference ({len(res.content)} bytes).")
                        saved = True
                        break
                except Exception as e:
                    continue

        await browser.close()
        return saved

if __name__ == "__main__":
    asyncio.run(search_bing_rocket())
