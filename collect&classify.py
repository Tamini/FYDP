import serial
import time
import pandas as pd
import warnings
import serial
import serial.tools.list_ports
import csv
import numpy as np
from sklearn import cluster

# Put as true to put in headers in .csv file
ENABLE_HEADERS = False
NUMBER_OF_SENSORS = 4

# Put in number of values the Arduino should be outputting
NUMBER_OF_ARDUINO_OUTPUTS = 5

WRITE_TO_FILE = False

def fetch_training_data():
    config_names = ['_back', '_middle', '_forward']
    config_letters = ['D']

    version = ''

    df_arrays = []

    df = None

    for letter in config_letters:
        df_arrays_inner = []
        for loc in config_names:
            # Load in CSV
            file_name = 'data/config' + letter + '/config' + letter + loc + version + '.csv'
            df = pd.read_csv(file_name)
            df.fillna(0)
            df = df.astype(float)
            df[df < 0 ] = 0

            df_total = df['Total (lb)']

            # Remove Total Column
            df.drop(['Total (lb)'], inplace=True, axis=1)
            df.reset_index(drop=True, inplace=True)

            # Divide by total to get percentages
            for row in range(len(df.index)):
                if (df_total.iloc[row] != 0):
                    df.iloc[row] = df.iloc[row] / df_total.iloc[row]

    return df   

 

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


def cluster_data(training_data, n_clusters):
    kmeans = cluster.KMeans(n_clusters=n_clusters)
    kmeans.fit_transform(training_data)
    labels = kmeans.labels_
    centroids = kmeans.cluster_centers_
    return kmeans

def classify_data(model, testing_data):
    c = model.predict(testing_data)


ser = find_arduino()

if WRITE_TO_FILE:
    name = raw_input('Name of session: ')
    file = open(name + '.csv', 'a')

if ENABLE_HEADERS:
    for x in range(0, NUMBER_OF_SENSORS):
        headers.append("Load " + str(x) + " (lb)")
    csv.writer(file).writerow(headers)
    
training_data = fetch_training_data()
model = cluster_data(training_data, 3)

while True:
    # Added decode to work with Python 3
    line = ser.readline().decode('utf_8')
    values = line.split(",")
    for i, val in enumerate(values):
        if float(val) < 0.5:
            values[i] = 0
            
            
    # Convert data to floats
    data = [float(i) for i in values]
    total = data[-1]
    
    # Convert data into percentanges 
    if total != 0:
        data = [x / total for x in data]
     
    
    # Shape it appropriately for classification function
    reformat_data = np.asarray(data[:-1]).reshape(1, -1)
    
    # Classify
    classify_data(model, reformat_data)

    if WRITE_TO_FILE:
        print(line)
        file.write(line + '\n')
        file.flush()
        
    time.sleep(0.1)


file.close()
ser.close()

