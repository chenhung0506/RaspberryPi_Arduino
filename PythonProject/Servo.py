import RPi.GPIO as GPIO
import time

# 選擇控制伺服馬達的GPIO引腳
servo_pin = 18

# 使用BCM模式
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# 設置PWM頻率為50Hz
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def set_angle(angle):
    duty_cycle = angle / 18 + 2
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    # 旋轉伺服馬達
    set_angle(0)
    set_angle(90)
    set_angle(180)
    set_angle(0)

finally:
    pwm.stop()
    GPIO.cleanup()
