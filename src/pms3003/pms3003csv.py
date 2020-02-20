import Adafruit_DHT
import datetime
import g3
import sys
import RPi.GPIO as GPIO
import serial
import time
import csv

air=g3.g3sensor()

while True:
    second = '{:%S}'.format(datetime.datetime.now())
    Timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    # print(second)
    if second== '00':
        pmdata=air.read("/dev/ttyS0")
        humidity, temperature = Adafruit_DHT.read_retry(11, 4)
        sys.stdout.write('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '\n')
        sys.stdout.write('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity) )
        sys.stdout.write(", PM1: " + str(pmdata[3]))
        sys.stdout.write(", PM10: " + str(pmdata[4]))
        sys.stdout.write(", PM2.5: " + str(pmdata[5]) + '\n')
        with open('aqi_data.csv', 'a') as newFile:
            newFileWriter = csv.writer(newFile)
            # Timestamp,Temp.(?C),Humidity(%),PM1(?g/m3),PM2.5(?g/m3),PM10(?g/m3),CO(ppm),SO2(ppm),O3(ppm),NO2(ppm)
            newFileWriter.writerow([Timestamp,'{0:0.1f}'.format(temperature) \
                                ,'{0:0.1f}'.format(humidity) ,str(pmdata[3]) , str(pmdata[5])  ,str(pmdata[4])        \
                                ])
    time.sleep(0.5)
