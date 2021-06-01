dict_aqi = {
    'TIME': "hndhgnghn","pm25":str(34)
}
minute = '00'

  # ------Send DB----
sText = "aqi:"
for key, val in dict_aqi.items():
    print(key, "=>", val)
    if key == 'TIME':
        pass
    sText = sText + ":" + val
# print(sText)
sTest = sText.encode('utf-8')
print(sText)
# sendDB(sTest)
# ------Hourly-----
if minute == '00':
    sText = "hourly:"
    for key, val in dict_aqi.items():
        print(key, "=>", val)
        if key == 'TIME':
            pass
        sText = sText + ":" + val
    # print(sText)
    sTest = sText.encode('utf-8')
    print(sText)
    # sendDB(sTest)
