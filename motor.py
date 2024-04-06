#pip install RPi.GPIO

# motor_control.py
import RPi.GPIO as GPIO
import time

class MotorController:
    def __init__(self, pwm_pin, frequency=1000):
        self.pwm_pin = pwm_pin
        self.frequency = frequency
        
        # GPIO 초기 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        
        # PWM 인스턴스 생성 및 시작
        self.pwm = GPIO.PWM(self.pwm_pin, self.frequency)
        self.pwm.start(0)
    
    def set_speed(self, speed_percent):
        """모터의 속도를 설정하는 함수입니다.
        speed_percent는 0(정지)에서 100(최대 속도) 사이의 값입니다."""
        if 0 <= speed_percent <= 100:
            duty_cycle = (speed_percent / 100) * 100
            self.pwm.ChangeDutyCycle(duty_cycle)
        else:
            raise ValueError("Speed must be between 0 and 100")
    
    def stop(self):
        """모터를 정지합니다."""
        self.set_speed(0)
    
    def cleanup(self):
        """사용이 끝난 후 GPIO 설정을 초기화합니다."""
        self.pwm.stop()
        GPIO.cleanup()

