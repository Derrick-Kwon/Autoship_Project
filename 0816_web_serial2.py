from flask import Flask, request, jsonify, render_template
import serial
from threading import Thread

app = Flask(__name__)

# 아두이노 시리얼 연결 설정
arduino = serial.Serial('COM5', 9600)
stop_flag = False

def serial_start():
    global stop_flag
    while not stop_flag:
        if arduino.readable():
            res = arduino.readline()
            res_decode = res.decode().strip()
            print(res_decode)

# Start the serial thread
serial_thread = Thread(target=serial_start)
serial_thread.start()

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
    arduino.write(f"{x},{y}\\n".encode())

    return jsonify({"message": "Success"})

if __name__ == '__main__':
    try:
        app.run(host='127.0.0.1', port=5000)
    finally:
        stop_flag = True
        serial_thread.join()