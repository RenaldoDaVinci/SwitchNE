import serial
import numpy as np

import struct
import time
from time import sleep

#ser = serial.Serial(port='COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1, write_timeout = 1)
ser = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600, bytesize=8, parity='N', stopbits=1, write_timeout = 1, dsrdtr = True)

testlist = [0, 0, 0 ,0, 0, 0, 0, 0]
ser.write("<".encode())
print("Sending <")

time.sleep(0.5)

x = 100

ser.write("255, 1, 7, 6, 30, 254, 123, 900".encode())


print("Sending")

time.sleep(0.5)

ser.write(">".encode())
print("Sending >")

item = ser.readline()
item2 = item.strip()
item3 = item2.split()

print(item3)
