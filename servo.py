import RPi.GPIO as GPIO
import time

class ServoMotor:
    def __init__(self, pwm_pin, min_angle=50, max_angle=140):
        self.pwm_pin = pwm_pin
        self.min_angle = min_angle
        self.max_angle = max_angle
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.pwm_pin, 50)  # 서보모터는 일반적으로 50Hz의 PWM 신호를 사용합니다.
        self.pwm.start(0)
        self.set_angle(95)  # 초기 각도를 중립값인 95도로 설정합니다.
    
    def angle_to_duty_cycle(self, angle):
        # 각도를 듀티 사이클 값으로 변환합니다. 이 계산은 서보 모터에 따라 다를 수 있습니다.
        duty_cycle = (angle / 180.0) * 10.0 + 2.5
        return duty_cycle
        
    def set_angle(self, angle):
        if self.min_angle <= angle <= self.max_angle:
            duty_cycle = self.angle_to_duty_cycle(angle)
            self.pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.5)  # 서보 모터가 목표 각도로 이동하는 데 시간을 부여합니다.
            self.pwm.ChangeDutyCycle(0)  # 서보의 진동을 방지하기 위해 신호를 끕니다.
        else:
            raise ValueError(f"Angle must be between {self.min_angle} and {self.max_angle}")
            
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

# 사용 예시
if __name__ == "__main__":
    servo_pin = 19  # PWM 신호를 출력할 GPIO 핀 번호를 지정합니다.
    servo = ServoMotor(pwm_pin=servo_pin)
    
    try:
        # 사용자가 지정한 각도로 서보모터를 회전시킵니다.
        servo.set_angle(50)  # 좌회전
        servo.set_angle(95)  # 중립
        servo.set_angle(140) # 우회전
    finally:
        servo.cleanup()



