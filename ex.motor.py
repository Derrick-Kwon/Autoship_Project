# 다른 Python 파일에서 import 사용 예시
from motor import MotorController
import time

# 모터 컨트롤러 인스턴스 생성
motor = MotorController(pwm_pin=18)

try:
    # 모터 속도 설정
    motor.set_speed(50)  # 모터를 50% 속도로 설정, 90/255 = 35.29....%
    time.sleep(2)
    
    motor.stop()  # 모터 정지
    time.sleep(1)
finally:
    motor.cleanup()  # GPIO 핀 상태 정리
