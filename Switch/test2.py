
import serial           # import the module
#ComPort = serial.Serial('COM24') # open COM24, windows
ComPort = serial.Serial('/dev/cu.usbmodem1411')
ComPort.baudrate = 9600 # set Baud rate to 9600
ComPort.bytesize = 8    # Number of data bits = 8
ComPort.parity   = 'N'  # No parity
ComPort.stopbits = 1    # Number of Stop bits = 1
# Write character 'A' to serial port
data = bytearray(b'A')
No = ComPort.write(data)
#Read data
#data = ComPort.readline()        # Wait and read data
#print(data)   

ComPort.close()         # Close the Com port