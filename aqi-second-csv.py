from mcp3208 import MCP3208
import time

adc = MCP3208()
name_ch_mcp = ['O3', 'NO2', 'CO', 'SO2',
               'Wind Speed', 'Wind Direction', ' ', ' ']
# while True:
#     '''
#     for i in range(8):
#         print('{}: ch[{}]: {:.2f}'.format(name_ch_mcp[i],i, adc.read(i)))
#     '''
#     o3 = adc.read(0) / 4095.0 *5.0
#     no2 = adc.read(1) / 4095.0 *5.0
#     co = adc.read(2) / 4095.0 *5.0
#     str_co = '{:.2f}'.format(co)
#     aqi_co = 200.0/(0.3) * (float(str_co) - 0.6)
#     so2 = adc.read(3) / 4095.0 *5.0

#     w_speed = adc.read(4) - 11
#     if w_speed < 0:
#          w_speed=0
#     w_di = ( adc.read(5) / 4095.0) * 360.0
#     print( '{}: {:.2f}'.format(name_ch_mcp[0], o3) +'\n' \
#     + '{}: {:.2f}'.format(name_ch_mcp[1], no2) +'\n' \
#     + '{}: {:.2f} ppm'.format(name_ch_mcp[2], aqi_co) +'\n' \
#     + '{}: {:.2f}'.format(name_ch_mcp[3], so2) +'\n' \
#     + '{}: {:.2f} '.format(name_ch_mcp[4], w_speed) +'\n' \
#     + '{}: {:.2f} from North'.format(name_ch_mcp[5], w_di) )
#     print('-----------------------------------------------')
#     time.sleep(0.1)


def getO3():
    o3 = adc.read(0) / 4095.0 * 5.0
    return o3


def getNO2():
    no2 = adc.read(1) / 4095.0 * 5.0
    return no2


def getCO():
    co = adc.read(2) / 4095.0 * 5.0
    str_co = '{:.2f}'.format(co)
    aqi_co = 200.0/(0.3) * (float(str_co) - 0.6)
    return aqi_co


def getSO2():
    so2 = adc.read(3) / 4095.0 * 5.0
    # str_co = '{:.2f}'.format(co)
    # aqi_co = 200.0/(0.3) * (float(str_co) - 0.6)
    return so2


def getWindSpeed():
    w_speed = adc.read(4) / 4095.0 * 5.0
    w_speed = adc.read(4) - 11
    if w_speed < 0:
        w_speed = 0
    return w_speed

def getWindDirection():
    w_di = ( adc.read(5) / 4095.0) * 360.0
    return w_di


def main():
    while True:
        print('{}: {:.2f}'.format(name_ch_mcp[0], getO3) + '\n'
              + '{}: {:.2f}'.format(name_ch_mcp[1], getNO2) + '\n'
              + '{}: {:.2f} ppm'.format(name_ch_mcp[2], getCO) + '\n'
              + '{}: {:.2f}'.format(name_ch_mcp[3], getSO2) + '\n'
              + '{}: {:.2f} m/s '.format(name_ch_mcp[4], getWindSpeed) + '\n'
              + '{}: {:.2f} from North'.format(name_ch_mcp[5], getWindDirection))
    print('-----------------------------------------------')
    time.sleep(0.1)


if __name__ == "__main__":
    main()
