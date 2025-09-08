import cloudscraper
from bs4 import BeautifulSoup


def extract_saramin_jobs(keyword):
    scraper = cloudscraper.create_scraper()
    url = "https://m.saramin.co.kr/search/get-theme-jobs"
    params = {"searchWord": keyword, "searchType": "search", "layout": "true"}
    response = scraper.get(url, params=params)

    if response.status_code != 200:
        print("Can't request API")
        return []

    try:
        data = response.json()
    except Exception as e:
        print("JSON parse error:", e)
        return []

    html = data.get("innerHTML", "")
    if not html:
        print("No innerHTML found in response")
        return []

    soup = BeautifulSoup(html, "html.parser")

    recruit_containers = soup.select("div.recruit_container")
    print(f"Found {len(recruit_containers)} recruit containers")

    results = []
    for container in recruit_containers:
        print("job: ", container)
        try:
            a_tag = container.find("a", href=True)
            if not a_tag:
                continue

            title_tag = a_tag.find("p", class_="tit")
            company_tag = a_tag.find("span", class_="corp_name")
            deadline_tag = a_tag.find("span", class_="date")
            location_tag = a_tag.select_one("div.meta > span")

            if not title_tag or not company_tag or not location_tag:
                continue

            link = a_tag['href']
            if link.startswith("/"):
                link = "https://m.saramin.co.kr" + link

            job = {
                "position":
                title_tag.get_text(strip=True).replace(",", " "),
                "company":
                company_tag.get_text(strip=True).replace(",", " "),
                "location":
                location_tag.get_text(strip=True).replace(",", " "),
                "dday":
                deadline_tag.get_text(strip=True).replace(",", " ")
                if deadline_tag else "마감일 미제공",
                "link":
                link
            }
            results.append(job)
        except Exception as e:
            print("Error:", e)
            continue

    print(f"Found {len(results)} jobs for '{keyword}'")
    return results
