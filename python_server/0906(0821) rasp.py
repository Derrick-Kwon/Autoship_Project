from flask import Flask, request, jsonify, render_template
import serial
from collections import deque
from math import atan2

app = Flask(__name__)
# 아두이노 시리얼 연결 설정
destinations = deque()
arduino = serial.Serial('COM7', 9600) #여기 포트 num은 라즈베리파이서 아두이노 실행시켜서 찾으면 됨(notion 참고)

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
    arduino.write(f"h,{deltaX},{deltaY}\n".encode())  # h는 헤더, {destLat},{destLng},{angle} 는 추후 처리
    return jsonify({"message": "Navigating to set destination"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)


