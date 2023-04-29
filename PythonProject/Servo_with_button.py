import RPi.GPIO as GPIO
from time import sleep
#Set warnings off (optional)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
#Set Button and LED pins
Button = 32
LED = 26
#Setup Button and LED
GPIO.setup(Button,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED,GPIO.OUT)
flag = 0

while True:
    button_state = GPIO.input(Button)
    if button_state==0:
        sleep(0.5)
        if flag==0:
            print(button_state)
            flag=1
        else:
            print(button_state)
            flag=0
    if flag==1:
        GPIO.output(LED,GPIO.HIGH)
    else:
        GPIO.output(LED,GPIO.LOW)  
