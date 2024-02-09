from flask import Flask, request, jsonify, render_template
import serial
import time
import RPi.GPIO as GPIO
from collections import deque
from math import atan2
import threading
from gps import *
import requests
import datetime, random, math


cgps = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) #cgps 정의
app = Flask(__name__)

# 아두이노 시리얼 연결 설정

destinations = deque() #큐 설정 
database = {
'latitude' : None,  #위도
'longitude' : None, #경도
'speed': None, #속도 km/h
'yaw': None, # 쓸필요없음
'pitch': None, #x축기울기
'roll': None, #y축기울기
'risk' : None, #위험도 1~3
'ridar' : [] } #장애물까지의 각도, 거리(cm)

#시리얼데이터 저장소

# arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1) #송신 라파->아두이노(서보모터조향각도)
serial = serial.Serial('/dev/ttyUSB1', 115200, timeout=1) #수신 아두이노 -> 라파(라이더, IMU)
serial.flush()

#deltaX, deltaY가 전역으로 못쓸경우
x_delta = 0.
y_delta = 0.

@app.route('/') #app run 하면 실행하는 page와 html
def index():
    return render_template('0906_webservo_rasp.html')

@app.route('/fetch_serial_data', methods=['GET'])
def fetch_serial_data():
    return jsonify(database)

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
    # arduino.write(f"h,{deltaX},{deltaY}\n".encode())  # h는 헤더, {destLat},{destLng},{angle} 는 추후 처리
    return jsonify({"message": "Navigating to set destination"})

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)


@app.route('/get_position')
def get_position():
    with app.app_context():
        nx = cgps.next()
        
        if nx['class'] == 'TPV':
            latitude = getattr(nx, 'lat', None)
            # print("위도: ", latitude) 
            longitude = getattr(nx, 'lon', None)
            # print("경도: ", longitude)
            speed = getattr(nx, 'speed', None)  # Get the speed  
            
            if speed !=None: 
                speed_kmh = 3.6*speed
            else:
                speed_kmh = speed

            if latitude!=None:
                database['latitude'] = latitude
            if longitude!=None:
                database['longitude'] = longitude
            if speed!=None:
                database['speed'] = speed
            
            return jsonify(latitude=latitude, longitude=longitude)
        else:
            return jsonify(error="No GPS data available")

def print_msg():
    for i in range(100):
        print("연결완료, 여기 함수안쪽부분 바꾸면 됨")
        time.sleep(1)

# def read_serial_data(): #라이더 데이타 받는부분
#     print(f'TEST')
#     if serial.in_waiting>0:
#             line = serial.readline().decode('utf-8').strip() #공백기준으로 나누고

#             print(f'Received data from Arduino (ridar_data): {line}')

def print_imu_serial():
    isFirst = True
    count = 50
    while True:
        if serial.in_waiting > 0:
            count += 1
            try:
                line = serial.readline().decode('utf-8').strip()
            except:
                continue
            arr = line.split()
            print("arr: ", arr)
            if '*' in line:
                continue
            
            database['yaw'] = arr[0]
            database['pitch'] = arr[1]
            database['roll'] = arr[2]
            database['risk'] = arr[3]
            
            if count%3==0:
                database['ridar'].append((arr[5], arr[6]))
                
            if count > 500:
                get_position()
                requests.post('http://192.168.43.235:5000/api/send', json=database)
                count = 0

            # print(f'Received data from Arduino(imu): {line}')

if __name__ == '__main__':
    # GPS -> 위도경도
    #아두이노 -> IMU, 라이더 
    #여기는 쓰레드 부분

    flask_thread= threading.Thread(target=run_flask_app) #플라스크 쓰레드
    flask_thread.start()

    # serial_thread = threading.Thread(target=read_serial_data) #시리얼 처리 쓰레드
    # serial_thread.start()

    serial_thread = threading.Thread(target=print_imu_serial) #ridar, imu 처리 쓰레드
    serial_thread.start()
    
    # deltaX, deltaY = load_delta()
    # while True:
    #          # 센서 들어오기전 예외처리
    #         model_yaw = int(arr[1]) #imu 의 yaw
    #         lidar_angle = int(arr[2]) #라이다가 몇도 틀어져 있는지
    #         obs_distance = int(arr[3]) #장애물까지의 거리
    #         obs_measure = int(arr[4]) #obs measure
    #         target_yaw = int(arr[5]) #내가 얼마나 틀어야 하는지
    #         if target_yaw != 0:    
    #             arduino.write(f"h,{deltaX},{deltaY},{target_yaw}\n".encode())