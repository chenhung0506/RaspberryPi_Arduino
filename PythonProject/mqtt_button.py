# pip install paho-mqtt
import RPi.GPIO as GPIO
import threading
import paho.mqtt.client as mqtt
from time import sleep

#Set warnings off (optional)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#Set Button and LED pins
button_off = 40
button_on = 38
#Setup Button and LED
GPIO.setup(button_off, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button_on, GPIO.IN, pull_up_down=GPIO.PUD_UP)

current_state = 0  # 將按鈕目前狀態儲存取來, 避免 button debounce 去抖動
def mqtt_off_play():
    global current_state
    while True:
        button_off_state = GPIO.input(button_off)
        if button_off_state == 0:
            if current_state == 1:
                current_state = 0
                print('button off:', button_off_state)
                # Publish a message
                client.publish("pi", "OFF")
                sleep(0.1)


def mqtt_on_play():
    global current_state
    while True:
        button_on_state = GPIO.input(button_on)
        if button_on_state == 0:
            if current_state == 0:
                current_state = 1
                print('button on:', button_on_state)
                # Publish a message
                client.publish("pi", "ON")

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("pi")

def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")



if __name__ == '__main__':
    t1 = threading.Thread(target=mqtt_off_play)
    t1.start()

    t2 = threading.Thread(target=mqtt_on_play)
    t2.start()

    # Create a client
    client = mqtt.Client()

    # Assign callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the broker
    client.connect("192.168.1.157", 1883, 60)

    # Start the loop
    client.loop_start()

    # Run indefinitely
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Exiting...")

    # Stop the loop and disconnect
    client.loop_stop()
    client.disconnect()