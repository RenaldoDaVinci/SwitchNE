import serial
import numpy as np
#from instrument import Keith2400
import SaveLibrary as SaveLib
from time import sleep
'''
exec(open("ivsetup.txt").read())
#Initialize the directory to save the files
savedirectory = SaveLib.createSaveDirectory(filepath, name)
ser = serial.Serial(port='/dev/cu.usbmodem1411', baudrate=9600, bytesize=8, parity='N', stopbits=2, write_timeout = 10)
keithley = Keith2400.Keithley_2400('keithley', 'GPIB0::11')
#set the current limit, in Amp
keithley.compliancei.set(5E-9)
#set the voltage limit in volts just in case something goes wrong from the set up file. DO NOT CHANGE THIS UNLESS YOU KNOW WHAT YOU'RE DOING
keithley.compliancev.set(2)
'''
'''
For this experiment, we suppose all 8 devices are connected, and the electrode 1 of all the devices are to the battery and the remains are to the output.
'''
#Necessary for the IV curve
voltrange = []
steps = Vabs/Vstep + 1
a = np.zeros((4,1,steps))

#Set of voltage range is appended to the voltagerange
first =(np.linspace(0,-Vabs, steps))
a[0] = first
second= (np.linspace(-Vabs, 0,steps))
a[1] = second
third= (np.linspace(0, Vabs, steps))
a[2] = third
fourth = (np.linspace(Vabs, 0, steps))
a[3] = fourth
for b in range(4):
	for c in range(steps):
		voltrange.append(a[b][0][c])

#initialize the IV numpy array and the bytelist to control switch configs
currentlist = np.zeros((8,7,2,4*steps))

for a in range(len(currentlist)):
	#b corresponds to the connection from electrode 1 to the electrode (b+1)
	for b in range(len(currentlist[a])):
		#Initialize bytelist (reset the bytelist everytime new scheme is examined)
		bytelist=[0,0,0,0,0,0,0,0]
		#turn on the battery(switch on the electrode 1 of the selected device)
		bytelist[0] = 2**(7-a)
		#then only turn on the switch that corresponds to the electrode output we want. a controls the x axis of the matrix config(device number) and b controls the y axis of matrix config(electrodes)
		bytelist[b+1] = 2**(7-a)
		#open and wait for the system to settle
		#ser.write(bytelist)
		#time.sleep(0.5)
		#for the range of voltage
		for c in range(len(voltrange)):
			#take money get rich
			'''
			keithley.volt.set(voltrange[c])
			time.sleep(0.05)
			current = keithley.curr()
			currentlist[a][b][0][c] = voltrange[c]
			currentlist[a][b][1][c] = current
			'''

#save the file
SaveLib.saveMain(savedirectory, currentlist)