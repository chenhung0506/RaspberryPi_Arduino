import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

# 設置蜂鳴器引腳和模式
buzzer_pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(buzzer_pin, GPIO.OUT)

try:
    print("請將卡靠近讀卡器...")
    GPIO.output(buzzer_pin, GPIO.HIGH)
    id, text = reader.read()
    GPIO.output(buzzer_pin, GPIO.LOW)
    print("ID: %s\nText: %s" % (id, text))

finally:
    GPIO.cleanup()
