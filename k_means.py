import pandas as pd
import numpy as np
from sklearn import cluster

config_names = ['_middle']
config_letters = ['A', 'B', 'C', 'D', 'E']

version = ''

df_arrays = []

df = None

for letter in config_letters:
	for loc in config_names:
		# Load in CSV
		file_name = 'data/config' + letter + '/config' + letter + loc + version + '.csv'
		df = pd.read_csv(file_name)
		df = df.astype(float)

		# Remove very low values
		df = df[df['Total (lb)'].apply(lambda x: x > 5)]
		df[df < 0 ] = 0

		df_total = df['Total (lb)']

		# Remove Total Column
		df.drop(['Total (lb)'], inplace=True, axis=1)
		df.reset_index(drop=True, inplace=True)

		# Divide by total to get percentages
		for row in range(len(df.index)):
			df.iloc[row] = df.iloc[row] / df_total.iloc[row]

		df_arrays.append(df.values)

k = 3

for arr in df_arrays:
	kmeans = cluster.KMeans(n_clusters=k)
	kmeans.fit(arr)
	labels = kmeans.labels_
	centroids = kmeans.cluster_centers_
	print("The # of clusters is " + str(k))
	print("The labels are " + str(labels))
	print("The centroids are " + str(centroids))
	print()
