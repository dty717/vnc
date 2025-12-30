import serial
import time
import threading
import datetime
from database.mongodb import insertLocation
from enum import Enum
from config.config import gpsSerName, lat_deg, lon_deg, time_zone_shift

saveGpsEvent = threading.Event()

gpsSer = serial.Serial(gpsSerName,timeout=0.2)

class GpsType(Enum):
    GPGSV = 0
    GNGLL = 1
    GNRMC = 2
    GNVTG = 3
    GNGGA = 4
    GNGSA = 5
    GPRMC = 6

class GpsData:
    def __init__(self):
        self.year = 0
        self.month = 0
        self.date = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.active = ''
        self.latitude = lat_deg
        self.latitudeFlag = ''
        self.longitude = lon_deg
        self.longitudeFlag = ''
        self.isOpen = False
        self.isOpening = False
        self.isClosing = False
    #
    def __str__(self):
        return "{}-{}-{} {}:{}:{} active:{} {} {},{} {}".format(self.year, self.month, self.date, self.hour, self.minute, self.second, self.active,
                                                                self.latitude, self.latitudeFlag, self.longitude, self.longitudeFlag)

gpsData = GpsData()

def openGPS():
    gpsSer.write(b"AT+QGPS=1\r\n")
    try:
        gpsRec= gpsSer.readall()
        if gpsRec.find(b'OK') != -1:
            return True
    except:
        return

def closeGPS():
    gpsSer.write(b"AT+QGPSEND\r\n")
    try:
        gpsRec= gpsSer.readall()
        if gpsRec.find(b'OK') != -1:
            return True
    except:
        return
def getGpsInfoUsingUSB():
    global gpsData
    active = gpsData.active
    gpsSer.write(b"AT+QGPSLOC?\r\n")
    try:
        gpsRec= gpsSer.readall()
        if gpsRec == b'':
            return
    except:
        return
    # Decode bytes to string and split into lines
    gpsText = gpsRec.decode()
    for line in gpsText.splitlines():
        if line.startswith("+QGPSLOC:"):
            # Remove prefix and split by comma
            fields = line.replace("+QGPSLOC: ", "").split(",")
            (
                utc_time, lat, lon, hdop, alt, fix, cog,
                spkm, spkn, date, nsat
            ) = fields
            gpsData.hour = int(utc_time[0:2]) + time_zone_shift
            gpsData.minute = int(utc_time[2:4])
            gpsData.second = int(utc_time[4:6])
            active = True
            gpsData.latitude = float(lat[0:len(lat)-1])
            gpsData.latitude = int(gpsData.latitude/100) + (gpsData.latitude % 100)/60
            gpsData.latitudeFlag = lat[len(lat)-1]
            gpsData.longitude = float(lon[0:len(lon)-1])
            gpsData.longitude = int(gpsData.longitude/100) + (gpsData.longitude % 100)/60
            gpsData.longitudeFlag = lon[len(lon)-1]
            gpsData.date = int(date[0:2])
            gpsData.month = int(date[2:4])
            gpsData.year = int(date[4:6]) + 2000
    gpsData.active = active

def getGpsInfo():
    global gpsData
    gpsType = None
    active = gpsData.active
    gpsString = gpsSer.readline()
    if gpsString != None and gpsString != "":
        if gpsString.find(b'$GNRMC') == 0:
            gpsType = GpsType.GNRMC
        elif gpsString.find(b'$GPRMC') == 0:
            gpsType = GpsType.GPRMC
        if gpsType != None:
            pointIndex = 7
            startIndex = 7
            strLen = len(gpsString)
            while pointIndex < strLen:
                pointIndex += 1
                if gpsString[pointIndex-1] == b','[0]:
                    if pointIndex > startIndex+5:
                        try:
                            gpsData.hour = int(gpsString[startIndex:startIndex+2]) + time_zone_shift
                            gpsData.minute = int(gpsString[startIndex+2:startIndex+4])
                            gpsData.second = int(gpsString[startIndex+4:startIndex+6])
                        except:
                            return
                        # print("time:{}:{}:{}\r\n".format(gpsData.hour,gpsData.minute,gpsData.second))
                    startIndex = pointIndex
                    break
            while pointIndex < strLen:
                pointIndex += 1
                if gpsString[pointIndex-1] == b','[0]:
                    if pointIndex > startIndex + 1:
                        active = gpsString[startIndex] == b'A'[0]
                        # print("active:{}\r\n".format(gpsData.active))
                    startIndex = pointIndex
                    break
            while pointIndex < strLen:
                pointIndex += 1
                if gpsString[pointIndex-1] == b','[0]:
                    if pointIndex > startIndex + 1:
                        try:
                            gpsData.latitude = float(gpsString[startIndex:pointIndex-1])
                            gpsData.latitude = int(gpsData.latitude/100) + (gpsData.latitude % 100)/60
                            # print("Latitude:{}\r\n".format(gpsData.latitude))
                        except:
                            return
                    startIndex = pointIndex
                    break
            while pointIndex < strLen:
                pointIndex += 1
                if gpsString[pointIndex-1] == b','[0]:
                    if pointIndex > startIndex + 1:
                        gpsData.latitudeFlag = chr(gpsString[startIndex])
                        # print("LatitudeFlag:{}\r\n".format(gpsData.latitudeFlag))
                    startIndex = pointIndex
                    break
            while pointIndex < strLen:
                pointIndex += 1
                if gpsString[pointIndex-1] == b','[0]:
                    if pointIndex > startIndex + 1:
                        try:
                            gpsData.longitude = float(gpsString[startIndex:pointIndex-1])
                            gpsData.longitude = int(gpsData.longitude/100) + (gpsData.longitude % 100)/60
                            # # print("Longitude:{}\r\n".format(gpsData.longitude))
                        except:
                            return
                    startIndex = pointIndex
                    break
            while pointIndex < strLen:
                pointIndex += 1
                if gpsString[pointIndex-1] == b','[0]:
                    if pointIndex > startIndex + 1:
                        gpsData.longitudeFlag = chr(gpsString[startIndex])
                        # print("longitudeFlag:{}\r\n".format(gpsData.longitudeFlag))
                    startIndex = pointIndex
                    break
            while pointIndex < strLen:
                pointIndex += 1
                if gpsString[pointIndex-1] == b','[0]:
                    if pointIndex > startIndex + 1:
                        pass
                    startIndex = pointIndex
                    break
            while pointIndex < strLen:
                pointIndex += 1
                if gpsString[pointIndex-1] == b','[0]:
                    if pointIndex > startIndex + 1:
                        pass
                    startIndex = pointIndex
                    break
            while pointIndex < strLen:
                pointIndex += 1
                if gpsString[pointIndex-1] == b','[0]:
                    if pointIndex > startIndex + 5:
                        try:
                            gpsData.date = int(gpsString[startIndex:startIndex+2])
                            gpsData.month = int(gpsString[startIndex+2:startIndex+4])
                            gpsData.year = int(gpsString[startIndex+4:startIndex+6]) + 2000
                        except:
                            return
                        # print("date:{}-{}-{}\r\n".format(gpsData.year,gpsData.month,gpsData.date))
                    startIndex = pointIndex
                    break
        gpsData.active = active

def saveLocation(year, month, date, hour, minute, second, latitude, longitude):
    if hour >= 24:
        insertLocation(datetime.datetime(year, month, date, hour % 24,
                       minute, second) + datetime.timedelta(days=1), latitude, longitude)
    else:
        insertLocation(datetime.datetime(year, month, date,
                       hour, minute, second), latitude, longitude)
