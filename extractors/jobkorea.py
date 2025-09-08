import cloudscraper
from bs4 import BeautifulSoup


def extract_jobkorea_jobs(keyword):
    scraper = cloudscraper.create_scraper()
    base_url = "https://www.jobkorea.co.kr/Search/?stext="
    response = scraper.get(f"{base_url}{keyword}")

    if response.status_code != 200:
        print("Can't request website")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    postings = soup.find_all("div", {"data-sentry-element": "Flex"})

    results = []
    for post in postings:
        try:
            # title: Typography_variant_size18__344nw25 클래스 가진 span
            title_span = post.find("span",
                                   class_="Typography_variant_size18__344nw25")
            if not title_span:
                continue
            title = title_span.get_text(strip=True)

            # link: title_span 기준으로 부모 a 태그가 있다면 링크 추출
            a_tag = title_span.find_parent("a", href=True)
            if not a_tag:
                continue
            link = a_tag['href']
            if link.startswith("/"):
                link = "https://www.jobkorea.co.kr" + link

            # company: Typography_variant_size16__344nw26 클래스 가진 span
            company_span = post.find(
                "span", class_="Typography_variant_size16__344nw26")
            company = company_span.get_text(
                strip=True) if company_span else "정보 없음"

            # deadline: Typography_variant_size13__344nw28 클래스 가진 span
            deadline_span = post.find(
                "span", class_="Typography_variant_size13__344nw28")
            deadline = deadline_span.get_text(
                strip=True) if deadline_span else "마감일 미제공"

            # location: Typography_variant_size14__344nw27 클래스 가진 span 중 4번째
            location_spans = post.find_all("span", class_="Typography_variant_size14__344nw27")
            if len(location_spans) >= 4:
                location = location_spans[3].get_text(strip=True)
            else:
                location = "정보 없음"


            job = {
                "position": title.replace(",", " "),
                "company": company.replace(",", " "),
                "location": location.replace(",", " "),
                "dday": deadline.replace(",", " "),
                "link": link
            }
            results.append(job)
        except Exception as e:
            print("Error:", e)
            continue

    print(f"Found {len(results)} jobs for '{keyword}'")
    return results