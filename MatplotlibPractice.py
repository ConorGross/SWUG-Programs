import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker


df = pd.read_csv("Data.csv") #convert CSV file to dataframe
liveData = df.tail(20) #only pull most recent data

def getMaxSensor(SensorMax):
    liveData[SensorMax].max()
    

def getMinSensor(SensorMin):
    liveData[SensorMin].min()
    

maxMagX = getMaxSensor('MagX') #get max values
maxMagY = getMaxSensor('MagY')
maxMagZ = getMaxSensor('MagZ')
maxTemp = getMaxSensor('TempSensor')
maxTime = getMaxSensor('Time')

minMagX = getMinSensor('MagX') #get min values
minMagY = getMinSensor('MagY')
minMagZ = getMinSensor('MagZ')
minTemp = getMinSensor('TempSensor')
minTime = getMinSensor('Time')


fig, ax = plt.subplots()

twin1 = ax.twinx() #create twin axes for second data set


# placed on the right by twinx above.


p1, = ax.plot(liveData['Time'], liveData['MagX'], "b-", label="Sensor X") #plot first data set
p2, = twin1.plot(liveData['Time'], liveData['TempSensor'], "r-", label="Temperature") #plot second data set


ax.set_xlim(minTime, maxTime) #set limits for axis x
ax.set_ylim(minMagX, maxMagX) #set limits for data 1 y
twin1.set_ylim(minTemp, maxTemp) #set limits for data 2 y


ax.set_xlabel("Time")
ax.set_ylabel("Sensor X")
twin1.set_ylabel("Temperature")


ax.yaxis.label.set_color(p1.get_color())
twin1.yaxis.label.set_color(p2.get_color())

tkw = dict(size=4, width=0.5)

ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
twin1.tick_params(axis='y', colors=p2.get_color(), **tkw)
ax.tick_params(axis='x', **tkw)
def setup(ax, title="LinearLocator(numticks=5)"):
    ax.xaxis.set_major_locator(ticker.LinearLocator(5))
    ax.xaxis.set_minor_locator(ticker.LinearLocator(20))

ax.legend(handles=[p1, p2])

plt.show()