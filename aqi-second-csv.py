from mcp3208 import MCP3208
import time
import datetime
import g3
import sys
import RPi.GPIO as GPIO
import serial
import csv

air = g3.g3sensor()
adc = MCP3208()
name_ch_mcp = ['O3', 'NO2', 'CO', 'SO2',
               'Wind Speed', 'Wind Direction', ' ', ' ']


def getO3():
    o3 = adc.read(0) / 4095.0 * 5.0
    str_o3 = '{:.2f}'.format(o3)
    aqi_o3 = 10 * ( 2.0 - float(str_o3) )
    #aqi_o3 = float(str_o3)
    return aqi_o3

def getNO2():
    no2 = adc.read(1) / 4095.0 * 5.0
    str_no2 = '{:.4f}'.format(no2)
    aqi_no2 = 10 * ( 2.0 - float(str_no2) )
    #aqi_no2 = float(str_no2)
    if aqi_no2 < 0:
        aqi_no2 = 0
    return aqi_no2


def getCO():
    co = adc.read(2) / 4095.0 * 5.0
    str_co = '{:.2f}'.format(co)
    aqi_co = 200.0/(0.3) * (float(str_co) - 0.6)
    #aqi_co = float(str_co)
    return aqi_co


def getSO2():
    so2 = adc.read(3) / 4095.0 * 5.0
    str_so2 = '{:.4f}'.format(so2)
    aqi_so2 = 0.4/(0.3) * (float(str_so2)-0.6)
    #aqi_so2 = float(str_so2)
    if aqi_so2 < 0:
        aqi_so2 = 0
    return aqi_so2


def getWindSpeed():
    w_speed = adc.read(4) / 4095.0 * 5.0
    w_speed = adc.read(4) - 11
    if w_speed < 0:
        w_speed = 0
    return w_speed%360


def getWindDirection():
    w_di = (adc.read(5) / 4095.0) * 360.0
    return w_di


def main():
    isWrited = False
    while True:
        second = '{:%S}'.format(datetime.datetime.now())
        Timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        TimeRecord = '{:%Y-%m-%d}'.format(datetime.datetime.now())
        
        if second == '59':
            isWrited = False
        if second == '00' and not isWrited:
            pmdata = air.read("/dev/ttyS0")
            print('\n'+'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            dict_aqi = { 'PM1': pmdata[3]
                        ,'PM2.5': pmdata[5]
                        ,'PM10': pmdata[4]
                        ,'O3' : format(getO3(), '.2f')
                        ,'NO2': format(getNO2(), '.2f')
                        ,'CO' : format(getCO(), '.2f')
                        ,'SO2': format(getSO2(), '.2f')
                        ,'WS' : format(getWindSpeed(), '.2f')
                        ,'WDI': format(getWindDirection(), '.2f')}
            for key,val in dict_aqi.items():
                print key, "=>", val
                       
            
            with open('data/'+TimeRecord+'-aqi_part2.csv', 'ab') as newFile:
                headers = ['TIME', 'PM1(ug/m^3)','PM2.5(ug/m^3)', 'PM10(ug/m^3)', 'O3(ppm)', 'NO2(ppm)', 'CO(ppm)', 'SO2(ppm)','WS(m/s)', 'WDI']
                newFileWriter = csv.DictWriter(newFile, fieldnames=headers)
                if newFile.tell() == 0:
                    newFileWriter.writeheader()  # file doesn't exist yet, write a header
            
                newFileWriter.writerow(
                    {  'TIME': Timestamp
                       ,'PM1(ug/m^3)' : str(pmdata[3])
                       ,'PM2.5(ug/m^3)' :str(pmdata[5])
                       ,'PM10(ug/m^3)' : str(pmdata[4])
                       ,'O3(ppm)' : format(getO3(), '.2f')
                       ,'NO2(ppm)': format(getNO2(), '.2f')
                       ,'CO(ppm)' : format(getCO(), '.2f')
                       ,'SO2(ppm)': format(getSO2(), '.2f')
                       ,'WS(m/s)' : format(getWindSpeed(), '.2f')
                       ,'WDI': format(getWindDirection(), '.2f')})
            isWrited = True


if __name__ == "__main__":
    main()
