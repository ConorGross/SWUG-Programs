import serial # import serial module

File_data = open("Data.txt", "a")
ser = serial.Serial("COM4", 9600) # assign variable 'ser' with magnetometer kit COM4
ser2 = serial.Serial("COM6", 9600) # assign variable 'ser2' with tempersture sensor COM6
count = 0 # initialize counter

while ser.in_waiting >= 0 and count < 100 and ser2.in_waiting >=0: # run a while loop for 100 seconds

    mag=str(ser.readline().decode("utf-8")) # convert magnetometer reading to string
    print(mag)
    File_data.write(mag) 
    temp=str(ser2.readline().decode("utf-8")) # convert temperature sensor reading to string
    print(temp) 
    File_data.write(temp)
    count = count + 1 

File_data.close()
ser.close() # close port COM4
ser2.close() # close port COM6
