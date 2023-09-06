from flask import Flask, render_template, jsonify
import serial
import threading

app = Flask(__name__)

ser = serial.Serial('COM5', 9600)  # COM 포트와 보레이트를 아두이노 설정에 맞게 변경

current_data = ""

def read_from_serial():
    global current_data
    while True:
        if ser.in_waiting > 0:
            current_data = ser.readline().decode('utf-8').rstrip()

threading.Thread(target=read_from_serial).start()

@app.route('/')
def index():
    return render_template("0810_PySerial.html")

@app.route('/data')
def get_data():
    return jsonify(data=current_data)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)