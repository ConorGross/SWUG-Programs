import serial
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from os import path
import datetime


def ensure_datafile():
    if path.exists('DataMag.csv'):
        with open ('DataMag.csv') as file:
            header = [file.readline()]
            if header != ['Date,Time,MagX,MagY,MagZ\n']:
                with open('DataMag.csv', 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Date", "Time", "MagX", "MagY", "MagZ"])
                
    else:
        with open('Data.csv', 'w') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Time", "MagX", "MagY", "MagZ", "TempSensor"])

def read_sensor():
    date = []
    time = []
    magX = []
    magY = []
    magZ = []
    runTime = 0
    ser = serial.Serial("COM4", 9600) # assign variable 'ser' with magnetometer kit COM4

    while ser.in_waiting >= 0 and runTime < 20: # run a while loop

            mag=str(ser.readline().decode("utf-8")) # convert magnetometer reading to string
            print(mag)
            
            x = mag.find('X')
            y = mag.find(',Y')
            z = mag.find(',Z')
            magZ_new = mag[z+3:].strip()
            date_new = mag[0:9].strip()
            #date_format = '%d.%m.%y'
            #date_string = mag[0:9]
            #try: 
            #    datetime.datetime.strptime(date_string, date_format)
            #except ValueError:
            #    date.append(0)
            #    print(date_string)
            #else:
            date.append(date_new)

            #time_format = '%H:%M:%S'
            #time_string = mag[10:18]
            #try: 
            #    datetime.datetime.strptime(time_string, time_format) 
            #except ValueError:
            #    time.append(0)
            #    print(time_string)   
            #else:
            time.append(mag[10:18])

            try:
                int(mag[x+2:y])
            except ValueError:
                magX.append(0)
            else:
                magX.append(mag[x+2:y])

            try:
                int(mag[y+3:z])
            except ValueError:
                magY.append(0)
            else:
                magY.append(mag[y+3:z])

            try:
                int(magZ_new)
            except ValueError:
                magZ.append(0)
            else:
                magZ.append(magZ_new)
            runTime += 1 
    print(date)
    print(magZ)
    with open('DataMag.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        count = 0
        while count < len(date):
            writer.writerow([date[count], time[count], magX[count], magY[count], magZ[count]])
            count = count + 1
        
        file.close

    ser.close() # close port COM4

        
def getMaxSensor(liveData, SensorMax):
    liveData[SensorMax].max()
        

def getMinSensor(liveData, SensorMin):
    liveData[SensorMin].min()

def plot_csv():
    df = pd.read_csv("DataMag.csv") #convert CSV file to dataframe
    liveData = df.tail(20) #only pull most recent data

            

    maxMagX = getMaxSensor(liveData, 'MagX') #get max values
    maxMagY = getMaxSensor(liveData, 'MagY')
    maxMagZ = getMaxSensor(liveData, 'MagZ')
    maxTime = getMaxSensor(liveData, 'Time')

    minMagX = getMinSensor(liveData, 'MagX') #get min values
    minMagY = getMinSensor(liveData, 'MagY')
    minMagZ = getMinSensor(liveData, 'MagZ')
    minTime = getMinSensor(liveData, 'Time')


    fig, ax = plt.subplots()

    p1, = ax.plot(liveData['Time'], liveData['MagZ'], "b-", label="Sensor Z") #plot first data set


    ax.set_xlim(minTime, maxTime) #set limits for axis x
    ax.set_ylim(minMagZ, maxMagZ) #set limits for data 1 y


    ax.set_xlabel("Time")
    ax.set_ylabel("Sensor Z")


    ax.yaxis.label.set_color(p1.get_color())

    tkw = dict(size=4, width=0.5)

    ax.tick_params(axis='y', colors=p1.get_color(), **tkw)
    ax.tick_params(axis='x', **tkw)
    ax.xaxis.set_major_locator(ticker.LinearLocator(5))
    ax.xaxis.set_minor_locator(ticker.LinearLocator(21))


    ax.legend(handles=[p1])

    plt.show()

def main():
    ensure_datafile()
    read_sensor()
    plot_csv()

if __name__ == "__main__":
    main()
        
