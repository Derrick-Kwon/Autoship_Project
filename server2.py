from flask import Flask, render_template
from flask_socketio import SocketIO
import serial

app = Flask(__name__)
socketio = SocketIO(app)
ser = serial.Serial('COM5', 9600)

@app.route('/')
def index():
    return render_template('map.html')


@socketio.on('request_data')
def send_serial_data():
    data = ser.readline().decode('utf-8').strip()
    latitude = 37.5665  # 기본값
    longitude = 126.9780  # 기본값

    if data.startswith('$GPRMC'):
        parts = data.split(',')
        if len(parts) >= 7 and parts[2] == 'A':  # A는 유효한 데이터임을 나타냅니다.
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

    socketio.emit('update_data', {'latitude': latitude, 'longitude': longitude})


if __name__ == '__main__':
    socketio.run(app, debug=True)