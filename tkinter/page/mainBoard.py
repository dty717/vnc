from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from components.table import SimpleTable
from components.groupLabelButton import GroupLabelButton
from service.device import write_single_register, write_single_coil, DeviceAddr, deviceInfo, deviceController, power, waterDetect, lastClickStartTime, lastSelectTime
from database.mongodb import dbGetLastHistory

from config.config import primaryColor,usingWaterDetect
mainHistoryText = None
backgroundColors = ["#ffffff", primaryColor]

def test():
    messagebox.showinfo("设置", str(deviceController))
    messagebox.showinfo("信息", str(deviceInfo))
    # updateMainDate(2022,12,12,1,1,32,121.2112,0)

def stateString(state):
    if state == 0:
        if waterDetect.value or not usingWaterDetect:
            return "正常"
        else:
            return "设备进水"
    else:
        if waterDetect.value or not usingWaterDetect:
            return "异常"
        else:
            return "异常且进水"

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
        beforeHeaderFrame.pack(side=TOP, fill=X, pady=30)
        headerFrame = Frame(self, bg=primaryColor)
        mainHistory = Label(headerFrame, textvariable=self.mainHistoryText,
                            fg="white", bg=primaryColor, font=(None, 16), justify="left")
        mainHistory.pack(side=LEFT, padx=40)
        #  -after, -anchor, -before, -expand, -fill, -in, -ipadx, -ipady, -padx, -pady, or -side
        stopButton = Button(headerFrame, text="设备急停", fg="white", bg="red", font=(None, 20),command = self.stop,activebackground="darkred",activeforeground = "white")
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
        headerFrame.pack(side=TOP, fill=X, pady=10)
        #
        stateFrame = Frame(self, bg=primaryColor)
        stateLabel = Label(stateFrame, text="当前状态:", fg="black",
                           bg=primaryColor, font=(None, 16), justify="left")
        stateLabel.pack(side=LEFT)
        self.currentModelSelectText = StringVar()
        self.currentModelSelectText.set(
            self.getcurrentModelSelect(deviceInfo.currentModelSelect))
        currentModelSelectButton = Button(stateFrame, textvariable=self.currentModelSelectText,
                                          relief=FLAT, fg="black", disabledforeground="black", bg=primaryColor, font=(None, 16))
        currentModelSelectButton.pack(side=LEFT, padx=10)
        currentModelSelectButton["state"] = DISABLED
        self.currentOperationSelectText = StringVar()
        self.currentOperationSelectText.set(
            self.getCurrentOperationSelect(deviceInfo.currentOperationSelect))
        currentOperationSelectButton = Button(stateFrame, textvariable=self.currentOperationSelectText,
                                              relief=FLAT, fg="black", disabledforeground="black", bg=primaryColor, font=(None, 16))
        currentOperationSelectButton.pack(side=LEFT, padx=0)
        currentOperationSelectButton["state"] = DISABLED
        self.currentStateText = StringVar()
        self.currentStateText.set(
            self.getCurrentState(deviceInfo.currentState))
        currentStateButton = Button(stateFrame, textvariable=self.currentStateText, relief=FLAT,
                                    fg="black", disabledforeground="black", bg=primaryColor, font=(None, 16))
        currentStateButton.pack(side=LEFT, padx=10)
        currentStateButton["state"] = DISABLED
        #
        stateFrame.pack(side=TOP, fill=X, pady=10, padx=40)
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
        self.selectOperateButton.pack(side="left", padx=10, pady=10)
        self.selectIntervalButton = Button(
            modelSelectGroupLine1, text="间隔做样", command=self.selectInterval, font=(None, 12))
        self.selectIntervalButton.pack(side="left", padx=10, pady=10)
        self.selectHourButton = Button(
            modelSelectGroupLine1, text="整点做样", command=self.selectHour, font=(None, 12))
        self.selectHourButton.pack(side="left", padx=10, pady=10)
        modelSelectGroupLine1.pack(fill=X)
        # Line2
        modelSelectGroupLine2 = Frame(modelSelectGroup, bg=primaryColor)
        self.selectCalibrateButton = Button(
            modelSelectGroupLine2, text="标定模式", command=self.selectCalibrate, font=(None, 12))
        self.selectCalibrateButton.pack(side="left", padx=10, pady=10)
        self.selectPumpButton = Button(
            modelSelectGroupLine2, text="手动进样", command=self.selectPump, font=(None, 12))
        self.selectPumpButton.pack(side="left", padx=10, pady=10)
        self.selectIdleButton = Button(
            modelSelectGroupLine2, text="空闲模式", command=self.selectIdle, font=(None, 12))
        self.selectIdleButton.pack(side="left", padx=10, pady=10)
        modelSelectGroupLine2.pack(fill=X)
        modelSelectGroup.pack(side=LEFT, anchor=N, padx=40)
        #
        #operationSelectGroup
        #
        operationSelectGroup = GroupLabelButton(self, title="手动做样", padx=10)
        # Line1
        operationSelectGroupLine1 = Frame(
            operationSelectGroup, bg=primaryColor)
        self.operateSampleButton = Button(
            operationSelectGroupLine1, text="水样", command=self.operateSample, font=(None, 12))
        self.operateSampleButton.pack(side="left", padx=10, pady=10)
        self.operateConcentration1Button = Button(
            operationSelectGroupLine1, text="标一", command=self.operateConcentration1, font=(None, 12))
        self.operateConcentration1Button.pack(side="left", padx=10, pady=10)
        operationSelectGroupLine1.pack(fill=X)
        # Line2
        operationSelectGroupLine2 = Frame(
            operationSelectGroup, bg=primaryColor)
        self.operateConcentration2Button = Button(
            operationSelectGroupLine2, text="标二", command=self.operateConcentration2, font=(None, 12))
        self.operateConcentration2Button.pack(side="left", padx=10, pady=10)
        self.operateConcentration3Button = Button(
            operationSelectGroupLine2, text="标三", command=self.operateConcentration3, font=(None, 12))
        self.operateConcentration3Button.pack(side="left", padx=10, pady=10)
        operationSelectGroupLine2.pack(fill=X)
        operationSelectGroup.pack(side=LEFT, anchor=N, padx=50)
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
    def selectModelButton(self, value):
        if value == 0:
            return self.selectIdleButton
        elif value == 1:
            return self.selectOperateButton
        elif value == 2:
            return self.selectIntervalButton
        elif value == 3:
            return self.selectHourButton
        elif value == 4:
            return self.selectCalibrateButton
        elif value == 5:
            return self.selectPumpButton
    def getcurrentModelSelect(self, value):
        if value == 0:
            return "空闲模式"
        elif value == 1:
            return "手动做样"
        elif value == 2:
            return "间隔做样"
        elif value == 3:
            return "整点做样"
        elif value == 4:
            return "标定模式"
        elif value == 5:
            return "手动进样"
    def getCurrentOperationSelect(self, value):
        if value == 0:
            return "空闲"
        elif value == 1:
            return "水样"
        elif value == 2:
            return "标一"
        elif value == 3:
            return "标二"
        elif value == 4:
            return "标三"

    def getCurrentState(self, value):
        if value == 0:
            return "仪器空闲"
        elif value == 1:
            return "做样前准备"
        elif value == 2:
            return "抽废液"
        elif value == 3:
            return "排废液"
        elif value == 4:
            return "抽蒸馏水"
        elif value == 5:
            return "进蒸馏水"
        elif value == 6:
            return "抽空气"
        elif value == 7:
            return "进空气"
        elif value == 8:
            return "抽水样"
        elif value == 9:
            return "进水样"
        elif value == 10:
            return "抽试剂一"
        elif value == 11:
            return "进试剂一"
        elif value == 12:
            return "抽试剂二"
        elif value == 13:
            return "进试剂二"
        elif value == 14:
            return "抽试剂三"
        elif value == 15:
            return "进试剂三"
        elif value == 16:
            return "加热"
        elif value == 17:
            return "冷却"
        elif value == 18:
            return "找基值"
        elif value == 19:
            return "找峰值"
        elif value == 20:
            return "抽反应液"
        elif value == 21:
            return "推反应液"
    def selectIdle(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value,
                         0, self.selectModelButton(0))
        return
    def selectOperate(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value,
                         1, self.selectModelButton(1))
        return
    def selectInterval(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value,
                         2, self.selectModelButton(2))
        return
    def selectHour(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value,
                         3, self.selectModelButton(3))
        return
    def selectCalibrate(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value,
                         4, self.selectModelButton(4))
        return
    def selectPump(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value,
                         5, self.selectModelButton(5))
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
        if value == 1:
            return self.operateSampleButton
        elif value == 2:
            return self.operateConcentration1Button
        elif value == 3:
            return self.operateConcentration2Button
        elif value == 4:
            return self.operateConcentration3Button
    def operateSample(self):
        self.selectOperation(
            DeviceAddr.operationSelectAddr.value, 1, self.selectOperationButton(1))
        return
    def operateConcentration1(self):
        self.selectOperation(
            DeviceAddr.operationSelectAddr.value, 2, self.selectOperationButton(2))
        return
    def operateConcentration2(self):
        self.selectOperation(
            DeviceAddr.operationSelectAddr.value, 3, self.selectOperationButton(3))
        return
    def operateConcentration3(self):
        self.selectOperation(
            DeviceAddr.operationSelectAddr.value, 4, self.selectOperationButton(4))
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
        self.currentModelSelectText.set(
            self.getcurrentModelSelect(deviceInfo.currentModelSelect))
        self.currentOperationSelectText.set(
            self.getCurrentOperationSelect(deviceInfo.currentOperationSelect))
        self.currentStateText.set(
            self.getCurrentState(deviceInfo.currentState))
        self.lastSelectModelButton.configure(background=backgroundColors[0])
        modelButton = self.selectModelButton(deviceController.modelSelect)
        modelButton.configure(background=backgroundColors[1])
        self.lastSelectModelButton = modelButton
        #
        if self.lastSelectOperationButton != None:
            self.lastSelectOperationButton.configure(
                background=backgroundColors[0])
        operationButton = self.selectModelButton(deviceController.modelSelect)
        operationButton.configure(background=backgroundColors[1])
        # self.lastSelectOperationButton = operationButton
        #
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
