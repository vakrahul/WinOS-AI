import asyncio
import json
from bs4 import BeautifulSoup
import httpx

URLS = [
    ("AI / Machine Learning", "https://internshala.com/internships/artificial-intelligence-ai,machine-learning-internship-in-hyderabad/"),
    ("Python Backend", "https://internshala.com/internships/python-django-internship-in-hyderabad/"),
    ("Remote AI / ML", "https://internshala.com/internships/work-from-home-artificial-intelligence-ai,machine-learning-internships/"),
]

async def scrape_internshala():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }
    jobs = []
    async with httpx.AsyncClient(headers=headers, timeout=20.0, follow_redirects=True) as client:
        for cat, url in URLS:
            print(f"Fetching: {url}...")
            res = await client.get(url)
            print(f"Status: {res.status_code}, Length: {len(res.text)}")
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                cards = soup.find_all("div", class_="individual_internship")
                print(f"Found {len(cards)} internship cards for {cat}")
                for card in cards:
                    title_elem = card.find("h3", class_="job-internship-name") or card.find("a", class_="view_detail_button")
                    company_elem = card.find("p", class_="company-name") or card.find("a", class_="link_display_like_text")
                    location_elem = card.find("div", class_="row-1-item locations") or card.find("span", class_="location_link")
                    duration_elem = card.find("div", class_="row-1-item duration") or card.find("span", class_="duration")
                    stipend_elem = card.find("span", class_="stipend")

                    link = ""
                    if title_elem and title_elem.name == "a":
                        link = "https://internshala.com" + title_elem.get("href", "")
                    elif card.get("data-href"):
                        link = "https://internshala.com" + card.get("data-href", "")

                    title = title_elem.get_text(strip=True) if title_elem else "Intern"
                    company = company_elem.get_text(strip=True) if company_elem else "Unknown Company"
                    loc = location_elem.get_text(strip=True) if location_elem else "Hyderabad"
                    dur = duration_elem.get_text(strip=True) if duration_elem else "N/A"
                    stipend = stipend_elem.get_text(strip=True) if stipend_elem else "Unspecified"

                    jobs.append({
                        "category": cat,
                        "job_title": title,
                        "company_name": company,
                        "location": loc,
                        "duration": dur,
                        "stipend": stipend,
                        "application_link": link,
                        "source": "Internshala",
                    })

    with open("actual_internships.json", "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)
    print(f"Total collected internships: {len(jobs)}")

if __name__ == "__main__":
    asyncio.run(scrape_internshala())
