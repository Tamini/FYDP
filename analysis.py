import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def saveFig(fig, path):
	fig.set_size_inches(24,18)
	fig.savefig(path)

def graphTestType(dfs, config_letters, legends, img):
	fig, axes = plt.subplots(nrows=2, ncols=3)
	graph_row = 0
	graph_col = 0
	for i in range(len(config_letters)):
		dfs[i].plot.bar(ax=axes[graph_row, graph_col], title='config' + config_letters[i])
		axes[graph_row,graph_col].legend(legends[i])
		graph_col += 1
		if(graph_col > 2):
			graph_col = 0
			graph_row += 1
	
	plt.subplot(2,3,6)
	plt.imshow(img)
	return fig


config_names = ['_back', '_forward', '_left', '_middle', '_right', '_rock']
config_letters = ['A', 'B', 'C', 'D', 'E']
legends = [['Back Left', 'Front Right', 'Back Right', 'Front Left'], ['Mid Left', 'Mid Right', 'Back', 'Front'], ['Front Left', 'Front Right', 'Front Mid', 'Mid'], ['Mid Left', 'Mid Right', 'Mid', 'Front'], ['Front Left', 'Front Right', 'MidMid Right', 'MidMid Left']]

backs = []
forwards = []
lefts = []
middles = []
rights = []
rocks = []

version = ''
config_num = 0

# Ingest data and graph each configuration separately
for letter in config_letters:
	fig, axes = plt.subplots(nrows=2, ncols=3)
	graph_row = 0
	graph_col = 0
	for loc in config_names:
		file_name = 'data/config' + letter + '/config' + letter + loc + version + '.csv'
		df = pd.read_csv(file_name)
		df = df.astype(float)
		# Filter garbage values
		df = df[df['Total (lb)'].apply(lambda x: x > 5)]
		df[df < 0 ] = 0
		df.drop(['Total (lb)'], inplace=True, axis=1)
		df.reset_index(drop=True, inplace=True)
		if (loc == '_back'):
			backs.append(df)
		elif (loc == '_forward'):
			forwards.append(df)
		elif (loc == '_left'):
			lefts.append(df)
		elif (loc == '_middle'):
			middles.append(df)
		elif (loc == '_right'):
			rights.append(df)
		elif (loc == '_rock'):
			rocks.append(df)
		df.plot.bar(ax=axes[graph_row, graph_col], title='config' + letter + loc + version)
		axes[graph_row,graph_col].legend(legends[config_num])
		graph_col += 1
		if(graph_col > 2):
			graph_col = 0
			graph_row += 1

	config_num += 1
	figure_name = './figures/configs/config_' + letter
	fig.set_size_inches(24,18)
	fig.savefig(figure_name)
	print('Done ', letter)

print('Creating graphs by test type')
config_img = mpimg.imread('configs.png')
output = graphTestType(backs, config_letters, legends, config_img)
saveFig(output, 'figures/tests/back')
output = graphTestType(forwards, config_letters, legends, config_img)
saveFig(output, 'figures/tests/forward')
output = graphTestType(lefts, config_letters, legends, config_img)
saveFig(output, 'figures/tests/left')
output = graphTestType(rights, config_letters, legends, config_img)
saveFig(output, 'figures/tests/right')
output = graphTestType(middles, config_letters, legends, config_img)
saveFig(output, 'figures/tests/middle')
output = graphTestType(rocks, config_letters, legends, config_img)
saveFig(output, 'figures/tests/rock')