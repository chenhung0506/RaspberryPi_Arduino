import time

import threading
import RPi.GPIO as GPIO
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

GPIO.setup(31, GPIO.OUT)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.setup(37, GPIO.OUT)


# Traffic Light (紅綠燈) PIN -------------------------------------------------------------
red_pin = 36  # 紅燈
GPIO.setup(red_pin, GPIO.OUT)
yellow_pin = 38  # 黃燈
GPIO.setup(yellow_pin, GPIO.OUT)
green_pin = 40  # 綠燈
GPIO.setup(green_pin, GPIO.OUT)

# 選擇控制伺服馬達的GPIO引腳
servo_pin = 16
# 使用BOARD模式
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin, GPIO.OUT)
# 設置PWM頻率為50Hz
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)
# 選擇控制伺服馬達的GPIO引腳
servo_pin_2 = 18
# 使用BOARD模式
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo_pin_2, GPIO.OUT)
# 設置PWM頻率為50Hz
pwm_2 = GPIO.PWM(servo_pin_2, 50)
pwm_2.start(0)

def traffic_light_play():
    while True:
        # 綠燈亮 10 秒
        GPIO.output(green_pin, GPIO.HIGH)
        GPIO.output(yellow_pin, GPIO.LOW)
        GPIO.output(red_pin, GPIO.LOW)
        time.sleep(10)
        # 黃燈亮 2 秒
        GPIO.output(green_pin, GPIO.LOW)
        GPIO.output(yellow_pin, GPIO.HIGH)
        GPIO.output(red_pin, GPIO.LOW)
        time.sleep(2)
        # 紅燈亮 10 秒
        GPIO.output(green_pin, GPIO.LOW)
        GPIO.output(yellow_pin, GPIO.LOW)
        GPIO.output(red_pin, GPIO.HIGH)
        time.sleep(10)


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
            
            # 啟動 Servo & 更新 Servo 在 LCD 上的狀態
            servo_play_and_lcd_update()
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

def set_angle_1(angle):
    duty_cycle = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

def set_angle_2(angle):
    duty_cycle = angle / 18 + 2
    GPIO.output(servo_pin_2, True)
    pwm_2.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(servo_pin_2, False)
    pwm_2.ChangeDutyCycle(0)

def servo_play_and_lcd_update():
    servo1_play()  # 啟動 Servo1
    servo2_play()  # 啟動 Servo2

def servo1_play():
    set_angle_1(95)  # 開門
    time.sleep(3)  # 停 3 秒
    set_angle_1(5)  # 關門

def servo2_play():
    # 旋轉伺服馬達
    set_angle_2(95)  # 開門
    time.sleep(3)  # 停 3 秒
    set_angle_2(5)  # 關門

def excute_angle():
    try:
        # 旋轉伺服馬達
        set_angle_1(0)  # 第一次先關門
        while True:
            set_angle_1(90)  # 開門
            time.sleep(2)
            set_angle_1(0)  # 關門
            set_angle_2(90)  # 關門
            time.sleep(2)
            set_angle_2(0)

    finally:
        pwm.stop()
        pwm_2.stop()
        GPIO.cleanup()

def excute_relay():
    try:
        while True:
            GPIO.output(31, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(31, GPIO.LOW)
            GPIO.output(33, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(33, GPIO.LOW)
            GPIO.output(35, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(35, GPIO.LOW)
            GPIO.output(37, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(37, GPIO.LOW)

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    set_angle_1(5)  # Servo1 第一次先關門
    set_angle_2(5)  # Servo2 第一次先關門
    t1 = threading.Thread(target=rfid_play)
    t1.start()
    t2 = threading.Thread(target=button_play)
    t2.start()
    # t3 = threading.Thread(target=excute_angle)
    # t3.start()
    t4 = threading.Thread(target=traffic_light_play)
    t4.start()
    t5 = threading.Thread(target=excute_relay)
    t5.start()