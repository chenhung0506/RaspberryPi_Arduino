import time

import threading
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD
import socket

# reader = SimpleMFRC522()
# lcd = CharLCD('PCF8574', address=0x3f, port=1, backlight_enabled=True)

GPIO.setwarnings(False)
Button_PIN_1 = 31
Button_PIN_2 = 33
LED_PIN_1 = 35
LED_PIN_2 = 37
GPIO.setmode(GPIO.BOARD)  # GPIO.BOARD, 使用BOARD模式
GPIO.setup(Button_PIN_1,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(Button_PIN_2,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)


# MQTT broker details
broker_address = "127.0.0.1"
broker_port = 1883
topic = "relay1"




def button_control_led_1():
    flag = 0
    try:
        while True:
            button_state_1 = GPIO.input(Button_PIN_1)
            if button_state_1==0:
                time.sleep(0.5)
                if flag==0:
                    print(button_state_1)
                    flag=1
                else:
                    print(button_state_1)
                    flag=0
            if flag==1:
                GPIO.output(LED_PIN_1,GPIO.HIGH)
            else:
                GPIO.output(LED_PIN_1,GPIO.LOW)  
    finally:
        GPIO.cleanup()
        
def button_control_led_2():
    flag = 0
    try:
        while True:
            button_state_1 = GPIO.input(Button_PIN_2)
            if button_state_1==0:
                time.sleep(0.5)
                if flag==0:
                    print(button_state_1)
                    flag=1
                else:
                    print(button_state_1)
                    flag=0
            if flag==1:
                GPIO.output(LED_PIN_2,GPIO.HIGH)
            else:
                GPIO.output(LED_PIN_2,GPIO.LOW)  
    finally:
        GPIO.cleanup()

def control_led_1(input):
    # flag = 0
    # if input==0:
    #     if flag==0:
    #         print(input)
    #         flag=1
    #     else:
    #         print(input)
    #         flag=0
    if input==1:
        GPIO.output(LED_PIN_1,GPIO.HIGH)
    else:
        GPIO.output(LED_PIN_1,GPIO.LOW)    
        

# 當地端程式連線伺服器得到回應時，要做的動作
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("pi")

# 當接收到從伺服器發送的訊息時要進行的動作
def on_message(client, userdata, msg):
    # 轉換編碼utf-8才看得懂中文
    data = msg.payload.decode('utf-8')
    print(msg.topic+" "+ data)
    if data == 'ON':
        GPIO.output(LED_PIN_1, GPIO.HIGH)
    else:
        GPIO.output(LED_PIN_1, GPIO.LOW)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(broker_address, broker_port)
    client.subscribe(topic)
    client.loop_start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        pass

    # Disconnect from the MQTT broker
    client.disconnect()

    # t6 = threading.Thread(target=button_control_led_1)
    # t6.start()
    # t6 = threading.Thread(target=button_control_led_2)
    # t6.start()
