import RPi.GPIO as GPIO

SERVO_MIN_DUTY = 3
SERVO_MAX_DUTY = 12

servo_pin = 18  # 임의로 서보 모터 핀 입력
desired_angle = 90 # 필요로 하는 서보모터 제어 값 (초기값은 90 설정)
servo_count = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def ServoPos(degree):
    degree = float(degree)  # degree를 float 타입으로 변환
    duty = SERVO_MIN_DUTY+(degree*(SERVO_MAX_DUTY-SERVO_MIN_DUTY)/180.0)
    pwm.ChangeDutyCycle(duty)
    
    
if __name__ == '__main__':
    ServoPos(100)