import serial
import numpy as np

ser = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600, bytesize=8, parity='N', stopbits=1, write_timeout = 1)

array1 = np.random.rand(8,8)
#said arrays contain random value from 0 to 1, round it so it's a same array with binary bits
Start = np.around(array1)
allzero = np.zeros((8,8))
allhigh = np.zeros((8,8))
for i in range(len(allhigh)):
	for j in range(len(allhigh[i])):
		allhigh[i][j] = 1

bytelist=[]
for k in range(len(Start)):
	tempbits= 0
	print(Start[k])
    #process every lines
	for j in range(len(Start[k])):
		if Start[k][j] == 1:
			tempbits += 2**(7-j)
			#print(tempbits)
	bytelist.append(tempbits)

print(bytelist)
p = bytes(bytelist)
q = bytearray(bytelist)
print(p)
print(bytes(bytelist))
print(q)
print(bytearray(bytelist))
#x = str(bytelist)
#print(x)
#y = bytes(x, 'utf8')
#print(y)
ser.write(p)
'''
hello = [0, 0, 0, 0, 0, 0, 0, 0]
for i in range(0, 256):
    hello[1] = i
    k = bytearray(hello)
    print(k)
    print(":" + str(i))
'''
#print(ser.readline()) # Read the newest output from the Arduino
	#sleep(.8) # Delay for one tenth of a second