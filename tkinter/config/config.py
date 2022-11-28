from tkinter import *

sysPath = "/home/dty717/Desktop/github/vnc/tkinter"

# deviceSerName = '/dev/ttyUSB0'
deviceSerName = '/dev/ttyS0'

isUsingGPS = False
gpsSerName = '/dev/ttyS0'

srcIndex = 0
__unitIdentifier = 0x01

time_zone_shift = 8

lat_deg = 35.516268
lon_deg = 113.377695

imgDicts = {"greenSignal": None, "redSignal": None}

primaryColor = "#26a69a"
primaryLightColor = "#64d8cb"
primaryDarkColor = "#00766c"

wsHostname = "test.dty71719dfd.site"
url = 'wss://' + wsHostname + ":6503"
deviceID = "SmartDetect_FD_DL2022071300000001"
deviceType = "SmartDetect"
sampleType = "FiveParam"
uploadDataURL = 'http://server.delinapi.top:3000/SaveFiveParametersHistory'
uploadWarningURL = 'http://server.delinapi.top:3000/warning'

usingLocalTime = True

usingWaterDetect = True
