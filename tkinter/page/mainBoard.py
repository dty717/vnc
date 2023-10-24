from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from components.table import SimpleTable
from components.groupLabelButton import GroupLabelButton
from service.device import write_single_register, write_single_coil, DeviceAddr, deviceInfo, deviceController, lastClickStartTime, lastSelectTime,\
    power, waterDetect
from service.motor import opticalUpSwitch, opticalDownSwitch, magnetism, FIXPOSITION, FASTEN, SEPARATE, STOP, motorState, IDLE
from database.mongodb import dbGetLastHistory

from config.config import primaryColor, usingWaterDetect
mainHistoryText = None
backgroundColors = ["#ffffff", primaryColor]

def stateString(state):
    if state == 0:
        if waterDetect.value or not usingWaterDetect:
            return "正常"
        else:
            return "设备进水"
    else:
        errorInfo = ''
        if state == 1:
            errorInfo = "缺试剂一"
        elif state == 2:
            errorInfo = "缺试剂二"
        elif state == 3:
            errorInfo = "缺试剂三"
        elif state == 4:
            errorInfo = "缺水样"
        elif state == 5:
            errorInfo = "缺蒸馏水"
        elif state == 6:
            errorInfo = "超温度上限"
        elif state == 7:
            errorInfo = "超量程上限"
        elif state == 8:
            errorInfo = "断电异常"
        elif state == 10:
            errorInfo = "电机异常"
        elif state == 13:
            errorInfo = "加热异常"
        if waterDetect.value or not usingWaterDetect:
            return errorInfo
        else:
            return errorInfo+"且进水"


def updateMainDate(year, month, day, hour, minitue, second, value, state):
    global mainHistoryText
    mainHistoryText.set("做样时间:"+datetime(year, month, day, hour, minitue, second).strftime("%Y-%m-%d %H:%M:%S")+"\n" +
                        "做样数据:"+str(value)+"mg/L\n" +
                        "报警状态:"+stateString(state))


class MainBoard(Frame):
    def __init__(self, master, header, data, **kargs):
        super().__init__(master, kargs)
        # concentration2Histories = list(dbGetConcentration2History(nPerPage = 0))
        # for index,concentration2History in enumerate(concentration2Histories):
        #     concentration2History['time'] = concentration2History['time'].strftime("%Y-%m-%d %H:%M:%S")
        #     concentration2HistoryTableDatas.insert(parent='',index='end',iid = index,text=str(index+1),values=tuple(concentration2History.values())[1:])
        self.mainHistoryText = StringVar()
        lastHistory = list(dbGetLastHistory())
        if len(lastHistory) == 1:
            lastHistory = lastHistory[0]
            self.mainHistoryText.set("做样时间:"+lastHistory['time'].strftime("%Y-%m-%d %H:%M:%S")+"\n" +
                                     "做样数据:"+str(round(lastHistory['CValue'], 4))+"mg/L\n" +
                                     "报警状态:"+stateString(deviceInfo.warningInfo))
        else:
            self.mainHistoryText.set("""做样时间:
做样数据:
报警状态:"""+stateString(deviceInfo.warningInfo))
        #
        beforeHeaderFrame = Frame(self, bg=primaryColor)
        beforeHeaderFrame.pack(side=TOP, fill=X, pady=20)
        headerFrame = Frame(self, bg=primaryColor)
        mainHistory = Label(headerFrame, textvariable=self.mainHistoryText,
                            fg="white", bg=primaryColor, font=(None, 16), justify="left")
        mainHistory.pack(side=LEFT, padx=40)
        #  -after, -anchor, -before, -expand, -fill, -in, -ipadx, -ipady, -padx, -pady, or -side
        stopButton = Button(headerFrame, text="设备急停", fg="white", bg="red", font=(
            None, 20), command=self.stop, activebackground="darkred", activeforeground="white")
        # stopButton = Button(headerFrame, text="设备急停", fg="white", bg="red", font=(None, 20), command=test, activebackground="darkred", activeforeground="white")
        stopButton.pack(side=LEFT, padx=10)
        self.powerButton = Button(headerFrame, text="开启设备", fg="white", bg="red", font=(
            None, 20), command=self.setPower, activebackground="darkred", activeforeground="white")
        self.powerButton.pack(side=LEFT)
        if power.value == 1:
            self.powerButton.configure(
                background="green", text="关闭设备", activebackground="darkgreen")
        else:
            self.powerButton.configure(
                background="red", text="开启设备", activebackground="darkred")
        #
        headerFrame.pack(side=TOP, fill=X, pady=5)
        #
        stateFrame = Frame(self, bg=primaryColor)
        stateLabel = Label(stateFrame, text="当前状态:", fg="black",
                           bg=primaryColor, font=(None, 16), justify="left")
        stateLabel.pack(side=LEFT)
        self.currentTemperatureText = StringVar()
        self.currentTemperatureText.set(
            str(round(deviceInfo.currentTemperature, 2))+"℃")
        currentTemperatureButton = Button(stateFrame, textvariable=self.currentTemperatureText,
                                          relief=FLAT, fg="black", disabledforeground="black", bg=primaryColor, font=(None, 16))
        currentTemperatureButton.pack(side=LEFT, padx=10)
        currentTemperatureButton["state"] = DISABLED
        self.currentDataFlagText = StringVar()
        self.currentDataFlagText.set(
            self.getCurrentDataFlag(deviceInfo.currentDataFlag))
        currentDataFlagButton = Button(stateFrame, textvariable=self.currentDataFlagText,
                                       relief=FLAT, fg="black", disabledforeground="black", bg=primaryColor, font=(None, 16))
        currentDataFlagButton.pack(side=LEFT, padx=0)
        currentDataFlagButton["state"] = DISABLED
        self.currentStateText = StringVar()
        self.currentStateText.set(
            self.getCurrentState(deviceInfo.currentState))
        currentStateButton = Button(stateFrame, textvariable=self.currentStateText, relief=FLAT,
                                    fg="black", disabledforeground="black", bg=primaryColor, font=(None, 16))
        currentStateButton.pack(side=LEFT, padx=10)
        currentStateButton["state"] = DISABLED
        #
        stateFrame.pack(side=TOP, fill=X, pady=5, padx=40)
        #
        inputStateFrame = Frame(self, bg=primaryColor)
        stateLabel = Label(inputStateFrame, text="传感器状态:", fg="black",
                           bg=primaryColor, font=(None, 16), justify="left")
        stateLabel.pack(side=LEFT)
        self.opticalUpSwitchText = StringVar()
        self.opticalUpSwitchText.set("上光耦" + ["闭", "通"][opticalUpSwitch.value])
        self.opticalUpSwitchButton = Button(inputStateFrame, textvariable=self.opticalUpSwitchText,
                                       relief=FLAT, fg="black", disabledforeground="black", bg=primaryColor, font=(None, 16))
        self.opticalUpSwitchButton.pack(side=LEFT, padx=10)
        self.opticalUpSwitchButton["state"] = DISABLED
        self.opticalDownSwitchText = StringVar()
        self.opticalDownSwitchText.set(
            "下光耦" + ["闭", "通"][opticalDownSwitch.value])
        self.opticalDownSwitchButton = Button(inputStateFrame, textvariable=self.opticalDownSwitchText,
                                         relief=FLAT, fg="black", disabledforeground="black", bg=primaryColor, font=(None, 16))
        self.opticalDownSwitchButton.pack(side=LEFT, padx=0)
        self.opticalDownSwitchButton["state"] = DISABLED

        self.magnetismText = StringVar()
        self.magnetismText.set("接近开关" + ["远", "近"][magnetism.value])
        self.magnetismButton = Button(inputStateFrame, textvariable=self.magnetismText, relief=FLAT,
                                 fg="black", disabledforeground="black", bg=primaryColor, font=(None, 16))
        self.magnetismButton.pack(side=LEFT, padx=10)
        self.magnetismButton["state"] = DISABLED
        #
        inputStateFrame.pack(side=TOP, fill=X, pady=5, padx=40)
        #
        self.mainTable = SimpleTable(self, header=header, data=data)
        self.mainTable.pack(side=BOTTOM, fill=X)
        #
        #modelSelectGroup
        #
        modelSelectGroup = GroupLabelButton(self, title="模式选择", padx=10)
        # Line1
        modelSelectGroupLine1 = Frame(modelSelectGroup, bg=primaryColor)
        self.selectOperateButton = Button(
            modelSelectGroupLine1, text="手动做样", command=self.selectOperate, font=(None, 12))
        self.selectOperateButton.pack(side="left", padx=10, pady=5)
        modelSelectGroupLine1.pack(fill=X)
        # Line2
        modelSelectGroupLine2 = Frame(modelSelectGroup, bg=primaryColor)
        self.selectAutoButton = Button(
            modelSelectGroupLine2, text="自动做样", command=self.selectAuto, font=(None, 12))
        self.selectAutoButton.pack(side="left", padx=10, pady=5)
        modelSelectGroupLine2.pack(fill=X)
        modelSelectGroup.pack(side=LEFT, anchor=N, pady=10, padx=(40, 10))
        #
        #operationSelectGroup
        #
        operationSelectGroup = GroupLabelButton(self, title="手动做样", padx=10)
        # Line1
        operationSelectGroupLine1 = Frame(
            operationSelectGroup, bg=primaryColor)
        self.operateSampleButton = Button(
            operationSelectGroupLine1, text="水样", command=self.operateSample, font=(None, 12))
        self.operateSampleButton.pack(side="left", padx=10, pady=5)
        self.operateConcentration1Button = Button(
            operationSelectGroupLine1, text="标一", command=self.operateConcentration1, font=(None, 12))
        self.operateConcentration1Button.pack(side="left", padx=10, pady=5)
        operationSelectGroupLine1.pack(fill=X)
        # Line2
        operationSelectGroupLine2 = Frame(
            operationSelectGroup, bg=primaryColor)
        self.operateConcentration2Button = Button(
            operationSelectGroupLine2, text="标二", command=self.operateConcentration2, font=(None, 12))
        self.operateConcentration2Button.pack(side="left", padx=10, pady=5)
        self.operateConcentration3Button = Button(
            operationSelectGroupLine2, text="标三", command=self.operateConcentration3, font=(None, 12))
        self.operateConcentration3Button.pack(side="left", padx=10, pady=5)
        operationSelectGroupLine2.pack(fill=X)
        operationSelectGroup.pack(side=LEFT, anchor=N, pady=10, padx=10)
        #
        #exchangeOperationGroup
        #
        exchangeOperationGroup = GroupLabelButton(self, title="换液操作", padx=10)
        # Line1
        exchangeOperationGroupLine1 = Frame(
            exchangeOperationGroup, bg=primaryColor)
        self.fixPositionButton = Button(
            exchangeOperationGroupLine1, text="确定位置", command=self.fixPosition, font=(None, 12))
        self.fixPositionButton.pack(side="left", padx=10, pady=5)
        self.fastenButton = Button(
            exchangeOperationGroupLine1, text="固定转盘", command=self.fasten, font=(None, 12))
        self.fastenButton.pack(side="left", padx=10, pady=5)
        self.requestOrderButton = Button(
            exchangeOperationGroupLine1, text="发送指令", command=self.requestOrder, font=(None, 12))
        self.requestOrderButton.pack(side="left", padx=10, pady=5)
        exchangeOperationGroupLine1.pack(fill=X)
        # Line2
        exchangeOperationGroupLine2 = Frame(
            exchangeOperationGroup, bg=primaryColor)
        self.separateButton = Button(
            exchangeOperationGroupLine2, text="分离转盘", command=self.separate, font=(None, 12))
        self.separateButton.pack(side="left", padx=10, pady=5)
        self.stopExchangeButton = Button(
            exchangeOperationGroupLine2, text="停止换液", command=self.stopExchange, font=(None, 12))
        self.stopExchangeButton.pack(side="left", padx=10, pady=5)
        exchangeOperationGroupLine2.pack(fill=X)
        exchangeOperationGroup.pack(side=LEFT, anchor=N, pady=10, padx=10)
        #
        # lastSelectModelButton, lastSelectOperationButton
        #
        self.lastSelectModelButton = self.selectModelButton(
            deviceController.modelSelect)
        self.lastSelectModelButton.configure(background=backgroundColors[1])
        self.lastSelectOperationButton = self.selectOperationButton(
            deviceController.operationSelect)
        if self.lastSelectOperationButton != None:
            self.lastSelectOperationButton.configure(
                background=backgroundColors[1])
        self.lastExchangeOperationButton = None

    def selectModelButton(self, value):
        if value == 0:
            return self.selectOperateButton
        elif value == 1:
            return self.selectAutoButton

    def getCurrentDataFlag(self, value):
        if value == 0:
            return "未做样"
        elif value == 4:
            return "水样"
        elif value == 1:
            return "标一"
        elif value == 2:
            return "标二"
        elif value == 3:
            return "标三"
        return ""

    def getCurrentState(self, value):
        if value == 0:
            return "仪器空闲"
        elif value == 1:
            return "做样前排废液"
        elif value == 2:
            return "做样前进清洗液"
        elif value == 3:
            return "清洗空气混合"
        elif value == 4:
            return "做样前排清洗液"
        elif value == 5:
            return "取试剂一"
        elif value == 6:
            return "取试剂二"
        elif value == 7:
            return "取试剂三"
        elif value == 8:
            return "取水样"
        elif value == 9:
            return "排试剂一多余"
        elif value == 10:
            return "排试剂二多余"
        elif value == 11:
            return "排试剂三多余"
        elif value == 12:
            return "排水样多余"
        elif value == 13:
            return "试剂一进消解池"
        elif value == 14:
            return "试剂二进消解池"
        elif value == 15:
            return "试剂三进消解池"
        elif value == 16:
            return "水样进消解池"
        elif value == 17:
            return "进样后空气混合"
        elif value == 18:
            return "加热消解"
        elif value == 19:
            return "冷却"
        elif value == 20:
            return "找基值进清洗液"
        elif value == 21:
            return "静止找基值"
        elif value == 22:
            return "找基值排清洗液"
        elif value == 23:
            return "静止找峰值"
        elif value == 24:
            return "清洗储液环"
        elif value == 25:
            return "做样前预填充水样"
        elif value == 26:
            return "做样后排废液"
        elif value == 27:
            return "做样后进清洗液"
        elif value == 28:
            return "做样后清洗曝气"
        elif value == 29:
            return "做样后排清洗液"
        elif value == 30:
            return "排废液"
        elif value == 32:
            return "取标一"
        elif value == 33:
            return "取标二"
        elif value == 34:
            return "取标三"
        elif value == 39:
            return "排多余标一"
        elif value == 40:
            return "排多余标二"
        elif value == 41:
            return "排多余标三"
        elif value == 45:
            return "标一进消解池"
        elif value == 46:
            return "标二进消解池"
        elif value == 47:
            return "标三进消解池"

    def selectOperate(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value,
                         0, self.selectModelButton(0))
        return

    def selectAuto(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value,
                         1, self.selectModelButton(1))
        return

    def selectModel(self, addr, value, button):
        write_single_register(addr, value,
                              lambda rec: self.lastSelectModelButton.configure(
                                  background=backgroundColors[0])
                              or button.configure(background=backgroundColors[1])
                              or setattr(self, 'lastSelectModelButton', button)
                              or setattr(deviceController, 'modelSelect', value), repeatTimes=0, needMesBox=True)
        return

    def selectOperationButton(self, value):
        if value == 4:
            return self.operateSampleButton
        elif value == 1:
            return self.operateConcentration1Button
        elif value == 2:
            return self.operateConcentration2Button
        elif value == 3:
            return self.operateConcentration3Button

    def selectExchangeOperationButton(self, value):
        if value == FIXPOSITION:
            return self.fixPositionButton
        elif value == FASTEN:
            return self.fastenButton
        elif value == SEPARATE:
            return self.separateButton
        elif value == STOP:
            return self.stopExchangeButton

    def exchangeFunction(self, command):
        global motorState
        motorState.command = command
        exchangeOperationButton = self.selectExchangeOperationButton(command)
        exchangeOperationButton.configure(background=backgroundColors[1])
        if self.lastExchangeOperationButton != None and self.lastExchangeOperationButton != exchangeOperationButton:
            self.lastExchangeOperationButton.configure(
                background=backgroundColors[0])
        self.lastExchangeOperationButton = exchangeOperationButton

    def fixPosition(self):
        self.exchangeFunction(FIXPOSITION)
        return

    def fasten(self):
        self.exchangeFunction(FASTEN)
        return

    def separate(self):
        self.exchangeFunction(SEPARATE)
        return

    def stopExchange(self):
        self.exchangeFunction(STOP)
        return

    def requestOrder(self):
        write_single_register(DeviceAddr.exchangeAddr.value, 1,
                              lambda rec: print(rec), repeatTimes=0, needMesBox=True)
        return

    def operateSample(self):
        self.selectOperation(
            DeviceAddr.operationSelectAddr.value, 7, self.selectOperationButton(4))
        return

    def operateConcentration1(self):
        self.selectOperation(
            DeviceAddr.operationSelectAddr.value, 1, self.selectOperationButton(1))
        return

    def operateConcentration2(self):
        self.selectOperation(
            DeviceAddr.operationSelectAddr.value, 2, self.selectOperationButton(2))
        return

    def operateConcentration3(self):
        self.selectOperation(
            DeviceAddr.operationSelectAddr.value, 3, self.selectOperationButton(3))
        return

    def selectOperation(self, addr, value, button):
        write_single_register(addr, value,
                              lambda rec: (self.lastSelectOperationButton and self.lastSelectOperationButton.configure(
                                  background=backgroundColors[0]))
                              or button.configure(background=backgroundColors[1])
                              or setattr(self, 'lastSelectOperationButton', button)
                              or setattr(deviceController, 'operationSelect', value), repeatTimes=0, needMesBox=True)
        return

    def stop(self):
        # write_single_coil
        write_single_coil(0, 1, lambda rec: None,
                          repeatTimes=0, needMesBox=True)
        return

    def setPower(self):
        global lastClickStartTime, lastSelectTime
        if power.value == 0:
            power.on()
            if power.value == 1:
                lastClickStartTime = datetime.now()
                self.powerButton.configure(
                    background="green", text="关闭设备", activebackground="darkgreen")
        else:
            power.off()
            if power.value == 0:
                lastClickStartTime = lastSelectTime
                self.powerButton.configure(
                    background="red", text="开启设备", activebackground="darkred")
        return

    def refreshPage(self):
        if power.value == 0:
            self.powerButton.configure(
                background="red", text="开启设备", activebackground="darkred")
        else:
            self.powerButton.configure(
                background="green", text="关闭设备", activebackground="darkgreen")
        #
        self.opticalUpSwitchText.set("上光耦" + ["闭", "通"][opticalUpSwitch.value])
        self.opticalUpSwitchButton.configure(background=backgroundColors[opticalUpSwitch.value])
        self.opticalDownSwitchText.set(
            "下光耦" + ["闭", "通"][opticalDownSwitch.value])
        self.opticalDownSwitchButton.configure(background=backgroundColors[opticalDownSwitch.value])
        self.magnetismText.set("接近开关" + ["近", "远"][magnetism.value])
        self.magnetismButton.configure(background=backgroundColors[magnetism.value])
        lastHistory = list(dbGetLastHistory())
        if len(lastHistory) == 1:
            lastHistory = lastHistory[0]
            self.mainHistoryText.set("做样时间:"+lastHistory['time'].strftime("%Y-%m-%d %H:%M:%S")+"\n" +
                                     "做样数据:"+str(round(lastHistory['CValue'], 4))+"mg/L\n" +
                                     "报警状态:"+stateString(deviceInfo.warningInfo))
        else:
            self.mainHistoryText.set("""做样时间:
做样数据:
报警状态:"""+stateString(deviceInfo.warningInfo))
        self.currentTemperatureText.set(
            str(round(deviceInfo.currentTemperature, 2))+"℃")
        self.currentStateText.set(
            self.getCurrentState(deviceInfo.currentState))
        modelButton = self.selectModelButton(deviceController.modelSelect)
        if modelButton != self.lastSelectModelButton:
            self.lastSelectModelButton.configure(
                background=backgroundColors[0])
        modelButton.configure(background=backgroundColors[1])
        self.lastSelectModelButton = modelButton
        #
        operationButton = self.selectModelButton(deviceController.modelSelect)
        if self.lastSelectOperationButton != None and (self.lastSelectOperationButton != operationButton):
            self.lastSelectOperationButton.configure(
                background=backgroundColors[0])
        operationButton.configure(background=backgroundColors[1])
        self.lastSelectOperationButton = operationButton
        #
        if motorState.command == IDLE and self.lastExchangeOperationButton != None:
            self.lastExchangeOperationButton.configure(
                background=backgroundColors[0])
        data = [
            ['标一', round(deviceInfo.concentration1Value, 4), round(deviceInfo.concentration1MaxValue, 4), round(
                deviceInfo.concentration1AValue, 4), round(deviceInfo.concentration1CValue, 4)],
            ['标二', round(deviceInfo.concentration2Value, 4), round(deviceInfo.concentration2MaxValue, 4), round(
                deviceInfo.concentration2AValue, 4), round(deviceInfo.concentration2CValue, 4)],
            ['标三', round(deviceInfo.concentration3Value, 4), round(deviceInfo.concentration3MaxValue, 4), round(
                deviceInfo.concentration3AValue, 4), round(deviceInfo.concentration3CValue, 4)],
            ['水样', round(deviceInfo.sampleValue, 4), round(deviceInfo.sampleMaxValue, 4), round(deviceInfo.sampleAValue, 4), round(deviceInfo.sampleCValue, 4)]]
        for row in range(4):
            for column in range(1, 5):
                self.mainTable.set(row + 1, column, data[row][column])
        return
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())


# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)
