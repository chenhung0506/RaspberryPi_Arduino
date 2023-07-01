import time

import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import socket

reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', address=0x3f, port=1, backlight_enabled=True)
lcd.clear()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

buzzer_pin = 12  # 根據BOARD模式，將BCM 18對應的引腳更改為12
GPIO.setup(buzzer_pin, GPIO.OUT)

button_pin = 26
button_1 = 32
button_2 = 36
button_3 = 38
button_4 = 40
GPIO.setup(button_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_3,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_4,GPIO.IN,pull_up_down=GPIO.PUD_UP)

relay_1=31
relay_2=33
relay_3=35
relay_4=37
GPIO.setup(relay_1, GPIO.OUT)
GPIO.setup(relay_2, GPIO.OUT)
GPIO.setup(relay_3, GPIO.OUT)
GPIO.setup(relay_4, GPIO.OUT)

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
    flag = 0
    while True:
        time.sleep(0.5)
        # 按下 button 將 LCD 螢幕清空
        button_state_0 = GPIO.input(button_pin)
        if button_state_0 == 0:
            time.sleep(0.5)
            if flag==0:
                flag=1
                lcd.cursor_pos = (1, 0)
                lcd.write_string(ip)
                execute_buzzer()
            else:
                flag=0
                lcd.cursor_pos = (1, 0)
                lcd.write_string('IP:'+ str(ip))
                execute_buzzer()

def execute_buzzer():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(buzzer_pin, GPIO.LOW)

def button_control_led(button, relay):
    flag = 0
    try:
        while True:
            button_state = GPIO.input(button)
            if button_state==0:
                execute_buzzer()
                if flag==0:
                    print("button:{0}, relay: {1}, button_state: {2}".format(str(button), str(relay), str(button_state)))
                    flag=1
                else:
                    print("button:{0}, relay: {1}, button_state: {2}".format(str(button), str(relay), str(button_state)))
                    flag=0
            if flag==1:
                GPIO.output(relay, GPIO.HIGH)
            else:
                GPIO.output(relay, GPIO.LOW)  
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    # 顯示 IP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    lcd.cursor_pos = (0, 0)
    lcd.write_string(ip)

    t1 = threading.Thread(target=button_control_led, args=(button_1, relay_1))
    t1.start()
    t2 = threading.Thread(target=button_control_led, args=(button_2, relay_2))
    t2.start()
    t3 = threading.Thread(target=button_control_led, args=(button_3, relay_3))
    t3.start()
    t4 = threading.Thread(target=button_control_led, args=(button_4, relay_4))
    t4.start()