import serial
ser = serial.Serial('COM5', 9600)  # COM 포트와 보레이트를 아두이노 설정에 맞게 변경해야 합니다.
while True:
    data = ser.readline().decode('utf-8').strip()  # 시리얼 포트에서 데이터 읽기
    print(data)  # 읽은 데이터 출력