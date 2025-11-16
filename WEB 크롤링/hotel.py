from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 상위 5개 호텔과 리뷰 수집
def get_hotels_with_reviews(cityID, destination, checkin, checkout, adults):
    base_url = (
        "https://kr.trip.com/hotels/list"
        "?city={}&cityName={}&provinceId=0&countryId=4&districtId=0"
        "&checkin={}&checkout={}&lowPrice=0&highPrice=-1"
        "&barCurr=KRW&searchType=CT&searchWord={}&crn=1&adult={}&children=0"
        "&searchBoxArg=t&travelPurpose=0&locale=ko-KR&curr=KRW"
    )
    url = base_url.format(cityID, destination, checkin, checkout, destination, adults)

    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 ... Chrome/117.0.0.0 Safari/537.36")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.list-card-title a.name"))
        )
    except:
        print("숙소 목록 로딩 실패")
        driver.quit()
        return []

    hotel_links = driver.find_elements(By.CSS_SELECTOR, "div.list-card-title a.name")
    hotels_data = []
    for elem in hotel_links:
        name = elem.text.strip()
        link = elem.get_attribute("href")
        if name and link:
            hotels_data.append((name, link))

    top_hotels = []
    for i, (name, link) in enumerate(hotels_data[:5]):
        try:
            driver.execute_script("window.open(arguments[0]);", link)
            driver.switch_to.window(driver.window_handles[1])

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h2.onlineTab_tabNavgation_item__NtJx2"))
            )

            review_tabs = driver.find_elements(By.CSS_SELECTOR, "h2.onlineTab_tabNavgation_item__NtJx2")
            clicked = False
            for tab in review_tabs:
                if "투숙객 리뷰" in tab.text:
                    driver.execute_script("arguments[0].click();", tab)
                    clicked = True
                    break

            if not clicked:
                raise Exception("투숙객 리뷰 탭을 찾지 못했음")

            time.sleep(3)  # 리뷰 로딩 대기

            review_elements = driver.find_elements(By.CSS_SELECTOR, "div[class^='UXjSnokalMIS5CzMtLSM']")
            reviews = [r.text.strip() for r in review_elements if r.text.strip()]
            if not reviews:
                reviews = ["(리뷰 없음)"]

            top_hotels.append({
                "name": name,
                "reviews": reviews,
                "link": link
            })

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        except Exception as e:
            print(f"{i+1}번째 숙소 처리 중 오류 발생: {e}")
            top_hotels.append({
                "name": name,
                "reviews": ["(리뷰 없음)"],
                "link": link
            })
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue
    print(hotels_data)
    driver.quit()
    return top_hotels

# 선택한 호텔 주소 가져오기
def get_hotel_address(hotel_link):
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 ... Chrome/117.0.0.0 Safari/537.36")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get(hotel_link)

        address_elem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[class^="hotelDescription_hotelDescription-address_detail"]'))
        )

        address_text = address_elem.text.strip()
        return address_text

    except Exception as e:
        print("주소 가져오기 실패:", e)
        return "(주소 없음)"

    finally:
        driver.quit()


# ------------------ 실행 ------------------
# destination = "오사카"
# checkin = "2025/08/20"
# checkout = "2025/08/23"
# adults = 1


cityID_search = {
    "오사카": 219,
    "후쿠오카": 248,
    "방콕": 359,
    "상하이": 2,
    "서울": 274,
    "도코": 228,
    "부산": 253,
    "다낭": 1356,
    "나트랑": 1777,
    "제주": 737
}

