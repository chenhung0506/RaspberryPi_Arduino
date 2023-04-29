import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# 設置蜂鳴器引腳和模式
buzzer_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    while True:
        print("請將卡靠近讀卡器...")
        GPIO.output(buzzer_pin, GPIO.LOW)
        id, text = reader.read()
        GPIO.output(buzzer_pin, GPIO.HIGH)
        print("ID: %s\nText: %s" % (id, text))
        time.sleep(0.5)
        GPIO.output(buzzer_pin, GPIO.LOW)
        time.sleep(0.5)
finally:
    GPIO.cleanup()
