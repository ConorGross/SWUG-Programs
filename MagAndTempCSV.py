import serial
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from os import path
import datetime


def ensure_datafile():
    if path.exists('Data.csv'):
        with open ('Data.csv') as file:
            header = [file.readline()]
            if header != ['Date,Time,MagX,MagY,MagZ,TempSensor\n']:
                with open('Data.csv', 'w') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Date", "Time", "MagX", "MagY", "MagZ", "TempSensor"])
                
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
    tempSensor = []
    runTime = 0
    ser = serial.Serial("COM4", 9600) # assign variable 'ser' with magnetometer kit COM4
    ser2 = serial.Serial("COM6", 9600) # assign variable 'ser2' with tempersture sensor COM6

    while ser.in_waiting >= 0 and runTime < 20 and ser2.in_waiting >=0: # run a while loop

            mag=str(ser.readline().decode("utf-8")) # convert magnetometer reading to string
            print(mag)
            
            temp=str(ser2.readline().decode("utf-8")) # convert temperature sensor reading to string
            print(temp) 

            x = mag.find('X')
            y = mag.find(',Y')
            z = mag.find(',Z')
            t = temp.find('C')

            date_format = '%d.%m.%y'
            date_string = mag[0:8]
            try: 
                datetime.datetime.strptime(date_string, date_format) 
            except ValueError:
                date.append(0)
            else:
                date.append(mag[0:9])

            time_format = '%H:%M:%S'
            time_string = mag[10:18]
            try: 
                datetime.datetime.strptime(time_string, time_format)    
            except ValueError:
                time.append(0)
            else:
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
                int(mag[z+3:])
            except ValueError:
                magZ.append(0)
            else:
                magZ.append(mag[z+3:])

            if(t == -1):
                print("We were not able to find C")
                tempSensor.append(0)
            else:
                try:
                    float(temp[t-6:t-1])
                except ValueError:
                    tempSensor.append(0)
                else:
                    tempSensor.append(temp[t-6:t-1])

            runTime += 1 

    with open('Data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            count = 0
            while count < len(date):
                if tempSensor[count] == 0:
                    count += 1
                else:
                    writer.writerow([date[count], time[count], magX[count], magY[count], magZ[count], tempSensor[count]])
                    count += 1
            
            file.close

    ser.close() # close port COM4
    ser2.close() # close port COM6

        
def getMaxSensor(liveData, SensorMax):
    liveData[SensorMax].max()
        

def getMinSensor(liveData, SensorMin):
    liveData[SensorMin].min()

def plot_csv():
    df = pd.read_csv("Data.csv") #convert CSV file to dataframe
    liveData = df.tail(20) #only pull most recent data

            

    maxMagX = getMaxSensor(liveData, 'MagX') #get max values
    maxMagY = getMaxSensor(liveData, 'MagY')
    maxMagZ = getMaxSensor(liveData, 'MagZ')
    maxTemp = getMaxSensor(liveData, 'TempSensor')
    maxTime = getMaxSensor(liveData, 'Time')

    minMagX = getMinSensor(liveData, 'MagX') #get min values
    minMagY = getMinSensor(liveData, 'MagY')
    minMagZ = getMinSensor(liveData, 'MagZ')
    minTemp = getMinSensor(liveData, 'TempSensor')
    minTime = getMinSensor(liveData, 'Time')


    fig, ax = plt.subplots()

    twin1 = ax.twinx() #create twin axes for second data set

    p1, = ax.plot(liveData['Time'], liveData['MagZ'], "b-", label="Sensor X") #plot first data set
    p2, = twin1.plot(liveData['Time'], liveData['TempSensor'], "r-", label="Temperature") #plot second data set


    ax.set_xlim(minTime, maxTime) #set limits for axis x
    ax.set_ylim(minMagZ, maxMagZ) #set limits for data 1 y
    twin1.set_ylim(minTemp, maxTemp) #set limits for data 2 


    ax.set_xlabel("Time")
    ax.set_ylabel("Sensor Z")
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

def main():
    ensure_datafile()
    read_sensor()
    plot_csv()

if __name__ == "__main__":
    main()
        
