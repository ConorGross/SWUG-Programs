import serial
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


ser = serial.Serial("COM4", 9600) # assign variable 'ser' with magnetometer kit COM4
ser2 = serial.Serial("COM6", 9600) # assign variable 'ser2' with tempersture sensor COM6
count = 0 # initialize counter
date = []
time = []
magX = []
magY = []
magZ = []
tempSensor = []

while ser.in_waiting >= 0 and count < 20 and ser2.in_waiting >=0: # run a while loop

    mag=str(ser.readline().decode("utf-8")) # convert magnetometer reading to string
    print(mag)
    
    temp=str(ser2.readline().decode("utf-8")) # convert temperature sensor reading to string
    print(temp) 

    x = mag.find('X')
    y = mag.find(',Y')
    z = mag.find(',Z')
    t = temp.find('C')

    date.append(mag[0:9])
    time.append(mag[10:18])
    magX.append(mag[x+2:y])
    magY.append(mag[y+3:z])
    magZ.append(mag[z+3:])
    tempSensor.append(temp[t-6:t-1])

    count = count + 1 

with open('Data.csv', 'a', newline='') as file:
   writer = csv.writer(file)
   count = 0
   while count < len(date):
     writer.writerow([date[count], time[count], magX[count], magY[count], magZ[count], tempSensor[count]])
     count = count + 1
   
file.close

ser.close() # close port COM4
ser2.close() # close port COM6


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
ax.xaxis.set_major_locator(ticker.LinearLocator(5))
ax.xaxis.set_minor_locator(ticker.LinearLocator(21))


ax.legend(handles=[p1, p2])

plt.show()

