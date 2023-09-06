from flask import Flask     #
import RPi.GPIO as GPIO     #


GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정

red_pin = 14                     # 빨간 LED 핀은 라즈베리파이 GPIO 14번핀으로
green_pin = 15                   # 초록 LED 핀은 라즈베리파이 GPIO 15번핀으로
blue_pin = 18                    # 파란 LED 핀은 라즈베리파이 GPIO 18번핀으로
GPIO.setup(red_pin, GPIO.OUT)    # 각각 LED 핀들을 출력으로 설정
GPIO.setup(green_pin, GPIO.OUT)
GPIO.setup(blue_pin, GPIO.OUT)

app = Flask(__name__)       # Flask라는 이름의 객체 생성

@app.route('/')             # 기본 주소
def hello():                # 해당 주소에서 실행되는 함수 정의
   return "LED 제어를 위해 주소창을 변경하세요"
   # 반드시 return이 있어야하며, 해당 값을 화면에 보여줌

@app.route('/red_on')       # IP주소:port/red_on 을 입력하면 나오는 페이지
def red_on():               # 해당 페이지의 뷰함수 정의
   GPIO.output(red_pin, GPIO.HIGH)  # 빨간 LED 핀에 HIGH 신호 인가(LED 켜짐)
   return "red LED on"              # 뷰함수의 리턴값

@app.route('/green_on')     # IP주소:port/green_on 을 입력하면 나오는 페이지
def green_on():             # 해당 페이지의 뷰함수 정의
   GPIO.output(green_pin, GPIO.HIGH) # 초록 LED 핀에 HIGH 신호 인가(LED 켜짐)
   return "green LED on"

@app.route('/blue_on')
def blue_on():
   GPIO.output(blue_pin, GPIO.HIGH)
   return "blue LED on"

@app.route('/off')          # IP주소:port/off 를 입력하면 나오는 페이지
def off():                  # 해당 페이지의 뷰함수 정의
   GPIO.output(red_pin, GPIO.LOW)   # 각각의 LED핀에 LOW 신호를 인가하여 LED 끔
   GPIO.output(green_pin, GPIO.LOW)
   GPIO.output(blue_pin, GPIO.LOW)
   return "all LED off"

@app.route('/clean_up')
def clean_up():
   GPIO.cleanup()
   return "clean up"

if __name__ == "__main__":  # 웹사이트를 호스팅하여 접속자에게 보여주기 위한 부분
   app.run(host="192.168.1.4", port = "8080")
   # host는 현재 라즈베리파이의 내부 IP, port는 임의로 설정
   # 해당 내부 IP와 port를 포트포워딩 해두면 외부에서도 접속가능