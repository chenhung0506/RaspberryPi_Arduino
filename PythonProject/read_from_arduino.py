import time

import serial


if __name__ == '__main__':
    ser = serial.Serial('COM5', 115200)
    while True:
        try:
            if ser.in_waiting > 0:
                data = ser.readline().decode().rstrip()
                print("收到 arduino 的資料:", data)
        except Exception as e:
            print('斷線~請檢查 USB 線')
            time.sleep(3)
            # 重新連線
            try:
                ser = serial.Serial('COM5', 115200)
            except:
                pass

