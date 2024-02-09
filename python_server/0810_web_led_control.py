from flask import Flask, render_template
import serial

app = Flask(__name__)

# 아두이노 연결
ser = serial.Serial('COM5', 9600)

@app.route('/')
def index():
    return render_template("0810_web_led.html")

@app.route('/red_on')
def red_on():
    ser.write(b'r')  # 빨간색 LED ON
    return "red LED on"

@app.route('/green_on')
def green_on():
    ser.write(b'g')  # 초록색 LED ON
    return "green LED on"


@app.route('/off')
def off():
    ser.write(b'o')  # 모든 LED OFF
    return "all LED off"

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8080)
    finally:
        ser.close()  # Flask 앱 종료 시 시리얼 연결을 닫습니다.


