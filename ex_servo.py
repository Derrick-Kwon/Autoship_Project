# 다른 Python 스크립트에서 서보 모터 제어 모듈 사용하기
from servo import ServoMotor
import time

servo_pin = 19  # PWM 신호를 출력할 GPIO 핀 번호를 지정합니다.
servo = ServoMotor(pwm_pin=servo_pin)

try:
    servo.set_angle(50)  # 좌회전
    time.sleep(1)
    servo.set_angle(95)  # 중립 상태
    time.sleep(1)
    servo.set_angle(140)  # 우회전
finally:
    servo.cleanup()
