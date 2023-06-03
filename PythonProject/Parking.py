import time
import threading
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from RPLCD.i2c import CharLCD

# GPIO 設定 ------------------------------------------------------------
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)  # GPIO.BOARD, 使用BOARD模式

# Servo 每次啟動費用 ----------------------------------------------------
FEE = 10  # 每次費用

# LED PIN -------------------------------------------------------------
led_pin = 38  # 用於 Servo 啟動時燈會亮
GPIO.setup(led_pin, GPIO.OUT)

# Traffic Light (紅綠燈) PIN -------------------------------------------------------------
red_pin = 33  # 紅燈
GPIO.setup(red_pin, GPIO.OUT)
yellow_pin = 35  # 黃燈
GPIO.setup(yellow_pin, GPIO.OUT)
green_pin = 37  # 綠燈
GPIO.setup(green_pin, GPIO.OUT)

# RFID 卡片前二碼 -------------------------------------------------------
CARD_ID_1 = "55"
CARD_ID_2 = "10"

# 選擇控制伺服馬達的 PIN 腳 -----------------------------------------------
servo1_pin = 16  # Servo 1
servo2_pin = 18  # Servo 2
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)
# 設置 Servo PWM 頻率為 50Hz
pwm1 = GPIO.PWM(servo1_pin, 50)
pwm2 = GPIO.PWM(servo2_pin, 50)
pwm1.start(0)
pwm2.start(0)

# 設定 LCD -------------------------------------------------------------
reader = SimpleMFRC522()
lcd = CharLCD('PCF8574', address=0x3f, port=1, backlight_enabled=True)
lcd.clear()  # LCD 清空
lcd.cursor_pos = (0, 0)
lcd.write_string("ID:   N:   $:    ")
lcd.cursor_pos = (1, 0)
lcd.write_string("S1:    S2:    ")

# 設置蜂鳴器引腳和模式 ----------------------------------------------------
buzzer_pin = 12  # 根據BOARD模式，將BCM 18對應的引腳更改為12
GPIO.setup(buzzer_pin, GPIO.OUT)

# 設定 Button ----------------------------------------------------------
button_pin = 40
GPIO.setup(button_pin,GPIO.IN,pull_up_down=GPIO.PUD_UP)


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
            # 首次讀取卡片資料
            id, text = reader.read()
            GPIO.output(buzzer_pin, GPIO.HIGH)
            print("ID: %s\nText: %s" % (id, text))
            leadId = str(id)[0:2]  # 取 RFID 的卡片 ID 前二碼

            count = 1  # 卡片記錄預設資料
            try:
                count = int(text) + 1  # 將卡片內容取出後 +1
            except:
                pass

            # 若 leadId == 指定 CARD_ID 才需要寫入
            if leadId == CARD_ID_1 or leadId == CARD_ID_2:
                try:
                    reader.write(str(count))  # 將累積次數寫入到卡片
                except:
                    pass

            # 顯示在 LCD 螢幕上
            lcd.cursor_pos = (0, 0)
            lcd.write_string("ID:   N:   $:    ")
            lcd.cursor_pos = (0, 3)
            lcd.write_string("%s" % leadId)
            lcd.cursor_pos = (0, 8)
            lcd.write_string("%d" % count)
            lcd.cursor_pos = (0, 13)
            lcd.write_string("%d" % (count * FEE))

            time.sleep(0.1)
            GPIO.output(buzzer_pin, GPIO.LOW)
            time.sleep(0.1)  # 在讀取到卡片後等待一段時間

            # 啟動 Servo & 更新 Servo 在 LCD 上的狀態
            servo_play_and_lcd_update(leadId)

    finally:
        GPIO.cleanup()


def button_play():
    while True:
        time.sleep(0.5)
        # 按下 button 將 LCD 螢幕清空
        button_state = GPIO.input(button_pin)
        # print(button_state)
        if button_state == 0:
            lcd.cursor_pos = (0, 0)
            lcd.write_string("ID:   N:   $:    ")


# 設定 Servo 1 角度
def set_angle1(angle):
    duty_cycle = angle / 18 + 2
    GPIO.output(servo1_pin, True)
    pwm1.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(servo1_pin, False)
    pwm1.ChangeDutyCycle(0)

# 設定 Servo 2 角度
def set_angle2(angle):
    duty_cycle = angle / 18 + 2
    GPIO.output(servo2_pin, True)
    pwm2.ChangeDutyCycle(duty_cycle)
    time.sleep(1)
    GPIO.output(servo2_pin, False)
    pwm2.ChangeDutyCycle(0)


def servo_play_and_lcd_update(leadId):
    # 開燈
    GPIO.output(led_pin, GPIO.HIGH)
    if leadId == CARD_ID_1:
        lcd.cursor_pos = (1, 3)
        lcd.write_string("ON ")
        servo1_play()  # 啟動 Servo1
        lcd.cursor_pos = (1, 3)
        lcd.write_string("OFF")
    elif leadId == CARD_ID_2:
        lcd.cursor_pos = (1, 10)
        lcd.write_string("ON ")
        servo2_play()  # 啟動 Servo2
        lcd.cursor_pos = (1, 10)
        lcd.write_string("OFF")
    # 關燈
    GPIO.output(led_pin, GPIO.LOW)


def servo1_play():
    set_angle1(95)  # 開門
    time.sleep(3)  # 停 3 秒
    set_angle1(5)  # 關門

def servo2_play():
    # 旋轉伺服馬達
    set_angle2(95)  # 開門
    time.sleep(3)  # 停 3 秒
    set_angle2(5)  # 關門

if __name__ == '__main__':
    set_angle1(5)  # Servo1 第一次先關門
    set_angle2(5)  # Servo2 第一次先關門
    t1 = threading.Thread(target=rfid_play)
    t1.start()
    t2 = threading.Thread(target=button_play)
    t2.start()
    # 紅綠燈執行緒
    t3 = threading.Thread(target=traffic_light_play)
    t3.start()


