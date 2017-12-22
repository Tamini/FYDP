import serial
import time

import warnings
import serial
import serial.tools.list_ports
import csv

import numpy as np
import matplotlib.pyplot as plt


# This will check every port and if the Arduino is connected,
# it has a 'CDC' in the description
arduino_ports = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'CDC' in p.description
]

if not arduino_ports:
    raise IOError("No Arduino found")
if len(arduino_ports) > 1:
    warnings.warn('Multiple Arduinos found - using the first')

ser = serial.Serial(arduino_ports[0])


name = raw_input('Name of session: ')
file = open(name + '.csv', 'a')

plt.ion() ## Note this correction
fig=plt.figure()
plt.xlabel('Time (s) ', fontsize=16)
plt.ylabel('Weight (lb)', fontsize=16)
fig.tight_layout();

i=0
x=list()
y=list()

print("connected to: " + ser.portstr)
print('Begin data collection for ' + name + '\n')
# Headers for the CSV file
csv.writer(file).writerow(["Load 1 (lb)", "Load 2 (lb)", "Load 3 (lb)", "Total (lb)"])
while True:
	line = ser.readline()
	values = line.split(",")
	# Check if there are 4 outputs 
	if len(values) == 4:
		totalValue = line.split(",")[3]
		print(totalValue)
		x.append(i);
		y.append(totalValue);
		plt.axhline(40, color='g')
		plt.plot(x, y, 'r');
		plt.show();
		plt.pause(0.0001)
		file.write(line + '\n')
		i+=0.2;
		if len(x) >= 11:
			x.pop(0);
			y.pop(0);
	time.sleep(0.1)
	

file.close()
ser.close()
