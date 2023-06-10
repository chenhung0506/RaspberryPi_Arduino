import time

import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import socket

# reader = SimpleMFRC522()
# lcd = CharLCD('PCF8574', address=0x3f, port=1, backlight_enabled=True)

GPIO.setwarnings(False)
Button_PIN = 31
LED_PIN = 35
GPIO.setmode(GPIO.BOARD)  # GPIO.BOARD, 使用BOARD模式
#Setup Button
GPIO.setup(Button_PIN,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# GPIO.setup(33, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)
# GPIO.setup(37, GPIO.OUT)



def button_control_led():
    flag = 0
    try:
        while True:
            button_state = GPIO.input(Button_PIN)
            if button_state==0:
                time.sleep(0.5)
                if flag==0:
                    print(button_state)
                    flag=1
                else:
                    print(button_state)
                    flag=0
            if flag==1:
                GPIO.output(LED_PIN,GPIO.HIGH)
            else:
                GPIO.output(LED_PIN,GPIO.LOW)  
    finally:
        GPIO.cleanup()

if __name__ == '__main__':
    t6 = threading.Thread(target=button_control_led)
    t6.start()
    