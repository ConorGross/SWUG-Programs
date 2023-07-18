import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#def getMaxSensor(liveData, SensorMax):
    #liveData[SensorMax].max()
        

#def getMinSensor(liveData, SensorMin):
 #   liveData[SensorMin].min()

df = pd.read_csv("Data.csv") #convert CSV file to dataframe
liveData = df.tail(20) #only pull most recent data
plt.rcParams["figure.autolayout"] = True
        

#maxMagX = getMaxSensor(liveData, 'MagX') #get max values
#maxMagY = getMaxSensor(liveData, 'MagY')
#maxMagZ = getMaxSensor(liveData, 'MagZ')
#maxTemp = getMaxSensor(liveData, 'TempSensor')
#maxTime = getMaxSensor(liveData, 'Time')

#minMagX = getMinSensor(liveData, 'MagX') #get min values
##minMagZ = getMinSensor(liveData, 'MagZ')
#minTemp = getMinSensor(liveData, 'TempSensor')
#minTime = getMinSensor(liveData, 'Time')


fig, ax = plt.subplots(2,2)


x = liveData['Time']

p1 = liveData['MagX']
p2 = liveData['TempSensor']
p3 = liveData['MagY']
p4 = liveData['MagZ']


ax[0, 0].plot(x, p1)
ax[0, 0].set_title('Sensor X')
ax[0, 1].plot(x, p2, 'tab:orange')
ax[0, 1].set_title('Temperature')
ax[1, 0].plot(x, p3, 'tab:green')
ax[1, 0].set_title('Sensor Y')
ax[1, 1].plot(x, p4, 'tab:red')
ax[1, 1].set_title('Sensor Z')

ax[0,0].xaxis.set_major_locator(ticker.LinearLocator(3))
ax[0,0].xaxis.set_minor_locator(ticker.LinearLocator(21))
ax[0,1].xaxis.set_major_locator(ticker.LinearLocator(3))
ax[0,1].xaxis.set_minor_locator(ticker.LinearLocator(21))
ax[1,0].xaxis.set_major_locator(ticker.LinearLocator(3))
ax[1,0].xaxis.set_minor_locator(ticker.LinearLocator(21))
ax[1,1].xaxis.set_major_locator(ticker.LinearLocator(3))
ax[1,1].xaxis.set_minor_locator(ticker.LinearLocator(21))

plt.show()