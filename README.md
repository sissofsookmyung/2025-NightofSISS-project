
## 📌 프로젝트 개요
Trip.com의 항공권 및 숙박 데이터를 크롤링해, 사용자가 원하는 조건을 입력하면 해당 정보를 빠르게 확인할 수 있는 웹사이트 제작


## ✈️  주요 기능
- 사용자가 입력한 출발일, 도착일, 인원수를 기반으로 최저가 항공권 정보 제공
- 여행 일정에 맞춰 평점이 가장 높은 숙박 장소 및 고객 리뷰 제공

## 🚀실행 방법
※ Selenium 사용을 위해 [ChromeDriver](https://sites.google.com/chromium.org/driver/)가 설치되어 있어야 하며,
   버전은 사용하는 Chrome 브라우저와 일치해야 함
   
1. 프로젝트 클론  
git clone https://github.com/La-hee/SISS-project.git
cd SISS-project/team8

3. 필요한 패키지 설치  
pip install -r requirements.txt

5. 웹 애플리케이션 실행  
python fianl.py

 ## 🛠️ 기술 스택

| 분야         | 사용 기술                          |
|--------------|-------------------------------------|
| **Language** | Python 3.12 |
| **Frontend** | HTML, CSS                           |
| **Web Framework**  | Flask                       |
| **Crawling** | Selenium, Requests             |
| **브라우저 자동화** | Selenium WebDriver, ChromeDriver|


## 👥 팀 정보
김라희 : 항공 정보 크롤링 기능 개발 및 HTML 템플릿 구성, 전체 코드 통합 및 테스트

정다인 : 숙박 정보 크롤링 기능 개발



