import matplotlib.pyplot as plt
import csv
import pandas as pd

#going to use dataframe.tail() function to find and insert last 20 lines of data for graph
#maxSensorX = df['Mag X'].max()
#maxSensorY = df['Mag Y'].max()
#maxSensorZ = df['Mag Z'].max()
#minSensorX = df['Mag X'].min()
#minSensorY = df['Mag Y'].min()
#minSensorZ = df['Mag Z'].min()
#maxTemp = df['Temp Sensor'].max()
#minTemp = df['Temp Sensor'].min()
#maxTime = df['Time'].max()
#minTime = df['Time'].min()

fig, ax = plt.subplots()

twin1 = ax.twinx() #create twin axes for second data set


# placed on the right by twinx above.


p1, = ax.plot(mag[10:18], mag[x+2:y], "b-", label="Sensor X") #plot first data set
p2, = twin1.plot(mag[10:18], temp[13:18], "r-", label="Temperature") #plot second data set


ax.set_xlim(minTime, maxTime) #set limits for axis x
ax.set_ylim(minSensorX, maxSensorX) #set limits for data 1 y
twin1.set_ylim(minTemp, maxTemp) #set limits for data 2 y


ax.set_xlabel("Time")
ax.set_ylabel("Sensor X")
twin1.set_ylabel("Temperature")


ax.yaxis.label.set_color(p1.get_color())
twin1.yaxis.label.set_color(p2.get_color())


tkw = dict(size=4, width=1.5)
ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
ax.tick_params(axis='x', **tkw)

ax.legend(handles=[p1, p2])

plt.show()
