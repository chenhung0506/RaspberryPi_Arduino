import sys
import time
from RPLCD.i2c import CharLCD
# 樹梅派安裝 sudo pip3 install RPLCD

lcd = CharLCD('PCF8574', address=0x27, port=1, backlight_enabled=True)
try:
    print('按下 Ctrl-C 可停止程式')
    lcd.clear()
    while True:
        lcd.cursor_pos = (0, 0)
        lcd.write_string("Date: {}".format(time.strftime("%Y/%m/%d")))
        lcd.cursor_pos = (1, 0)
        lcd.write_string("Time: {}".format(time.strftime("%H:%M:%S")))
        time.sleep(1)
except KeyboardInterrupt:
    print('關閉程式')
finally:
    lcd.clear()
