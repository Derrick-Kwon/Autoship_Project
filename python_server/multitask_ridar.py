from flask import Flask, request, jsonify, render_template
import serial
import time
import RPi.GPIO as GPIO
from collections import deque
from math import atan2
import threading
import gpsd

app = Flask(__name__)
# 아두이노 시리얼 연결 설정
destinations = deque() #큐 설정 
arduino = serial.Serial('/dev/ttyACM0', 9600)  # 여기 포트 num은 라즈베리파이서 아두이노 실행시켜서 찾으면 됨(notion 참고)

#deltaX, deltaY가 전역으로 못쓸경우
x_delta = 0.
y_delta = 0.

@app.route('/') #app run 하면 실행하는 page와 html
def index():
    return render_template('0906_webservo_rasp.html')

@app.route('/set_destination', methods=['POST'])
def set_destination():  # 위도값, 경도값, 각도값 큐에 저장
    deltaX = float(request.json['deltaX']) #상대 위도
    deltaY = float(request.json['deltaY']) #상대 경도
    latitude = float(request.json['destLat']) #목적지 위도
    longitude = float(request.json['destLng'])  # 목적지 경도
    angle = atan2(deltaY, deltaX) * (180.0 / 3.141592653589793) #각도 angle
    destinations.append((deltaX, deltaY, latitude, longitude, angle))  # 방향벡터, 위도, 경도, 각도 순서.
    print("목적지를 추가하였습니다")

    return jsonify({"message": "Destination set successfully"})


@app.route('/navigate', methods=['GET', 'POST'])  # 목적지 아두이노로 전송 코드
def navigate():
    deltaX, deltaY, destLat, destLng, angle = destinations.popleft()
    print("아두이노로 전송", deltaX, deltaY, destLat, destLng, angle)
    arduino.write(f"h,{deltaX},{deltaY}\n".encode())  # h는 헤더, {destLat},{destLng},{angle} 는 추후 처리
    return jsonify({"message": "Navigating to set destination"})

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

def read_gps_data():
    # gpsd에 연결
    gpsd.connect()
    try:
        while True:
            packet = gpsd.get_current()
            print("Latitude:", packet.lat)
            print("Longitude:", packet.lon)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program end.")

def print_msg():
    for i in range(100):
        print("연결완료, 여기 함수안쪽부분 바꾸면 됨")
        time.sleep(1)

if __name__ == '__main__':
    serial = serial.Serial('/dev/ttyUSB0', 115200, timeout=None)
    serial.flush()

    #여기는 쓰레드 부분 
    flask_thread = threading.Thread(target=run_flask_app) #앱은 다른 쓰레드에서 실행했음
    flask_thread.start()
    #read_gps_data()

    deltaX, deltaY = load_delta()
    while True:
        if serial.in_waiting>0:
            line = serial.readline().decode('utf=8').rstrip() #공백기준으로 나누고
            arr = line.split() 
            length = len(arr[0])
            if length > 4 : 
                continue # 센서 들어오기전 예외처리
            
            model_yaw = int(arr[1]) #imu 의 yaw
            lidar_angle = int(arr[2]) #라이다가 몇도 틀어져 있는지
            obs_distance = int(arr[3]) #장애물까지의 거리
            obs_measure = int(arr[4]) #obs measure
            target_yaw = int(arr[5]) #내가 얼마나 틀어야 하는지
            if target_yaw != 0:    
                arduino.write(f"h,{deltaX},{deltaY},{target_yaw}\n".encode())