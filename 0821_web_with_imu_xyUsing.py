from flask import Flask, request, jsonify, render_template
import serial
from math import atan2

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
    print(f"아두이노로 보내기: x={x}, y={y}")

    # 아두이노에 x, y 전송
    arduino.write(f"h,{x},{y}\\n".encode())
    return jsonify({"message": "Success"})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)