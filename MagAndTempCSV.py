import serial
import csv
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy
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
    ser = serial.Serial('/dev/ttyUSB0', 9600) # assign variable 'ser' with magnetometer kit COM4
    ser2 = serial.Serial('/dev/ttyACM0', 9600) # assign variable 'ser2' with tempersture sensor COM6
    try:
        while ser.in_waiting >= 0 and ser2.in_waiting >=0: # run a while loop

                mag=str(ser.readline().decode("utf-8")) # convert magnetometer reading to string
                print(mag)
                
                temp=str(ser2.readline().decode("utf-8")) # convert temperature sensor reading to string
                print(temp) 

                x = mag.find('X')
                y = mag.find(',Y')
                z = mag.find(',Z')
                t = temp.find('C')
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
    except KeyboardInterrupt:
        pass

    with open('Data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        count = 0
        while count < len(date):
            writer.writerow([date[count], time[count], magX[count], magY[count], magZ[count], tempSensor[count]])
            count = count + 1
        
        file.close

    ser.close() # close port COM4
    ser2.close() # close port COM6

    

def plot_csv():
    df = pd.read_csv("Data.csv") #convert CSV file to dataframe
    liveData = df.tail(len(df)) #only pull most recent data
    plt.rcParams["figure.autolayout"] = True

    fig, ax = plt.subplots(4,1,sharex=True)
    

    p1 = liveData['MagX']
    p4 = liveData['TempSensor']
    p2 = liveData['MagY']
    p3 = liveData['MagZ']

    x = liveData['Date'] + liveData['Time']

    ax[0].plot(x, p1)
    ax[0].set_title('Sensor X (nT)')
    ax[1].plot(x, p2, 'tab:orange')
    ax[1].set_title('Sensor Y (nT)')
    ax[2].plot(x, p3, 'tab:green')
    ax[2].set_title('Sensor Z (nT)')
    ax[3].plot(x, p4, 'tab:red')
    ax[3].set_title('Temperature (C)')

    ax.get_xgridlines()
    ax.get_ygridlines()

    ax.xaxis.set_major_locator(ticker.LinearLocator(3))
    ax.xaxis.set_minor_locator(ticker.LinearLocator(21))

    plt.show()

def main():
    ensure_datafile()
    read_sensor()
    plot_csv()

if __name__ == "__main__":
    main()
        