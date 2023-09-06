from flask import Flask, request, jsonify, render_template
import serial
from math import atan2
import math

float PI = math.pi

app = Flask(__name__)

# 아두이노 시리얼 연결 설정
arduino = serial.Serial('COM7', 9600)

@app.route('/')
def index():
    return render_template('0813_web_servo.html')

@app.route('/send_vector', methods=['POST'])
def send_vector():
    data = request.get_json()
    x = data['x']
    y = data['y']
    float ang =0
    ang = atan2(y, x)*(180.0 /PI)
    print(f"아두이노로 보내기: angle={ang}, y={y}")

    # 아두이노에 angle
    arduino.write(f"h,{x},{y}\\n".encode())
    return jsonify({"message": "Success"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)