import time

import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import socket

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', address=0x3f, port=1, backlight_enabled=True)

GPIO.setwarnings(False)

# 設置蜂鳴器引腳和模式
buzzer_pin = 12  # 根據BOARD模式，將BCM 18對應的引腳更改為12
GPIO.setmode(GPIO.BOARD)  # GPIO.BOARD, 使用BOARD模式
GPIO.setup(buzzer_pin, GPIO.OUT)
#Setup Button
button_pin = 32
GPIO.setup(button_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# LCD clear
lcd.clear()

relay_1=31
relay_2=33
relay_3=35
relay_4=37

GPIO.setup(relay_1, GPIO.OUT)
GPIO.setup(relay_2, GPIO.OUT)
GPIO.setup(relay_3, GPIO.OUT)
GPIO.setup(relay_4, GPIO.OUT)


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
            lcd.write_string(button_state)
            lcd.cursor_pos = (1, 0)
            lcd.write_string(ip)

def excute_relay():
    try:
        while True:
            GPIO.output(relay_1, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(relay_1, GPIO.LOW)
            GPIO.output(relay_2, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(relay_2, GPIO.LOW)
            GPIO.output(relay_3, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(relay_3, GPIO.LOW)
            GPIO.output(relay_4, GPIO.HIGH)
            time.sleep(1)                                         
            GPIO.output(relay_4, GPIO.LOW)

    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    t2 = threading.Thread(target=button_play)
    t2.start()

    t5 = threading.Thread(target=excute_relay)
    t5.start()