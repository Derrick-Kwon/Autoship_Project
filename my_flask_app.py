from flask import Flask, render_template
from flask_socketio import SocketIO
import serial

app = Flask(__name__)
app.config['SECRET_KEY'] = '0000'
socketio = SocketIO(app)

ser = None  # 초기값을 None으로 설정

@app.before_request
def init_serial_communication():
    global ser
    if ser is None:  # 만약 아직 시리얼 연결이 초기화되지 않았다면
        ser = serial.Serial('COM5', 9600)

@app.route('/')
def index():
    data = ser.readline().decode('utf-8').strip()

    if data.startswith('$GPRMC'):
        parts = data.split(',')
        if len(parts) >= 7 and parts[2] == 'A':  # A는 유효한 데이터임을 나타냄
            latitude_str = parts[3]
            latitude_dir = parts[4]
            longitude_str = parts[5]
            longitude_dir = parts[6]

            latitude = float(latitude_str[:2]) + float(latitude_str[2:]) / 60
            if latitude_dir == 'S':
                latitude = -latitude

            longitude = float(longitude_str[:3]) + float(longitude_str[3:]) / 60
            if longitude_dir == 'W':
                longitude = -longitude
        else:
            latitude = 37.5665  # default 값
            longitude = 126.9780
    else:
        latitude = 37.5665  # default 값
        longitude = 126.9780

    return render_template('map.html', latitude=latitude, longitude=longitude)

if __name__ == '__main__':
        socketio.run(app, debug=True)


