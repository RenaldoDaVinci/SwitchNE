import serial
import numpy as np

<<<<<<< HEAD:Switch/sending.py
ser = serial.Serial(port='COM3', baudrate=9600, bytesize=8, parity='N', stopbits=1, write_timeout = 1)
=======
ser = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600, bytesize=8, parity='N', stopbits=2, write_timeout = 10)
>>>>>>> 8dd8bc1e40b51084f56d261991fab239e63fe962:Switch/TestFolders/sending.py

array1 = np.random.rand(8,8)
#said arrays contain random value from 0 to 1, round it so it's a same array with binary bits
Start = np.around(array1)
allzero = np.zeros((8,8))
allhigh = np.zeros((8,8))
for i in range(len(allhigh)):
	for j in range(len(allhigh[i])):
		allhigh[i][j] = 1

bytelist=[]
bytelist2=[]
bytelist3=[]
for k in range(len(Start)):
	tempbits= 0
<<<<<<< HEAD:Switch/sending.py
	print(Start[k])
    #process allhighallhigh lines
=======
	#print(Start[k])
    #process every lines
>>>>>>> 8dd8bc1e40b51084f56d261991fab239e63fe962:Switch/TestFolders/sending.py
	for j in range(len(Start[k])):
		if Start[k][j] == 1:
			tempbits += 2**(7-j)
			#print(tempbits)
	bytelist.append(tempbits)

for k in range(len(allhigh)):
	tempbits= 0
	#print(allhigh[k])
    #process every lines
	for j in range(len(allhigh[k])):
		if allhigh[k][j] == 1:
			tempbits += 2**(7-j)
			#print(tempbits)
	bytelist2.append(tempbits)

for k in range(len(allzero)):
	tempbits= 0
	#print(allzero[k])
    #process every lines
	for j in range(len(allzero[k])):
		if allzero[k][j] == 1:
			tempbits += 2**(7-j)
			#print(tempbits)
	bytelist3.append(tempbits)

print(bytelist)
<<<<<<< HEAD:Switch/sending.py
p = bytes(bytelist)
q = bytearray(bytelist)
print(p)
#print(bytes(bytelist))
print(q)
#print(bytearray(bytelist))
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
=======
print(bytelist2)
print(bytelist3)
y = bytes(bytelist)
ser.write(y)
>>>>>>> 8dd8bc1e40b51084f56d261991fab239e63fe962:Switch/TestFolders/sending.py
