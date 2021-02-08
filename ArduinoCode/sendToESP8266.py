import serial

sPortToUse = "/dev/ttyUSB0"
#sPortToUse = "/dev/ttyAMA0"

#'pm:pm2.5:pm10'
#sTest = "pm:12:20".encode('utf-8')

#'meteo:light:temp:humi:pressure:rain:O3:NO2:CO:SO2:WS:WDI'
sTest = "meteo:0:20:50:760:2:4:5:7:3:21:68".encode('utf-8')

iBytesSent = 0

serialPort = serial.Serial(sPortToUse, 115200)
serialPort.flushOutput()
serialPort.flushInput()

if serialPort.open:
    print("Opened port", sPortToUse)
    print(sTest)
    iBytesSent = serialPort.write(sTest)
    serialPort.write(b"\n")
    print ("Sent", iBytesSent, "bytes")

else:
    print("Port", sPortToUse, "failed to open")
serialPort.close()

