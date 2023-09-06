from flask import Flask, request, jsonify, render_template
import serial
from collections import deque
from math import sqrt

app = Flask(__name__)

# 아두이노 시리얼 연결 설정
waypoint_queue = deque()
arduino = serial.Serial('COM7', 9600)

@app.route('/')
def index():
    return render_template('0821_web_algorithm.html')

def calculate_distance(current, target):
    return sqrt((current[0] - target[0]) ** 2 + (current[1] - target[1]) ** 2)

@app.route('/set_destination', methods=['POST'])
def set_destination():  #목적지 추가
    data = request.get_json()
    x = data['x']
    y = data['y']
    waypoint_queue.append((x, y))
    return jsonify({"message": "Waypoint added successfully"})

@app.route('/add_waypoint', methods=['POST'])
def add_waypoint(): #경유지 추가
    data = request.get_json()
    x = data['x']
    y = data['y']
    waypoint_queue.append((x, y))
    return jsonify({"message": "Waypoint added successfully"})

@app.route('/navigate', methods=['GET'])
def navigate():
    if not waypoint_queue:
        return jsonify({"message": "No waypoints left"})

    data = request.get_json()
    current_position = (data['currentLat'], data['currentLng'])
    target_position = waypoint_queue[0]

    if calculate_distance(current_position, target_position) <= 2:
        waypoint_queue.popleft()
        if waypoint_queue:
            target_position = waypoint_queue[0]
        else:
            return jsonify({"message": "All waypoints visited"})

    directionX = target_position[0] - current_position[0]
    directionY = target_position[1] - current_position[1]
    arduino.write(f"h,{directionX},{directionY}\\n".encode())
    return jsonify({"message": "Direction sent"})

def send_vector(data):
    directionX = data['directionX']
    directionY = data['directionY']
    currentLat = data['currentLat']
    currentLng = data['currentLng']
    targetLat = data['targetLat']
    targetLng = data['targetLng']
    print(f"아두이노로 보내기: x={directionX}, y={directionY}")
    arduino.write(f"h,{directionX},{directionY},{currentLat},{currentLng},{targetLat},{targetLng}\\n".encode())
    return jsonify({"message": "Success"})

@app.route('/send_to_arduino', methods=['POST'])
def send_to_arduino():
    while waypoint_queue:
        data = waypoint_queue.popleft()
        send_vector(data)
    return jsonify({"message": "Data sent to Arduino successfully"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)