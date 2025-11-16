from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import urllib.parse
import re

def search(dcity, acity, dep_date, arr_date, people):

    # 봇으로 인식되지 않도록, 브라우저 설정
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")


    driver = webdriver.Chrome(options=options)

    base_url = "https://kr.trip.com/flights/showfarefirst?"

    # 검색 파라미터 구성
    params = {
        "dcity": dcity,
        "acity": acity,
        "ddate": dep_date,
        "rdate": arr_date,
        "quantity": people,
        "triptype": "rt",
        "class": 'y'
    }

    # URL 생성
    query_string = urllib.parse.urlencode(params)
    final_search_url = f"{base_url}{query_string}"

    # 페이지 이동
    driver.get(final_search_url)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # 항공편 카드 XPath
    flight_list_xpath = '//*[starts-with(@data-testid, "u-flight-card-")]'
    wait = WebDriverWait(driver, 30)
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, flight_list_xpath)))

    #결과 딕셔너리를 저장할 리스트
    results = []

    for flight in elements[:5]:
        try:
            # 항공편 정보 텍스트 추출
            info_element = flight.find_element(By.CSS_SELECTOR, 'div.flight-info.is-v2')
            text = info_element.get_attribute('aria-label') or ""

            # 출발/도착 시간 추출
            deptime_match = re.search(r'\d{4}-\d{2}-\d{2} (\d{2}:\d{2}):\d{2}에 출발하여', text)
            arrtime_match = re.search(r'\d{4}-\d{2}-\d{2} (\d{2}:\d{2}):\d{2}에 도착하는', text)

            deptime = deptime_match.group(1) if deptime_match else "출발 정보 없음"
            arrtime = arrtime_match.group(1) if arrtime_match else "도착 정보 없음"

            # 항공사 이름 추출
            try:
                airline_element = flight.find_element(By.CSS_SELECTOR, '[data-testid="flights-name"]')
                airline = airline_element.text.strip()
            except:
                airline = "항공사 정보 없음"

            # 가격 추출
            price_match = re.search(r'왕복 요금:\s*([\d,]+)원', text)
            price = price_match.group(1) if price_match else "가격 정보 없음"

            # 결과 저장
            results.append({
                "airline": airline,
                "departure": deptime,
                "arrival": arrtime,
                "price": price
            })

        except Exception as e:
            print(f"오류 발생: {e}")
            continue
    
    driver.quit()
    return results
    
