from enum import Enum
class DeviceAddr(Enum):
    # DeviceController Addr
    modelSelectAddr = 0x00
    operationSelectAddr = 0x01
    selectingHoursAddr = 0x02
    daySelectAddr = 0x1a
    hourSelectAddr = 0x1b
    minuteSelectAddr = 0x1c
    immediateCalibrateAddr = 0x1d
    concentration1SettingValueAddr = 0x1e
    concentration2SettingValueAddr = 0x20
    concentration3SettingValueAddr = 0x22
    waterAddAddr = 0x24
    concentration1AddAddr = 0x25
    concentration2AddAddr = 0x26
    concentration3AddAddr = 0x27
    chemical1AddAddr = 0x28
    chemical2AddAddr = 0x29
    chemical3AddAddr = 0x2a
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
    init = False
    modelSelect = 0
    operationSelect = 0
    selectingHours = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    daySelect = 0
    hourSelect = 0
    minuteSelect = 0
    immediateCalibrate = 0
    concentration1SettingValue = 0
    concentration2SettingValue = 0
    concentration3SettingValue = 0
    waterAdd = 0
    concentration1Add = 0
    concentration2Add = 0
    concentration3Add = 0
    chemical1Add = 0
    chemical2Add = 0
    chemical3Add = 0
    reactionTubeClean = 0
    suctionClean = 0
    measurementInterval = 0
    # 
    def __str__(self):
        return """init = {}
modelSelect = {}
operationSelect = {}
selectingHours = {}
daySelect = {}
hourSelect = {}
minuteSelect = {}
immediateCalibrate = {}
concentration1SettingValue = {}
concentration2SettingValue = {}
concentration3SettingValue = {}
waterAdd = {}
concentration1Add = {}
concentration2Add = {}
concentration3Add = {}
chemical1Add = {}
chemical2Add = {}
chemical3Add = {}
reactionTubeClean = {}
suctionClean = {}
measurementInterval = {}""".format(self.init,self.modelSelect,self.operationSelect,self.selectingHours,self.daySelect,self.hourSelect,self.minuteSelect,
            self.immediateCalibrate,self.concentration1SettingValue,self.concentration2SettingValue,
            self.concentration3SettingValue,self.waterAdd,self.concentration1Add,self.concentration2Add,
            self.concentration3Add,self.chemical1Add,self.chemical2Add,self.chemical3Add,self.reactionTubeClean,
            self.suctionClean,self.measurementInterval)


class DeviceInfo:
    init = False
    concentration1Value = 0
    concentration1MaxValue = 0
    concentration1AValue = 0
    concentration1CValue = 0
    concentration2Value = 0
    concentration2MaxValue = 0
    concentration2AValue = 0
    concentration2CValue = 0
    concentration3Value = 0
    concentration3MaxValue = 0
    concentration3AValue = 0
    concentration3CValue = 0    
    sampleValue = 0
    sampleMaxValue = 0
    sampleAValue = 0
    sampleCValue = 0
    measureYear = 0
    measureMonth = 0
    measureDay = 0
    measureHour = 0
    measureMinute = 0
    measureSecond = 0
    warningInfo = 0
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
        deviceController.daySelect = (buffer[shiftAddr + 2 * DeviceAddr.daySelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.daySelectAddr.value + 1]
        deviceController.hourSelect = (buffer[shiftAddr + 2 * DeviceAddr.hourSelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.hourSelectAddr.value + 1]
        deviceController.minuteSelect = (buffer[shiftAddr + 2 * DeviceAddr.minuteSelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.minuteSelectAddr.value + 1]
        deviceController.immediateCalibrate = (buffer[shiftAddr + 2 * DeviceAddr.immediateCalibrateAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.immediateCalibrateAddr.value + 1]
        deviceController.concentration1SettingValue = (buffer[shiftAddr + 2 * DeviceAddr.concentration1SettingValueAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration1SettingValueAddr.value + 1]
        deviceController.concentration2SettingValue = (buffer[shiftAddr + 2 * DeviceAddr.concentration2SettingValueAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration2SettingValueAddr.value + 1]
        deviceController.concentration3SettingValue = (buffer[shiftAddr + 2 * DeviceAddr.concentration3SettingValueAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration3SettingValueAddr.value + 1]
        deviceController.waterAdd = (buffer[shiftAddr + 2 * DeviceAddr.waterAddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.waterAddAddr.value + 1]
        deviceController.concentration1Add = (buffer[shiftAddr + 2 * DeviceAddr.concentration1AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration1AddAddr.value + 1]
        deviceController.concentration2Add = (buffer[shiftAddr + 2 * DeviceAddr.concentration2AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration2AddAddr.value + 1]
        deviceController.concentration3Add = (buffer[shiftAddr + 2 * DeviceAddr.concentration3AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration3AddAddr.value + 1]
        deviceController.chemical1Add = (buffer[shiftAddr + 2 * DeviceAddr.chemical1AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical1AddAddr.value + 1]
        deviceController.chemical2Add = (buffer[shiftAddr + 2 * DeviceAddr.chemical2AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical2AddAddr.value + 1]
        deviceController.chemical3Add = (buffer[shiftAddr + 2 * DeviceAddr.chemical3AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical3AddAddr.value + 1]
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
        _daySelect = (buffer[shiftAddr + 2 * DeviceAddr.daySelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.daySelectAddr.value + 1]
        if _daySelect != deviceController.daySelect:
            deviceController.daySelect = _daySelect
        _hourSelect = (buffer[shiftAddr + 2 * DeviceAddr.hourSelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.hourSelectAddr.value + 1]
        if _hourSelect != deviceController.hourSelect:
            deviceController.hourSelect = _hourSelect
        _minuteSelect = (buffer[shiftAddr + 2 * DeviceAddr.minuteSelectAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.minuteSelectAddr.value + 1]
        if _minuteSelect != deviceController.minuteSelect:
            deviceController.minuteSelect = _minuteSelect
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
        _waterAdd = (buffer[shiftAddr + 2 * DeviceAddr.waterAddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.waterAddAddr.value + 1]
        if _waterAdd != deviceController.waterAdd:
            deviceController.waterAdd = _waterAdd
        _concentration1Add = (buffer[shiftAddr + 2 * DeviceAddr.concentration1AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration1AddAddr.value + 1]
        if _concentration1Add != deviceController.concentration1Add:
            deviceController.concentration1Add = _concentration1Add
        _concentration2Add = (buffer[shiftAddr + 2 * DeviceAddr.concentration2AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration2AddAddr.value + 1]
        if _concentration2Add != deviceController.concentration2Add:
            deviceController.concentration2Add = _concentration2Add
        _concentration3Add = (buffer[shiftAddr + 2 * DeviceAddr.concentration3AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.concentration3AddAddr.value + 1]
        if _concentration3Add != deviceController.concentration3Add:
            deviceController.concentration3Add = _concentration3Add
        _chemical1Add = (buffer[shiftAddr + 2 * DeviceAddr.chemical1AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical1AddAddr.value + 1]
        if _chemical1Add != deviceController.chemical1Add:
            deviceController.chemical1Add = _chemical1Add
        _chemical2Add = (buffer[shiftAddr + 2 * DeviceAddr.chemical2AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical2AddAddr.value + 1]
        if _chemical2Add != deviceController.chemical2Add:
            deviceController.chemical2Add = _chemical2Add
        _chemical3Add = (buffer[shiftAddr + 2 * DeviceAddr.chemical3AddAddr.value] <<8) | buffer[shiftAddr + 2 * DeviceAddr.chemical3AddAddr.value + 1]
        if _chemical3Add != deviceController.chemical3Add:
            deviceController.chemical3Add = _chemical3Add
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
        print(deviceInfo)
    pass



    