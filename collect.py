import serial
import time
import warnings
import serial
import serial.tools.list_ports
import csv

# Put as true to put in headers in .csv file
ENABLE_HEADERS = False
NUMBER_OF_SENSORS = 4


# This function looks through all the ports, and looks for the 'CDC' indicator associated with an Arduino
# Returns serial to the arduino
def find_arduino():
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'CDC' in p.description
        ]
    if not arduino_ports:
        raise IOError("No Arduino found")
    if len(arduino_ports) > 1:
        warnings.warn('Multiple Arduinos found - using the first')
    return serial.Serial(arduino_ports[0])




ser = find_arduino()
name = raw_input('Name of session: ')
file = open(name + '.csv', 'a')

if ENABLE_HEADERS:
    for x in range(0, NUMBER_OF_SENSORS):
        headers.append("Load " + str(x) + " (lb)")
    csv.writer(file).writerow(headers)
    
while True:
    line = ser.readline().decode('utf_8')
    print(line)
    values = line.split(",")
    file.write(line + '\n')
    file.flush()
    time.sleep(0.1)


file.close()
ser.close()

