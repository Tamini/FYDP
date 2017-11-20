import serial
import time

ser = serial.Serial(
    port='/dev/cu.usbmodemFD121',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

file = open('sensor_data.csv', 'a')
print("connected to: " + ser.portstr)
name = raw_input('Name of session: ')
file.write('Begin data collection for ' + name + '\n')
while True:
	line = ser.readline()
	if len(line) >= 11:
		print(line)
		file.write(line + '\n')
	time.sleep(1)

file.close()
ser.close()
