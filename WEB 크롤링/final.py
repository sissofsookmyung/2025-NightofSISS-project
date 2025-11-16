from flask import Flask, render_template
from flask import request
from flight import search
from hotel import get_hotels_with_reviews, get_hotel_address


app = Flask(__name__)


#메인 페이지
@app.route('/', methods = ['GET', 'POST'])
def mainpage() :
    return render_template('main.html')

#항공권 검색 전 정보 입력받기
@app.route('/search/flight', methods = ['GET', 'POST'])
def searchFlight() :
    return render_template('flightSearch.html')

#항공권 검색 및 검색 결과
@app.route('/result/flight', methods = ['GET', 'POST'])
def go() :
    if request.method == 'POST' :
        dcity = request.form.get('dcity')
        acity = request.form.get('acity')
        checkin = request.form.get('checkin', ' ')
        checkout = request.form.get('checkout', ' ')
        people = request.form.get('people', 1)

        #항공권 검색
        flightResult = search(dcity, acity, checkin, checkout, people)

        #결과 페이지로 결과 전송
        return render_template('flightResult.html', flights = flightResult)
    
@app.route('/search/hotel', methods=['GET', 'POST'])
def searchHotel() :
    return render_template('hotelSearch.html')

@app.route('/result/hotel', methods=['GET', 'POST'])
def hotel():
    destination = request.form.get('dcity')
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')
    adults = int(request.form.get('people', 1))

    cityID = request.form.get('acity')
    if not cityID:
        return f"잘못된 도시 입력: {destination}"

    hotels = get_hotels_with_reviews(cityID, destination, checkin, checkout, adults)
    return render_template('hotelResult.html', hotels=hotels)


app.run(debug = True)

