#!/usr/bin/python3

# ---------------------------------------------------------------------
from mcp3208 import MCP3208
import datetime
import smbus
import time
import board
import busio
import adafruit_bme280
import RPi.GPIO as GPIO
import csv

adc = MCP3208()
name_ch_mcp = ['O3', 'NO2', 'CO', 'SO2',
               'Wind Speed', 'Wind Direction', ' ', ' ']


def getO3():
    o3 = adc.read(0) / 4095.0 * 5.0
    str_o3 = '{:.2f}'.format(o3)
    aqi_o3 = 10 * (2.0 - float(str_o3))
    #aqi_o3 = float(str_o3)
    return aqi_o3


def getNO2():
    no2 = adc.read(1) / 4095.0 * 5.0
    str_no2 = '{:.4f}'.format(no2)
    aqi_no2 = 10 * (2.0 - float(str_no2))
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
    return w_speed % 360


def getWindDirection():
    w_di = (adc.read(5) / 4095.0) * 360.0
    return w_di


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
            # one click = 1.6363 mm. (Rainfall height)
            rain = count_minutelyRain*1.6363
            # or one click = 9 ml. = 9 cm^3
            count_minutelyRain = 0
            print(
                '\n'+'Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
            dict_aqi = {'Light(lx)': format(lightLevel, '.2f'), 'Temp.(C)': format(bme280.temperature, '.2f'), 'Humi.(%)': format(bme280.humidity, '.2f'), 'Pressure(hPa)': format(bme280.pressure, '.2f'), 'Altitude(meters)': format(
                bme280.altitude, '.2f'), 'rain(mm)': format(rain, '.2f'), 'O3': format(getO3(), '.2f'), 'NO2': format(getNO2(), '.2f'), 'CO': format(getCO(), '.2f'), 'SO2': format(getSO2(), '.2f'), 'WS': format(getWindSpeed(), '.2f'), 'WDI': format(getWindDirection(), '.2f')}

            for key, val in dict_aqi.items():
                print(key, "=>", val)

            filename = 'data/'+TimeRecord+'-aqi.csv'
            with open(filename, 'a') as newFile:
                headers = ['TIME', 'light(lx)', 'temperature(C)', 'humidity(%)', 'pressure(hPa)',
                           'rain(mm)', 'O3(ppm)', 'NO2(ppm)', 'CO(ppm)', 'SO2(ppm)', 'WS(m/s)', 'WDI']
                newFileWriter = csv.DictWriter(newFile, fieldnames=headers)
                if newFile.tell() == 0:
                    newFileWriter.writeheader()  # file doesn't exist yet, write a header

                newFileWriter.writerow(
                    {'TIME': Timestamp
                    , 'light(lx)': format(lightLevel, '.2f')
                    , 'temperature(C)': format(bme280.temperature, '.2f')
                    , 'humidity(%)': format(bme280.humidity, '.2f')
                    , 'pressure(hPa)': format(bme280.pressure, '.2f')
                    , 'rain(mm)': format(rain, '.2f')
                    , 'O3(ppm)' : format(getO3(), '.2f')
                    , 'NO2(ppm)': format(getNO2(), '.2f')
                    , 'CO(ppm)' : format(getCO(), '.2f')
                    , 'SO2(ppm)': format(getSO2(), '.2f')
                    , 'WS(m/s)' : format(getWindSpeed(), '.2f')
                    , 'WDI': format(getWindDirection(), '.2f')})

            print('-----------------------------------------------')
            isWrited = True
        if (GPIO.input(INPUT_PIN) == False):
            count_minutelyRain += 1
            # print(count_rain)
            time.sleep(0.1)


if __name__ == "__main__":
    main()
