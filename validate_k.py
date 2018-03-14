import time
import pandas as pd
import warnings
import csv
import numpy as np
from sklearn import cluster

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

print(df)