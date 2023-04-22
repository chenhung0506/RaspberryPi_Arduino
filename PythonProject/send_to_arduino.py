import time

import serial

def send_data_to_arduino(data):
    time.sleep(1.5)
    ser.write(str(data).encode())

if __name__ == '__main__':
    ser = serial.Serial('COM5', 115200)
    send_data_to_arduino(1)
    send_data_to_arduino(2)
    send_data_to_arduino(4)
    send_data_to_arduino(8)



