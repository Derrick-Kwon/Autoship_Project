from flask import Flask, request, jsonify, render_template
import serial
from collections import deque
from math import atan2
import threading
import time
#import gpsd
import connect
import requests
import datetime, random, math
#수정 테스트
import forecast

app = Flask(__name__)
# 아두이노 시리얼 연결 설정

destinations = deque()
#arduino = serial.Serial('/dev/ttyACM0', 9600)  # 여기 포트 num은 라즈베리파이서 아두이노 실행시켜서 찾으면 됨(notion 참고)

@app.route('/')
def index():
    return render_template('0906_webservo_rasp.html')

@app.route('/set_destination', methods=['POST'])
def set_destination():  # 위도값, 경도값, 각도값 큐에 저장
    deltaX = float(request.json['deltaX'])
    deltaY = float(request.json['deltaY'])
    latitude = float(request.json['destLat'])
    longitude = float(request.json['destLng'])  # Fix here
    angle = atan2(deltaY, deltaX) * (180.0 / 3.141592653589793)
    destinations.append((deltaX, deltaY, latitude, longitude, angle))  # 방향벡터, 위도, 경도, 각도 순서.
    print("목적지를 추가하였습니다")
    return jsonify({"message": "Destination set successfully"})


@app.route('/navigate', methods=['GET', 'POST'])  # Allow both GET and POST
def navigate():
    deltaX, deltaY, destLat, destLng, angle = destinations.popleft()
    print("아두이노로 전송", deltaX, deltaY, destLat, destLng, angle)
    #arduino.write(f"h,{deltaX},{deltaY}\n".encode())  # h는 헤더, {destLat},{destLng},{angle} 는 추후 처리
    return jsonify({"message": "Navigating to set destination"})

@app.route('/api/send')
def send():
    parameter = getparameter()
    sql message = "insert data values(?, ?, ?, )"
    conn.execute(message, parameter)

# raspberry
def sendData(speed, distance):
    requests.post('url', {speed, distance})

# API for fetch data
@app.route('/api/fetch')
def fetch():
    connect.gen_random_data()
    result = connect.get_data()
    return result

@app.route('/api/weather')
def weather():
    # default location
    lng = 127.3604
    lat = 36.3721

    # if parameter for location is provided, use it.
    parameter_dic = request.args.to_dict()
    if len(parameter_dic) > 0 and parameter_dic["lng"] and parameter_dic["lat"]:
        lng = parameter_dic["lng"]
        lat = parameter_dic["lat"]
    result = connect.get_weather(lat, lng)
    print("weather result: ", result)
    return jsonify(result)

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

@app.route('/get_position')
def get_position():
    nx = cgps.next()
    if nx['class'] == 'TPV':
        latitude = getattr(nx, 'lat', None)
        longitude = getattr(nx, 'lon', None)
        return jsonify(latitude=latitude, longitude=longitude)
    else:
        return jsonify(error="No GPS data available")

def print_msg():
    for i in range(100):
        print("연결완료, 여기 함수안쪽부분 바꾸면 됨")
        time.sleep(1)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask_app) #앱은 다른 쓰레드에서 실행했음
    flask_thread.start()
    #read_gps_data()
    #print_msg() #여기 이부분이 추가 함수부분. 이 밑으로 수정하던가 함수 위에 추가로 만들면 됨.