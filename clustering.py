import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.animation as animation
from matplotlib import style

import os, copy, json

# Plan:
# 1. Read the latest csv file
# 2. Split into the number of sensors [0,1,2]
# 3. compute kmeans cluster for each sensor

NUM_OF_SENSORS = 3

def get_latest_file():
    index = 0
    while os.path.exists('sensor-data-%s.csv' % index):
        index += 1
    filename = 'sensor-data-%s.csv' % (index-1)
    return open(filename, 'r')

# Initialise sensor list for each sensor
sensors_readings = []
for i in range(NUM_OF_SENSORS):
    sensors_readings.append([])

# Read the latest CSV file
csv_file = get_latest_file()
csv_file.readline() # Skip the first line

# Parse the CSV file and split the data into
# sensors[0], sensors[1], sensors[2]
for line in csv_file:
    line = line.split(',')

    id = int(line[1])
    light = float(line[2])
    temperature = float(line[3])
    humidity = float(line[4])

    sensors_readings[id].append([temperature, humidity, light])

csv_file.close()

# Convert list to numpy array
for i in range(NUM_OF_SENSORS):
    sensors_readings[i] = np.array(sensors_readings[i])

# KMeans Clustering
kmeans = KMeans(n_clusters=2)
labels = []

# For each sensor, perform clustering and save the generated labels
for i in range(NUM_OF_SENSORS):
    kmeans.fit(sensors_readings[i])
    labels.append(copy.deepcopy(kmeans.labels_))

cluster_data = {}

# Find the number of points in each cluster of each sensor
for i in range(NUM_OF_SENSORS):
    count_0 = 0
    count_1 = 0

    for j in range(len(labels[i])):
        if (labels[i][j] == 0):
            count_0 = count_0 + 1
        else:
            count_1 = count_1 + 1

    cluster_data["sensor" + str(i)] = {"cluster0count" : count_0, "cluster1count": count_1}


json_string = json.dumps(cluster_data)

# write cluster data to file
json_file = open("clustering.json", "wt")
json_file.write(json_string)
json_file.close()


#  Matplotlib Stuffs
# --------------------------------------------------------------------------

# fig = plt.figure()
# ax = fig.add_subplot(111, projection = '3d')
# size = len(sensors[2])
# ax.scatter(sensors[2][:size,0], sensors[2][:size,1], sensors[2][:size,2])
# plt.show()