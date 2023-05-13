import time

import threading
import RPi.GPIO as GPIO
import RPi.GPIO as GPIO2
import RPi.GPIO as GPIO3
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import socket

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', address=0x3f, port=1, backlight_enabled=True)

GPIO.setwarnings(False)
button_pin = 32

# 設置蜂鳴器引腳和模式
buzzer_pin = 12  # 根據BOARD模式，將BCM 18對應的引腳更改為12
GPIO.setmode(GPIO.BOARD)  # GPIO.BOARD, 使用BOARD模式
GPIO.setup(buzzer_pin, GPIO.OUT)
#Setup Button
GPIO.setup(button_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# LCD clear
lcd.clear()

def rfid_play():
    try:
        while True:
            print("請將卡靠近讀卡器...")
            GPIO.output(buzzer_pin, GPIO.LOW)
            id, text = reader.read()
            GPIO.output(buzzer_pin, GPIO.HIGH)
            print("ID: %s\nText: %s" % (id, text))
            # 顯示在 LCD 螢幕上
            lcd.cursor_pos = (0, 0)
            lcd.write_string(text)
            time.sleep(0.2)
            GPIO.output(buzzer_pin, GPIO.LOW)
            time.sleep(0.2)  # 在讀取到卡片後等待一段時間
    finally:
        GPIO.cleanup()


def button_play():
    lcd = CharLCD('PCF8574', address=0x3f, port=1, backlight_enabled=True)
    lcd.clear()
    # 顯示 IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    lcd.cursor_pos = (1, 0)
    lcd.write_string(ip)

    while True:
        time.sleep(0.5)
        # 按下 button 將 LCD 螢幕清空
        button_state = GPIO.input(button_pin)
        print(button_state)
        if button_state == 0:
            lcd.cursor_pos = (0, 0)
            lcd.write_string(ip)

# 選擇控制伺服馬達的GPIO引腳
servo_pin = 16
# 使用BOARD模式
GPIO2.setmode(GPIO.BOARD)
GPIO2.setup(servo_pin, GPIO.OUT)
# 設置PWM頻率為50Hz
pwm = GPIO2.PWM(servo_pin, 50)
pwm.start(0)

def set_angle(angle):
    duty_cycle = angle / 18 + 2
    GPIO2.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO2.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

# 選擇控制伺服馬達的GPIO引腳
servo_pin_2 = 18
# 使用BOARD模式
GPIO3.setmode(GPIO.BOARD)
GPIO3.setup(servo_pin_2, GPIO.OUT)
# 設置PWM頻率為50Hz
pwm_2 = GPIO3.PWM(servo_pin_2, 50)
pwm_2.start(0)

def set_angle_2(angle):
    duty_cycle = angle / 36 + 2
    GPIO3.output(servo_pin_2, True)
    pwm_2.ChangeDutyCycle(angle)
    time.sleep(1)
    GPIO3.output(servo_pin_2, False)
    pwm_2.ChangeDutyCycle(0)


def excute_angle():
    try:
        # 旋轉伺服馬達
        set_angle(0)  # 第一次先關門
        while True:
            set_angle(90)  # 開門
            set_angle_2(90)  # 開門
            time.sleep(2)
            set_angle(0)  # 關門
            set_angle_2(0)  # 關門
            time.sleep(2)

    finally:
        pwm.stop()
        pwm_2.stop()
        GPIO.cleanup()




if __name__ == '__main__':
    t1 = threading.Thread(target=rfid_play)
    t1.start()
    t2 = threading.Thread(target=button_play)
    t2.start()
    t3 = threading.Thread(target=excute_angle)
    t3.start()
