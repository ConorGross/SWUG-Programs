import serial
import csv
import pandas as pd
import matplotlib.pyplot as plt

ser = serial.Serial("COM4", 9600) # assign variable 'ser' with magnetometer kit COM4
ser2 = serial.Serial("COM6", 9600) # assign variable 'ser2' with tempersture sensor COM6
count = 0 # initialize counter


while ser.in_waiting >= 0 and count < 20 and ser2.in_waiting >=0: # run a while loop

    mag=str(ser.readline().decode("utf-8")) # convert magnetometer reading to string
    print(mag)
    
    temp=str(ser2.readline().decode("utf-8")) # convert temperature sensor reading to string
    print(temp) 

    x = mag.find('X')
    y = mag.find(',Y')
    z = mag.find(',Z')
        
    with open('Data.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([mag[0:9], mag[10:18], mag[x+2:y], mag[y+3:z], mag[z+3:], temp[13:18]]) #add new data to Data file
    
    count = count + 1 



ser.close() # close port COM4
ser2.close() # close port COM6

