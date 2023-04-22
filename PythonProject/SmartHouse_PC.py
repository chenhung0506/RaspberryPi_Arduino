'''
GUI
+------+------+------+------+
| 溫度 | 25 C | 濕度  | 53 % |
+------+------+------+------+
|    Data    |      77      |
+------+------+------+------+
| LED1 | LED2 | LED3 | LED3 |
+------+------+------+------+

Arduino: SmartHouse.ino
https://github.com/vincenttuan/2023_RaspberryPi_Arduino/blob/main/Arduino/SmartHouse/SmartHouse.ino
'''

import tkinter
import threading
import time
import requests
import serial
from tkinter import font
import time
import json

ser = ''
data = ''

def lcd_display():
    pass

def upload_firebase():
    while True:
        firebase_url = 'https://你的FB.firebaseio.com/'
        upload_data = {'data': data}
        result = requests.put(firebase_url + '/raspberry.json', verify=True, data=json.dumps(upload_data))
        print(result)
        time.sleep(1)


def led1_click() :
    t1 = threading.Thread(target=send_data_to_arduino, args=(1,))
    t1.start()

def led2_click() :
    t1 = threading.Thread(target=send_data_to_arduino, args=(2,))
    t1.start()

def led3_click() :
    t1 = threading.Thread(target=send_data_to_arduino, args=(4,))
    t1.start()

def led4_click() :
    t1 = threading.Thread(target=send_data_to_arduino, args=(8,))
    t1.start()

def send_data_to_arduino(data):
    #time.sleep(0.5)
    ser.write(str(data).encode())

def rev_data_from_arduino():
    global ser
    ser = serial.Serial('COM8', 115200)
    time.sleep(1)
    while True:
        try:
            if ser.in_waiting > 0:
                global data
                data = ser.readline().decode().rstrip()
                print("收到 arduino 的資料:", data)
                dataArray = data.split(",")
                data_value.set(dataArray[0])
                temp_value.set(dataArray[1] + '°C')
                humd_value.set(dataArray[2] + '%')
                # LED/Relay Control
                if dataArray[3] == '1':
                    led1_value.set('LED1\nON')
                    led2_value.set('LED2')
                    led3_value.set('LED3')
                    led4_value.set('LED4')
                elif dataArray[4] == '1':
                    led1_value.set('LED1')
                    led2_value.set('LED2\nON')
                    led3_value.set('LED3')
                    led4_value.set('LED4')
                elif dataArray[5] == '1':
                    led1_value.set('LED1')
                    led2_value.set('LED2')
                    led3_value.set('LED3\nON')
                    led4_value.set('LED4')
                elif dataArray[6] == '1':
                    led1_value.set('LED1')
                    led2_value.set('LED2')
                    led3_value.set('LED3')
                    led4_value.set('LED4\nON')



        except Exception as e:
            print('斷線~請檢查 USB 線')
            time.sleep(3)
            # 重新連線
            try:
                ser = serial.Serial('COM5', 115200)
            except:
                pass

if __name__ == '__main__':
    win = tkinter.Tk()
    win.title('Smart House')
    win.geometry('700x500')

    myfont = font.Font(family='Arial', size=24, weight='bold')

    temp_value = tkinter.StringVar()
    temp_value.set('0°C')
    humd_value = tkinter.StringVar()
    humd_value.set('0%')
    data_value = tkinter.StringVar()
    data_value.set('0')
    led1_value = tkinter.StringVar()
    led1_value.set('LED1')
    led2_value = tkinter.StringVar()
    led2_value.set('LED2')
    led3_value = tkinter.StringVar()
    led3_value.set('LED3')
    led4_value = tkinter.StringVar()
    led4_value.set('LED4')

    # view 元件
    temp_label = tkinter.Label(text='溫度', font=myfont)
    humd_label = tkinter.Label(text='濕度', font=myfont)
    temp_value_label = tkinter.Label(textvariable=temp_value, font=myfont)
    humd_value_label = tkinter.Label(textvariable=humd_value, font=myfont)
    data_label = tkinter.Label(text='Data', font=myfont)
    data_value_label = tkinter.Label(textvariable=data_value, font=myfont)
    led1_button = tkinter.Button(textvariable=led1_value, font=myfont, command=led1_click)
    led2_button = tkinter.Button(textvariable=led2_value, font=myfont, command=led2_click)
    led3_button = tkinter.Button(textvariable=led3_value, font=myfont, command=led3_click)
    led4_button = tkinter.Button(textvariable=led4_value, font=myfont, command=led4_click)

    win.rowconfigure((0, 1, 2), weight=1)  # 列 0, 1, 2 同步放大與縮小
    win.columnconfigure((0, 1, 2, 3), weight=1)  # 欄 0, 1, 2, 3 同步放大與縮小

    # 將 view 元件配置到 grid 元件中
    # 第一列
    temp_label.grid(row=0, column=0, sticky='EWNS')
    temp_value_label.grid(row=0, column=1, sticky='EWNS')
    humd_label.grid(row=0, column=2, sticky='EWNS')
    humd_value_label.grid(row=0, column=3, sticky='EWNS')
    # 第二列
    data_label.grid(row=1, column=0, columnspan=2, sticky='EWNS')
    data_value_label.grid(row=1, column=2, columnspan=2, sticky='EWNS')
    # 第三列
    led1_button.grid(row=2, column=0, sticky='EWNS')
    led2_button.grid(row=2, column=1, sticky='EWNS')
    led3_button.grid(row=2, column=2, sticky='EWNS')
    led4_button.grid(row=2, column=3, sticky='EWNS')

    # 啟動一條執行緒去執行(接收 Arduino)
    t1 = threading.Thread(target=rev_data_from_arduino)
    t1.start()

    # 啟動一條執行緒去執行(LCD 顯示)
    t2 = threading.Thread(target=lcd_display)
    t2.start()

    # 啟動一條執行緒去執行(上傳到 Firebase)
    t3 = threading.Thread(target=upload_firebase)
    t3.start()

    win.mainloop()







