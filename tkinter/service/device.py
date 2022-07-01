import serial
import time
import threading
import jsonpickle
import os
from tkinter import messagebox
from enum import Enum

from config.config import sysPath,deviceSerName ,__unitIdentifier
from tool.crc import checkLen,checkCrc,crc16
from service.logger import Logger

ser = serial.Serial(deviceSerName ,timeout=0.2) 
serialQueues = []
sendBusy = False
isSending = False
lastTime = time.time()
isBlocking = False
requestDeviceEvent = threading.Event()


class RequestData:
    def __init__(self, sendBuf,callBack, repeatTimes ,needMesBox):
        self.sendBuf = sendBuf
        self.repeatTimes = repeatTimes
        self.callBack = callBack
        self.needMesBox = needMesBox

def compare(arr1, arr2):
    if len(arr1) == len(arr2):
        for i in range(len(arr1)):
            if arr1[i] != arr2[i]:
                return False
        return True
    else:
        return False    

def sendReq(sendReqBuf, callBack, repeatTimes, needMesBox):
    global sendBusy,lastTime,isSending,serialQueues
    if (not isSending) and (len(serialQueues) == 0):
        serialQueues.append(RequestData(sendReqBuf, callBack,repeatTimes,needMesBox))
        send(sendReqBuf, callBack, repeatTimes, needMesBox)
    else:
        queuesCount = len(serialQueues)
        for i in range(queuesCount):
            if compare(serialQueues[i].sendBuf,sendReqBuf):
                return
        serialQueues.append(RequestData(sendReqBuf,callBack, repeatTimes,needMesBox));
        if len(serialQueues) > 5:
            serialQueues.clear()
            isSending = False

def send(sendReqBuf, callBack, repeatTimes, needMesBox):
    global sendBusy,lastTime,isSending,serialQueues
    if sendReqBuf[1] != 0x03:
        sendBusy = True
    lastTime = time.time()
    if not request(sendReqBuf,callBack, needMesBox):
        if repeatTimes > 0:
            send(s, callBack, repeatTimes - 1, needMesBox)
            return
        else:
            serialQueues.remove(serialQueues[0])
    else:
        serialQueues.remove(serialQueues[0])
    isSending = False
    if len(serialQueues)>0:
        requestData = serialQueues[0]
        send(requestData.sendBuf, requestData.callBack, requestData.repeatTimes,requestData.needMesBox)

def request(sendReqBuf,callBack ,needMesBox):
    global isSending,isBlocking,lastTime
    isSending = True
    if not ser.is_open:
        if isBlocking:
            return True
        else:
            isBlocking = True
        if needMesBox:
            messagebox.showerror("通讯异常", _serialPort.PortName + "端口被占用或者未开启")
        try:
            ser.open()
        except:
            pass
        isBlocking = False
        return
    _now = time.time()
    try:
        if _now - lastTime<1:
            requestDeviceEvent.wait(lastTime+1-_now)
        lastTime = time.time()
        ser.flush()
        ser.write(sendReqBuf)
    except:
        isSending = False
        return False
    recBytes = None
    try:
        recBytes = ser.read(1024)
    except:
        return False
    isSending = False
    return checkRecv(sendReqBuf,recBytes,callBack, needMesBox)

def checkRecv(sendReqBuf,recBytes,callBack, needMesBox):
    if sendReqBuf[1] ==0x03:
        if len(recBytes)==0:
            Logger.log("通讯异常", "设备问询无回复", "", 1200)
            return False
        if sendReqBuf[0]!=recBytes[0]:
            Logger.log("通讯异常", "设备问询回复地址错误", "", 1200)
            return False
        if not checkCrc(recBytes):
            Logger.log("通讯异常", "设备问询回复校验错误", "", 1200)
            return False
        if not checkLen(recBytes,(sendReqBuf[4]<<8)|sendReqBuf[5]):
            Logger.log("通讯异常", "设备问询回复长度错误", "", 1200)
            return False
        try:
            callBack(recBytes)
        except Exception as e:
            Logger.log("通讯异常", "设备问询解析异常", str(e).split('\n')[0].strip(), 1200)
        return True
    if len(recBytes)==0:
        if needMesBox:
            messagebox.showerror("通讯异常", "设备未反应")
        Logger.log("通讯异常", "设备设置无回复", str(sendReqBuf[0]) + " " + str(sendReqBuf[1]) + " " + str(sendReqBuf[2]) + " " + str(sendReqBuf[3]) + " "+ str(sendReqBuf[4]) + " " + str(sendReqBuf[5]) + " ", 1200)
        return False
    if sendReqBuf[0]!=recBytes[0]:
        if needMesBox:
            messagebox.showerror("通讯异常", "通讯繁忙,稍后再试")
        Logger.log("通讯异常", "设备设置回复地址错误", "", 1200)
        return False
    if not checkCrc(recBytes):
        if needMesBox:
            messagebox.showerror("通讯异常", "通讯繁忙,稍后再试")
        Logger.log("通讯异常", "设备设置回复校验错误", "", 1200)
        return False
    equal = True
    if sendReqBuf[1] == 0x06 or sendReqBuf[1] == 0x05:
        if len(recBytes) != 8:
            if (needMesBox):
                messagebox.showerror("通讯异常", "通讯繁忙,稍后再试")
            Logger.log("通讯异常", "设备设置回复长度错误", "", 1200);
            return False    
        for i in range(8):
            if recBytes[i] != sendReqBuf[i]:
                equal = False
                break
        if equal:
            if needMesBox:
                messagebox.showinfo("设置", "设置成功")
            if callBack != None:
                callBack(recBytes)
            if (sendReqBuf[1] == 6 or (sendReqBuf[1] == 5 and (sendReqBuf[3] <= 0x58 and sendReqBuf[3] >= 0x35))):
                saveSetting()
        else:
            if needMesBox:
                messagebox.showerror("通讯异常", "设备未反应")
            Logger.log("通讯异常", "设备设置回复错误", "", 1200)
    elif sendReqBuf[1] == 0x10:
        if callBack != None:
            callBack(recBytes)
    return equal

lastSaveSetting = time.time()

def saveSetting():
    global lastSaveSetting
    _now = time.time()
    if _now - lastSaveSetting < 10:
        return
    lastSaveSetting = _now
    f_deviceController = open(f"{sysPath}/deviceController.json", "w")
    f_deviceController.write(jsonpickle.encode(deviceController))
    f_deviceController.close()
    f_deviceInfo = open(f"{sysPath}/deviceInfo.json", "w")
    f_deviceInfo.write(jsonpickle.encode(deviceInfo))
    f_deviceInfo.close()
    return

def write_single_coil(starting_address, value, callBack, repeatTimes, needMesBox):
    function_code = 6
    starting_address_lsb = (starting_address & 0xFF)
    starting_address_msb = ((starting_address & 0xFF00) >> 8)
    if value:
        valueLSB = 0
        valueMSB = (0xFF00 >> 8)
    else:
        valueLSB = 0
        valueMSB = (0 >> 8)
    data = [__unitIdentifier, function_code, starting_address_msb, starting_address_lsb, valueMSB, valueLSB]
    crcCheck = crc16(data,0,len(data))
    data.append(crcCheck>>8)
    data.append(crcCheck&0xff)
    sendReq(data, callBack, repeatTimes, needMesBox)

def write_single_register(starting_address, value, callBack, repeatTimes, needMesBox):
    function_code = 6
    starting_address_lsb = (starting_address & 0xFF)
    starting_address_msb = ((starting_address & 0xFF00) >> 8)
    valueLSB = (value & 0xFF)
    valueMSB = ((value & 0xFF00) >> 8)
    data = [__unitIdentifier, function_code, starting_address_msb, starting_address_lsb, valueMSB, valueLSB]
    crcCheck = crc16(data,0,len(data))
    data.append(crcCheck>>8)
    data.append(crcCheck&0xff)
    sendReq(data, callBack, repeatTimes, needMesBox)


def write_multiple_registers(starting_address, values, callBack, repeatTimes, needMesBox):
    function_code = 16
    starting_address_lsb = (starting_address & 0xFF)
    starting_address_msb = ((starting_address & 0xFF00) >> 8)
    # valueLSB = (value & 0xFF)
    # valueMSB = ((value & 0xFF00) >> 8)
    quantityLSB = len(values) & 0xFF
    quantityMSB = (len(values) & 0xFF00) >> 8
    data = [__unitIdentifier, function_code, starting_address_msb, starting_address_lsb, quantityMSB, quantityLSB]
    data.append(len(values) * 2)
    for value in values:
        data.append((value & 0xFF00) >> 8)
        data.append(value & 0xFF)
    crcCheck = crc16(data,0,len(data))
    data.append(crcCheck>>8)
    data.append(crcCheck&0xff)
    sendReq(data, callBack, repeatTimes, needMesBox)

class DeviceAddr(Enum):
    # DeviceController Addr
    modelSelectAddr = 0x00
    operationSelectAddr = 0x01
    selectingHoursAddr = 0x02
    calibrateDayAddr = 0x1a
    calibrateHourAddr = 0x1b
    calibrateMinuteAddr = 0x1c
    immediateCalibrateAddr = 0x1d
    concentration1SettingValueAddr = 0x1e
    concentration2SettingValueAddr = 0x20
    concentration3SettingValueAddr = 0x22
    samplePumpAddr = 0x24
    concentration1PumpAddr = 0x25
    concentration2PumpAddr = 0x26
    concentration3PumpAddr = 0x27
    chemical1PumpAddr = 0x28
    chemical2PumpAddr = 0x29
    chemical3PumpAddr = 0x2a
    reactionTubeCleanAddr = 0x2b
    suctionCleanAddr = 0x2c
    measurementIntervalAddr = 0x2d
    # DeviceInfo Addr
    concentration1ValueAddr = 0x81
    concentration1MaxValueAddr = 0x82
    concentration1AValueAddr = 0x83
    concentration1CValueAddr = 0x85
    concentration2ValueAddr = 0x87
    concentration2MaxValueAddr = 0x88
    concentration2AValueAddr = 0x89
    concentration2CValueAddr = 0x8b
    concentration3ValueAddr = 0x8d
    concentration3MaxValueAddr = 0x8e
    concentration3AValueAddr = 0x8f
    concentration3CValueAddr = 0x91    
    sampleValueAddr = 0x93
    sampleMaxValueAddr = 0x94
    sampleAValueAddr = 0x95
    sampleCValueAddr = 0x97
    measureYearAddr = 0x99
    measureMonthAddr = 0x9a
    measureDayAddr = 0x9b
    measureHourAddr = 0x9c
    measureMinuteAddr = 0x9d
    measureSecondAddr = 0x9e
    warningInfoAddr = 0x9f

class DeviceController:
    def __init__(self):
        self.init = False
        self.modelSelect = 0
        self.operationSelect = 0
        self.selectingHours = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.calibrateDay = 0
        self.calibrateHour = 0
        self.calibrateMinute = 0
        self.immediateCalibrate = 0
        self.concentration1SettingValue = 0
        self.concentration2SettingValue = 0
        self.concentration3SettingValue = 0
        self.samplePump = 0
        self.concentration1Pump = 0
        self.concentration2Pump = 0
        self.concentration3Pump = 0
        self.chemical1Pump = 0
        self.chemical2Pump = 0
        self.chemical3Pump = 0
        self.reactionTubeClean = 0
        self.suctionClean = 0
        self.measurementInterval = 0
    # 
    def __str__(self):
        return """init = {}
modelSelect = {}
operationSelect = {}
selectingHours = {}
calibrateDay = {}
calibrateHour = {}
calibrateMinute = {}
immediateCalibrate = {}
concentration1SettingValue = {}
concentration2SettingValue = {}
concentration3SettingValue = {}
samplePump = {}
concentration1Pump = {}
concentration2Pump = {}
concentration3Pump = {}
chemical1Pump = {}
chemical2Pump = {}
chemical3Pump = {}
reactionTubeClean = {}
suctionClean = {}
measurementInterval = {}""".format(self.init,self.modelSelect,self.operationSelect,self.selectingHours,self.calibrateDay,self.calibrateHour,self.calibrateMinute,
            self.immediateCalibrate,self.concentration1SettingValue,self.concentration2SettingValue,
            self.concentration3SettingValue,self.samplePump,self.concentration1Pump,self.concentration2Pump,
            self.concentration3Pump,self.chemical1Pump,self.chemical2Pump,self.chemical3Pump,self.reactionTubeClean,
            self.suctionClean,self.measurementInterval)

class DeviceInfo:
    def __init__(self):
        self.init = False
        self.concentration1Value = 0
        self.concentration1MaxValue = 0
        self.concentration1AValue = 0
        self.concentration1CValue = 0
        self.concentration2Value = 0
        self.concentration2MaxValue = 0
        self.concentration2AValue = 0
        self.concentration2CValue = 0
        self.concentration3Value = 0
        self.concentration3MaxValue = 0
        self.concentration3AValue = 0
        self.concentration3CValue = 0    
        self.sampleValue = 0
        self.sampleMaxValue = 0
        self.sampleAValue = 0
        self.sampleCValue = 0
        self.measureYear = 0
        self.measureMonth = 0
        self.measureDay = 0
        self.measureHour = 0
        self.measureMinute = 0
        self.measureSecond = 0
        self.warningInfo = 0
    #
    def __str__(self):
        return """init = {}
concentration1Value = {}
concentration1MaxValue = {}
concentration1AValue = {}
concentration1CValue = {}
concentration2Value = {}
concentration2MaxValue = {}
concentration2AValue = {}
concentration2CValue = {}
concentration3Value = {}
concentration3MaxValue = {}
concentration3AValue = {}
concentration3CValue = {}
sampleValue = {}
sampleMaxValue = {}
sampleAValue = {}
sampleCValue = {}
measureYear = {}
measureMonth = {}
measureDay = {}
measureHour = {}
measureMinute = {}
measureSecond = {}
warningInfo = {}""".format(self.init,self.concentration1Value,self.concentration1MaxValue,self.concentration1AValue,
    self.concentration1CValue,self.concentration2Value,self.concentration2MaxValue,self.concentration2AValue,self.concentration2CValue,
    self.concentration3Value,self.concentration3MaxValue,self.concentration3AValue,self.concentration3CValue,self.sampleValue,
    self.sampleMaxValue,self.sampleAValue,self.sampleCValue,self.measureYear,self.measureMonth,self.measureDay,self.measureHour,
    self.measureMinute,self.measureSecond,self.warningInfo)

shiftAddr = 3

def getBytesControllingInfo(buffer,deviceController):
    if not deviceController.init:
        deviceController.init = True
        deviceController.modelSelect = (buffer[shiftAddr + 2 * DeviceAddr.modelSelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.modelSelectAddr.value + 1]
        deviceController.operationSelect = (buffer[shiftAddr + 2 * DeviceAddr.operationSelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.operationSelectAddr.value + 1]
        for i in range(24):
            deviceController.selectingHours[i] = (buffer[shiftAddr + 2 * (DeviceAddr.selectingHoursAddr.value+i)] <<8) | buffer[shiftAddr + 2 * (DeviceAddr.selectingHoursAddr.value+i) + 1]
        deviceController.calibrateDay = (buffer[shiftAddr + 2 * DeviceAddr.calibrateDayAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.calibrateDayAddr.value + 1]
        deviceController.calibrateHour = (buffer[shiftAddr + 2 * DeviceAddr.calibrateHourAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.calibrateHourAddr.value + 1]
        deviceController.calibrateMinute = (buffer[shiftAddr + 2 * DeviceAddr.calibrateMinuteAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.calibrateMinuteAddr.value + 1]
        deviceController.immediateCalibrate = (buffer[shiftAddr + 2 * DeviceAddr.immediateCalibrateAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.immediateCalibrateAddr.value + 1]
        deviceController.concentration1SettingValue = (buffer[shiftAddr + 2 * DeviceAddr.concentration1SettingValueAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration1SettingValueAddr.value + 1]
        deviceController.concentration2SettingValue = (buffer[shiftAddr + 2 * DeviceAddr.concentration2SettingValueAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration2SettingValueAddr.value + 1]
        deviceController.concentration3SettingValue = (buffer[shiftAddr + 2 * DeviceAddr.concentration3SettingValueAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration3SettingValueAddr.value + 1]
        deviceController.samplePump = (buffer[shiftAddr + 2 * DeviceAddr.samplePumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.samplePumpAddr.value + 1]
        deviceController.concentration1Pump = (buffer[shiftAddr + 2 * DeviceAddr.concentration1PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration1PumpAddr.value + 1]
        deviceController.concentration2Pump = (buffer[shiftAddr + 2 * DeviceAddr.concentration2PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration2PumpAddr.value + 1]
        deviceController.concentration3Pump = (buffer[shiftAddr + 2 * DeviceAddr.concentration3PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration3PumpAddr.value + 1]
        deviceController.chemical1Pump = (buffer[shiftAddr + 2 * DeviceAddr.chemical1PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical1PumpAddr.value + 1]
        deviceController.chemical2Pump = (buffer[shiftAddr + 2 * DeviceAddr.chemical2PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical2PumpAddr.value + 1]
        deviceController.chemical3Pump = (buffer[shiftAddr + 2 * DeviceAddr.chemical3PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical3PumpAddr.value + 1]
        deviceController.reactionTubeClean = (buffer[shiftAddr + 2 * DeviceAddr.reactionTubeCleanAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.reactionTubeCleanAddr.value + 1]
        deviceController.suctionClean = (buffer[shiftAddr + 2 * DeviceAddr.suctionCleanAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.suctionCleanAddr.value + 1]
        deviceController.measurementInterval = (buffer[shiftAddr + 2 * DeviceAddr.measurementIntervalAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.measurementIntervalAddr.value + 1]
    else:
        _modelSelect = (buffer[shiftAddr + 2 * DeviceAddr.modelSelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.modelSelectAddr.value + 1]
        if _modelSelect != deviceController.modelSelect:
            deviceController.modelSelect = _modelSelect
        _operationSelect = (buffer[shiftAddr + 2 * DeviceAddr.operationSelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.operationSelectAddr.value + 1]
        if _operationSelect != deviceController.operationSelect:
            deviceController.operationSelect = _operationSelect
        for i in range(24):
            _selectingHours = (buffer[shiftAddr + 2 * (DeviceAddr.selectingHoursAddr.value+i)] <<8) | buffer[shiftAddr + 2 * (DeviceAddr.selectingHoursAddr.value+i) + 1]
            if _selectingHours != deviceController.selectingHours[i]:
                deviceController.selectingHours[i] = _selectingHours
        _calibrateDay = (buffer[shiftAddr + 2 * DeviceAddr.calibrateDayAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.calibrateDayAddr.value + 1]
        if _calibrateDay != deviceController.calibrateDay:
            deviceController.calibrateDay = _calibrateDay
        _calibrateHour = (buffer[shiftAddr + 2 * DeviceAddr.calibrateHourAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.calibrateHourAddr.value + 1]
        if _calibrateHour != deviceController.calibrateHour:
            deviceController.calibrateHour = _calibrateHour
        _calibrateMinute = (buffer[shiftAddr + 2 * DeviceAddr.calibrateMinuteAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.calibrateMinuteAddr.value + 1]
        if _calibrateMinute != deviceController.calibrateMinute:
            deviceController.calibrateMinute = _calibrateMinute
        _immediateCalibrate = (buffer[shiftAddr + 2 * DeviceAddr.immediateCalibrateAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.immediateCalibrateAddr.value + 1]
        if _immediateCalibrate != deviceController.immediateCalibrate:
            deviceController.immediateCalibrate = _immediateCalibrate
        _concentration1SettingValue = (buffer[shiftAddr + 2 * DeviceAddr.concentration1SettingValueAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration1SettingValueAddr.value + 1]
        if _concentration1SettingValue != deviceController.concentration1SettingValue:
            deviceController.concentration1SettingValue = _concentration1SettingValue
        _concentration2SettingValue = (buffer[shiftAddr + 2 * DeviceAddr.concentration2SettingValueAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration2SettingValueAddr.value + 1]
        if _concentration2SettingValue != deviceController.concentration2SettingValue:
            deviceController.concentration2SettingValue = _concentration2SettingValue
        _concentration3SettingValue = (buffer[shiftAddr + 2 * DeviceAddr.concentration3SettingValueAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration3SettingValueAddr.value + 1]
        if _concentration3SettingValue != deviceController.concentration3SettingValue:
            deviceController.concentration3SettingValue = _concentration3SettingValue
        _samplePump = (buffer[shiftAddr + 2 * DeviceAddr.samplePumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.samplePumpAddr.value + 1]
        if _samplePump != deviceController.samplePump:
            deviceController.samplePump = _samplePump
        _concentration1Pump = (buffer[shiftAddr + 2 * DeviceAddr.concentration1PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration1PumpAddr.value + 1]
        if _concentration1Pump != deviceController.concentration1Pump:
            deviceController.concentration1Pump = _concentration1Pump
        _concentration2Pump = (buffer[shiftAddr + 2 * DeviceAddr.concentration2PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration2PumpAddr.value + 1]
        if _concentration2Pump != deviceController.concentration2Pump:
            deviceController.concentration2Pump = _concentration2Pump
        _concentration3Pump = (buffer[shiftAddr + 2 * DeviceAddr.concentration3PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration3PumpAddr.value + 1]
        if _concentration3Pump != deviceController.concentration3Pump:
            deviceController.concentration3Pump = _concentration3Pump
        _chemical1Pump = (buffer[shiftAddr + 2 * DeviceAddr.chemical1PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical1PumpAddr.value + 1]
        if _chemical1Pump != deviceController.chemical1Pump:
            deviceController.chemical1Pump = _chemical1Pump
        _chemical2Pump = (buffer[shiftAddr + 2 * DeviceAddr.chemical2PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical2PumpAddr.value + 1]
        if _chemical2Pump != deviceController.chemical2Pump:
            deviceController.chemical2Pump = _chemical2Pump
        _chemical3Pump = (buffer[shiftAddr + 2 * DeviceAddr.chemical3PumpAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical3PumpAddr.value + 1]
        if _chemical3Pump != deviceController.chemical3Pump:
            deviceController.chemical3Pump = _chemical3Pump
        _reactionTubeClean = (buffer[shiftAddr + 2 * DeviceAddr.reactionTubeCleanAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.reactionTubeCleanAddr.value + 1]
        if _reactionTubeClean != deviceController.reactionTubeClean:
            deviceController.reactionTubeClean = _reactionTubeClean
        _suctionClean = (buffer[shiftAddr + 2 * DeviceAddr.suctionCleanAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.suctionCleanAddr.value + 1]
        if _suctionClean != deviceController.suctionClean:
            deviceController.suctionClean = _suctionClean
        _measurementInterval = (buffer[shiftAddr + 2 * DeviceAddr.measurementIntervalAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.measurementIntervalAddr.value + 1]
        if _measurementInterval != deviceController.measurementInterval:
            deviceController.measurementInterval = _measurementInterval
        # print(deviceController)
    pass

shiftAddr2 = 3 - 2 * DeviceAddr.concentration1ValueAddr.value
def getBytesInfo(buffer,deviceInfo):
    if not deviceInfo.init:
        deviceInfo.init = True
        deviceInfo.concentration1Value = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration1ValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration1ValueAddr.value + 1]
        deviceInfo.concentration1MaxValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration1MaxValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration1MaxValueAddr.value + 1]
        deviceInfo.concentration1AValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration1AValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration1AValueAddr.value + 1]
        deviceInfo.concentration1CValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration1CValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration1CValueAddr.value + 1]
        deviceInfo.concentration2Value = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration2ValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration2ValueAddr.value + 1]
        deviceInfo.concentration2MaxValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration2MaxValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration2MaxValueAddr.value + 1]
        deviceInfo.concentration2AValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration2AValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration2AValueAddr.value + 1]
        deviceInfo.concentration2CValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration2CValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration2CValueAddr.value + 1]
        deviceInfo.concentration3Value = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration3ValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration3ValueAddr.value + 1]
        deviceInfo.concentration3MaxValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration3MaxValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration3MaxValueAddr.value + 1]
        deviceInfo.concentration3AValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration3AValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration3AValueAddr.value + 1]
        deviceInfo.concentration3CValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration3CValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration3CValueAddr.value + 1]    
        deviceInfo.sampleValue = (buffer[shiftAddr2 + 2 * DeviceAddr.sampleValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.sampleValueAddr.value + 1]
        deviceInfo.sampleMaxValue = (buffer[shiftAddr2 + 2 * DeviceAddr.sampleMaxValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.sampleMaxValueAddr.value + 1]
        deviceInfo.sampleAValue = (buffer[shiftAddr2 + 2 * DeviceAddr.sampleAValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.sampleAValueAddr.value + 1]
        deviceInfo.sampleCValue = (buffer[shiftAddr2 + 2 * DeviceAddr.sampleCValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.sampleCValueAddr.value + 1]
        deviceInfo.measureYear = (buffer[shiftAddr2 + 2 * DeviceAddr.measureYearAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureYearAddr.value + 1]
        deviceInfo.measureMonth = (buffer[shiftAddr2 + 2 * DeviceAddr.measureMonthAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureMonthAddr.value + 1]
        deviceInfo.measureDay = (buffer[shiftAddr2 + 2 * DeviceAddr.measureDayAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureDayAddr.value + 1]
        deviceInfo.measureHour = (buffer[shiftAddr2 + 2 * DeviceAddr.measureHourAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureHourAddr.value + 1]
        deviceInfo.measureMinute = (buffer[shiftAddr2 + 2 * DeviceAddr.measureMinuteAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureMinuteAddr.value + 1]
        deviceInfo.measureSecond = (buffer[shiftAddr2 + 2 * DeviceAddr.measureSecondAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureSecondAddr.value + 1]
        deviceInfo.warningInfo = (buffer[shiftAddr2 + 2 * DeviceAddr.warningInfoAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.warningInfoAddr.value + 1]
    else:
        _concentration1Value = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration1ValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration1ValueAddr.value + 1]
        if _concentration1Value != deviceInfo.concentration1Value:
            deviceInfo.concentration1Value = _concentration1Value
        _concentration1MaxValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration1MaxValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration1MaxValueAddr.value + 1]
        if _concentration1MaxValue != deviceInfo.concentration1MaxValue:
            deviceInfo.concentration1MaxValue = _concentration1MaxValue
        _concentration1AValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration1AValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration1AValueAddr.value + 1]
        if _concentration1AValue != deviceInfo.concentration1AValue:
            deviceInfo.concentration1AValue = _concentration1AValue
        _concentration1CValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration1CValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration1CValueAddr.value + 1]
        if _concentration1CValue != deviceInfo.concentration1CValue:
            deviceInfo.concentration1CValue = _concentration1CValue
        _concentration2Value = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration2ValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration2ValueAddr.value + 1]
        if _concentration2Value != deviceInfo.concentration2Value:
            deviceInfo.concentration2Value = _concentration2Value
        _concentration2MaxValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration2MaxValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration2MaxValueAddr.value + 1]
        if _concentration2MaxValue != deviceInfo.concentration2MaxValue:
            deviceInfo.concentration2MaxValue = _concentration2MaxValue
        _concentration2AValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration2AValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration2AValueAddr.value + 1]
        if _concentration2AValue != deviceInfo.concentration2AValue:
            deviceInfo.concentration2AValue = _concentration2AValue
        _concentration2CValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration2CValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration2CValueAddr.value + 1]
        if _concentration2CValue != deviceInfo.concentration2CValue:
            deviceInfo.concentration2CValue = _concentration2CValue
        _concentration3Value = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration3ValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration3ValueAddr.value + 1]
        if _concentration3Value != deviceInfo.concentration3Value:
            deviceInfo.concentration3Value = _concentration3Value
        _concentration3MaxValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration3MaxValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration3MaxValueAddr.value + 1]
        if _concentration3MaxValue != deviceInfo.concentration3MaxValue:
            deviceInfo.concentration3MaxValue = _concentration3MaxValue
        _concentration3AValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration3AValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration3AValueAddr.value + 1]
        if _concentration3AValue != deviceInfo.concentration3AValue:
            deviceInfo.concentration3AValue = _concentration3AValue
        _concentration3CValue = (buffer[shiftAddr2 + 2 * DeviceAddr.concentration3CValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.concentration3CValueAddr.value + 1]
        if _concentration3CValue != deviceInfo.concentration3CValue:
            deviceInfo.concentration3CValue = _concentration3CValue    
        _sampleValue = (buffer[shiftAddr2 + 2 * DeviceAddr.sampleValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.sampleValueAddr.value + 1]
        if _sampleValue != deviceInfo.sampleValue:
            deviceInfo.sampleValue = _sampleValue
        _sampleMaxValue = (buffer[shiftAddr2 + 2 * DeviceAddr.sampleMaxValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.sampleMaxValueAddr.value + 1]
        if _sampleMaxValue != deviceInfo.sampleMaxValue:
            deviceInfo.sampleMaxValue = _sampleMaxValue
        _sampleAValue = (buffer[shiftAddr2 + 2 * DeviceAddr.sampleAValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.sampleAValueAddr.value + 1]
        if _sampleAValue != deviceInfo.sampleAValue:
            deviceInfo.sampleAValue = _sampleAValue
        _sampleCValue = (buffer[shiftAddr2 + 2 * DeviceAddr.sampleCValueAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.sampleCValueAddr.value + 1]
        if _sampleCValue != deviceInfo.sampleCValue:
            deviceInfo.sampleCValue = _sampleCValue
        _measureYear = (buffer[shiftAddr2 + 2 * DeviceAddr.measureYearAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureYearAddr.value + 1]
        if _measureYear != deviceInfo.measureYear:
            deviceInfo.measureYear = _measureYear
        _measureMonth = (buffer[shiftAddr2 + 2 * DeviceAddr.measureMonthAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureMonthAddr.value + 1]
        if _measureMonth != deviceInfo.measureMonth:
            deviceInfo.measureMonth = _measureMonth
        _measureDay = (buffer[shiftAddr2 + 2 * DeviceAddr.measureDayAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureDayAddr.value + 1]
        if _measureDay != deviceInfo.measureDay:
            deviceInfo.measureDay = _measureDay
        _measureHour = (buffer[shiftAddr2 + 2 * DeviceAddr.measureHourAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureHourAddr.value + 1]
        if _measureHour != deviceInfo.measureHour:
            deviceInfo.measureHour = _measureHour
        _measureMinute = (buffer[shiftAddr2 + 2 * DeviceAddr.measureMinuteAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureMinuteAddr.value + 1]
        if _measureMinute != deviceInfo.measureMinute:
            deviceInfo.measureMinute = _measureMinute
        _measureSecond = (buffer[shiftAddr2 + 2 * DeviceAddr.measureSecondAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.measureSecondAddr.value + 1]
        if _measureSecond != deviceInfo.measureSecond:
            deviceInfo.measureSecond = _measureSecond
        _warningInfo = (buffer[shiftAddr2 + 2 * DeviceAddr.warningInfoAddr.value] <<8) | buffer[shiftAddr2 + 2 * DeviceAddr.warningInfoAddr.value + 1]
        if _warningInfo != deviceInfo.warningInfo:
            deviceInfo.warningInfo = _warningInfo
        # print(deviceInfo)
    pass


if os.path.exists(f"{sysPath}/deviceController.json"):
    f_deviceController = open(f"{sysPath}/deviceController.json", "r")
    deviceController = jsonpickle.decode(f_deviceController.read())
else:
    deviceController = DeviceController()

if os.path.exists(f"{sysPath}/deviceInfo.json"):
    f_deviceInfo = open(f"{sysPath}/deviceInfo.json", "r")
    deviceInfo = jsonpickle.decode(f_deviceInfo.read())
    deviceInfo.init = False
else:
    deviceInfo = DeviceInfo()


# deviceController = DeviceController()
# deviceInfo = DeviceInfo()