#!/usr/bin/python

# ---------------------------------------------------------------------
import datetime
import smbus
import time
import board
import busio
import adafruit_bme280
import RPi.GPIO as GPIO
import csv

GPIO.setmode(GPIO.BCM)           
INPUT_PIN = 6
GPIO.setup(INPUT_PIN, GPIO.IN) 
# ---------------------------------------------------------------------
# Define some constants from the datasheet
DEVICE = 0x23  # Default device I2C address
POWER_DOWN = 0x00  # No active state
POWER_ON = 0x01  # Power on
RESET = 0x07  # Reset data register value

# Start measurement at 4lx resolution. Time typically 16ms.
CONTINUOUS_LOW_RES_MODE = 0x13
# Start measurement at 1lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_1 = 0x10
# Start measurement at 0.5lx resolution. Time typically 120ms
CONTINUOUS_HIGH_RES_MODE_2 = 0x11
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_1 = 0x20
# Start measurement at 0.5lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_HIGH_RES_MODE_2 = 0x21
# Start measurement at 1lx resolution. Time typically 120ms
# Device is automatically set to Power Down after measurement.
ONE_TIME_LOW_RES_MODE = 0x23

bus = smbus.SMBus(1)  # Rev 2 Pi uses 1


def convertToNumber(data):
    # Simple function to convert 2 bytes of data
    # into a decimal number. Optional parameter 'decimals'
    # will round to specified number of decimal places.
    result = (data[1] + (256 * data[0])) / 1.2
    return (result)


def readLight(addr=DEVICE):
    # Read data from I2C interface
    light = bus.read_i2c_block_data(addr, ONE_TIME_HIGH_RES_MODE_1)
    return convertToNumber(light)
# ---------------------------------------------------------------------


# ---------------------------------------------------------------------
# Create library object using our Bus I2C port
i2c = busio.I2C(board.SCL, board.SDA)
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)

# change this to match the location's pressure (hPa) at sea level
bme280.sea_level_pressure = 1013.25

# ---------------------------------------------------------------------


def main():
    isWrited = False
    count_minutelyRain = 0
    #count_hourlyRain = 0
    #count_dailyRain = 0
    while True:
        #day = '{:%d}'.format(datetime.datetime.now())
        #hour = '{:%H}'.format(datetime.datetime.now())
        #minute = '{:%M}'.format(datetime.datetime.now())
        second = '{:%S}'.format(datetime.datetime.now())
        Timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        TimeRecord = '{:%Y-%m-%d}'.format(datetime.datetime.now())
        if second == '59':
            isWrited = False
        if second == '00' and not isWrited:
            lightLevel = readLight()
            rain = count_minutelyRain*1.6363 # one click = 1.6363 mm. (Rainfall height)
                                      # or one click = 9 ml. = 9 cm^3
            count_minutelyRain = 0
            print('\n'+'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            dict_aqi = { 'Light(lx)': format(lightLevel, '.2f')
                        ,'Temp.(C)': format(bme280.temperature, '.2f')
                        ,'Humi.(%)': format(bme280.humidity, '.2f')
                        ,'Pressure(hPa)': format(bme280.pressure, '.2f')
                        ,'Altitude(meters)': format(bme280.altitude, '.2f')
                        ,'rain(mm)' : format(rain, '.2f')}
            for key,val in dict_aqi.items():
                print( key, "=>", val)
            
            filename = 'data/'+TimeRecord+'-aqi_part1.csv'
            with open(filename, 'a') as newFile:
                headers = ['TIME', 'light(lx)','temperature(C)', 'humidity(%)', 'pressure(hPa)', 'rain(mm)' ]
                newFileWriter = csv.DictWriter(newFile, fieldnames=headers)
                if newFile.tell() == 0:
                    newFileWriter.writeheader()  # file doesn't exist yet, write a header
                
                newFileWriter.writerow(
                    {'TIME': Timestamp
                     ,'light(lx)' :format(lightLevel, '.2f')
                     ,'temperature(C)' : format(bme280.temperature, '.2f')
                     ,'humidity(%)' : format(bme280.humidity, '.2f')
                     ,'pressure(hPa)' : format(bme280.pressure, '.2f')
                     ,'rain(mm)' : format(rain, '.2f') })

            print('-----------------------------------------------')
            isWrited = True
        if (GPIO.input(INPUT_PIN) == False):
            count_minutelyRain += 1
            #print(count_rain)
            time.sleep(0.1)



if __name__ == "__main__":
    main()
