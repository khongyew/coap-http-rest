import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.animation as animation
from matplotlib import style

import os

# plan:
# 1. open the latest csv file
# 2. perform kmeans on the data
# 3. animate the plot as a live plot 

fig = plt.figure()
ax = fig.add_subplot(111, projection = '3d')

def get_latest_file():
    index = 0
    while os.path.exists('sensor-data-%s.csv' % index):
        index += 1
    filename = 'sensor-data-%s.csv' % (index-1)
    return open(filename, 'r')

def animate(i):
    # Get the latest available csv file
    csv_file = get_latest_file()
    csv_file.readline() # skip the first line

    data = []

    for line in csv_file:
        line = line.split(',')
        
        light = float(line[2])
        temperature = float(line[3])
        humidity = float(line[4])

        data.append([temperature, humidity, light])
    
    data = np.array(data)

    kmeans = KMeans(n_clusters=3)
    kmeans.fit(data)

    data_size = len(data)

    ax.clear()
    ax.scatter(data[:data_size-2,0], data[:data_size-2,1], data[:data_size-2,2], c=kmeans.labels_[:data_size-2], s=10)
    ax.scatter(data[data_size-2:,0], data[data_size-2:,1], data[data_size-2:,2], c='red', s=20, marker='X')

    ax.set_xlabel('temperature')
    ax.set_ylabel('humidity')
    ax.set_zlabel('light')

    csv_file.close()

ani = animation.FuncAnimation(fig, animate, interval=60000)
plt.show()