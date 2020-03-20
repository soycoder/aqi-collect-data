from pms7003 import Pms7003Sensor
import time
import datetime
import g3
import sys
import RPi.GPIO as GPIO
import serial
import csv

airsensor = Pms7003Sensor('/dev/ttyAMA2')
def main():
    isWrited = False
    
    while True:
        
        second = '{:%S}'.format(datetime.datetime.now())
        Timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        TimeRecord = '{:%Y-%m-%d}'.format(datetime.datetime.now())
        
        if second == '59':
            isWrited = False
        if second == '00' and not isWrited:
            pmdata = airsensor.read()
            print('\n'+'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            dict_aqi = { 'PM1': pmdata['pm1_0']
                        ,'PM2.5': pmdata['pm2_5']
                        ,'PM10': pmdata['pm10']
                        }
            for key,val in dict_aqi.items():
                print (key, " => ", val)
                       
            
            with open('data/'+TimeRecord+'-aqi_pm.csv', 'ab') as newFile:
                headers = ['TIME', 'PM1(ug/m^3)','PM2.5(ug/m^3)', 'PM10(ug/m^3)']
                newFileWriter = csv.DictWriter(newFile, fieldnames=headers)
                if newFile.tell() == 0:
                    newFileWriter.writeheader()  # file doesn't exist yet, write a header
            
                newFileWriter.writerow(
                    {  'TIME': Timestamp
                       ,'PM1(ug/m^3)' : str(pmdata['pm1_0'])
                       ,'PM2.5(ug/m^3)' :str(pmdata['pm1_0'])
                       ,'PM10(ug/m^3)' : str(pmdata['pm1_0'])
                    })
            isWrited = True


if __name__ == "__main__":
    main()





