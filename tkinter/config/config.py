from tkinter import *

sysPath = "/home/dty717/Desktop/github/vnc/tkinter"

deviceSerName = '/dev/ttyUSB0'
# deviceSerName = '/dev/ttyS0'

isUsingGPS = True
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
deviceID = "SmartDetect_FD_DL2022071300000002"
deviceType = "SmartDetect"
sampleType = "FloatNineParam"
uploadDataURL = 'http://server.delinapi.top:3000/SaveFloatNineParametersHistory'
uploadWarningURL = 'http://server.delinapi.top:3000/warning'

addrsID = [0x99,0x41,0x81,0x20,0x88]

socketUploadIP = "155.138.195.23"
socketUploadPort = 2030

usingLocalTime = True

usingWaterDetect = True

dataScale = {
    "temp": 10,
    "PH": 100,
    "O2": 10,
    "COD": 10,
    "ele": 1,
    "tur": 1,
    "NH3": 100,
    "N": 100,
    "P": 100,
    "chl": 10,
}

dataShiftScale = {
    "temp": 1,
    "PH": 1,
    "O2": 1,
    "COD": 0.35,
    "ele": 0.23,
    "tur": 1,
    "NH3": 0.4,
    "NO3": 0.1,
    "P": 1,
    "chl": 1,
}

