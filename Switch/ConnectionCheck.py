import serial
import numpy as np
#from instrument import Keith2400
import SaveLibrary as SaveLib
from time import sleep
'''
ser = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600, bytesize=8, parity='N', stopbits=2, write_timeout = 10)
keithley = Keith2400.Keithley_2400('keithley', 'GPIB0::11')
'''
'''
For this experiment, we suppose all 8 devices are connected, and the electrode 1 of all the devices are to the battery and the remains are to the output.
'''


#first row won't be used
ConnectionCheck = np.zeros((8,8))
OutputCurrent = np.zeros((8,8))
#set the compliance current
#keithley.compliancei.set(1E-6)
#set the voltage (in volts)
#keithley.volt.set(10E-3)

for z in range(len(OutputCurrent)):
	for y in range(len(OutputCurrent[z])):
		ConnectionCheck[z][y] = 1
		bytelist = []
		for x in range(len(ConnectionCheck)):
			tempbits = 0
			for w in range(len(ConnectionCheck[x])):
				if ConnectionCheck[x][w] == 1:
					tempbits += 2**(7 - w)
			bytelist.append(tempbits)
		bytelist[0] = 255
		print(bytelist)
		#Send the connection configuration
		#ser.write(bytelist)
		#time.sleep(0.5)
		#current = keithley.curr()
		#OutputCurrent[z][y] = current
		ConnectionCheck[z][y] = 0

#All the variables except the first row should give a finite current value.
print(OutputCurrent)
