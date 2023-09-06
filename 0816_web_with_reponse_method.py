from flask import Flask, request, jsonify, render_template, Response, stream_with_context
import serial

app = Flask(__name__)

# 아두이노 시리얼 연결 설정
arduino = serial.Serial('COM5', 9600)

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
    return jsonify({"message": "Success"}) #성공시

@app.route('/serial_data') # 라우트를 추가, 아두이노 시리얼 데이터를 스트림 형식 -> 반환
def serial_data():
    def generate(): #데이터 읽어 클라이언트에 반환
        while True:
            if arduino.readable():
                res = arduino.readline()
                res_decode = res.decode().strip()
                yield res_decode + "\\n"
    return Response(stream_with_context(generate()), content_type='text/plain')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)