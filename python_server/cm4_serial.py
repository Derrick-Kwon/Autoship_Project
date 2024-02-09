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
    return render_template('1103_cm4_serial.html')

@app.route('/fetch_serial_data', methods=['GET'])
def fetch_serial_data():
    return jsonify(database)

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)


def print_imu_serial():
    isFirst = True
    count = 50
    while True:
        
        # GPS 데이터 처리
        nx = cgps.next()
        if nx['class'] == 'TPV':
            latitude = getattr(nx, 'lat', None)
            longitude = getattr(nx, 'lon', None)
            speed = getattr(nx, 'speed', None)
            if speed is not None: 
                speed_kmh = 3.6 * speed
                database['speed'] = speed_kmh  # km/h로 변환하여 저장
            if latitude is not None:
                database['latitude'] = latitude
            if longitude is not None:
                database['longitude'] = longitude


        # IMU 데이터 처리
        if serial.in_waiting > 0:
            count += 1
            try:
                line = serial.readline().decode('utf-8').strip()
            except:
                continue
            arr = line.split()
            if '*' in line:
                continue
            # IMU 데이터를 데이터베이스에 저장
            database['yaw'] = arr[0]
            database['pitch'] = arr[1]
            database['roll'] = arr[2]
            database['risk'] = arr[3]
            if count % 3 == 0:
                database['ridar'].append((arr[5], arr[6]))
            if count > 500:
                # 데이터베이스가 업데이트됨
                requests.post('http://192.168.43.235:5000/api/send', json=database)
                count = 0

        time.sleep(0.1)  # CPU 사용률을 낮추기 위한 작은 지연

if __name__ == '__main__':
    
    # GPS -> 위도경도
    #아두이노 -> IMU, 라이더 
    #여기는 쓰레드 부분

    flask_thread= threading.Thread(target=run_flask_app) #플라스크 쓰레드
    flask_thread.start()

    serial_thread = threading.Thread(target=print_imu_serial) #ridar, imu 처리 쓰레드
    serial_thread.start()
    