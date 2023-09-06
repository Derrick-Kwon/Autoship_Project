from flask import Flask, request, jsonify, render_template
import serial
from collections import deque
from math import atan2

app = Flask(__name__)
# 아두이노 시리얼 연결 설정
destinations = deque()

arduino = serial.Serial('COM7', 9600)

@app.route('/')
def index():
    return render_template('0906_webservo_rasp.html')

@app.route('/set_destination', methods=['POST'])
def set_destination(): #위도값, 경도값, 각도값 큐에 저장
    latitude = float(request.form['latitude'])
    longitude = float(request.form['longitude'])
    angle = atan2(longitude, latitude) * (180.0 / 3.141592653589793)
    destinations.append((latitude, longitude, angle)) #위도, 경도, 각도 순서.
    return jsonify({"message": "Destination set successfully"})

@app.route('/navigate', methods=['POST'])
def navigate(): #방향벡터 보내기
    data = request.get_json()
    x = data['x']
    y = data['y']
    print(f"아두이노로 보내기: x={x}, y={y}")

    # 아두이노에 x, y 전송
    arduino.write(f"h,{x},{y}\\n".encode())
    return jsonify({"message": "Success"})


@app.route('/navigate', methods=['POST'])
def navigate(): #위도경도 보내기
    if not destinations:
        return jsonify({"message": "No destination set"})

    latitude, longitude, angle = destinations.popleft()
    # Sending the x, y, and angle to Arduino (assuming x is latitude and y is longitude for this context)
    arduino.write(f"h,{latitude},{longitude}\\n".encode())
    return jsonify({"message": "Navigating to set destination"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)