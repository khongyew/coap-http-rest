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

    ax.clear()
    ax.scatter(data[:,0], data[:,1], data[:,2], c='b', s=10)

    csv_file.close()

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()