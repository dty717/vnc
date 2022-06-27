from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from components.table import SimpleTable
from components.groupLabelButton import GroupLabelButton
from service.device import write_single_register,write_single_coil,DeviceAddr,deviceInfo,deviceController
from database.mongodb import dbGetLastHistory

mainHistoryText = None
backgroundColors = ["#ffffff","#1fa1af"]

def test():
    messagebox.showinfo("设置", str(deviceController))
    updateMainDate(2022,12,12,1,1,32,121.2112,0)

def stateString(state):
    if state == 0:
        return "正常"
    return "异常"

def updateMainDate(year, month, day, hour, minitue, second, value, state):
    global mainHistoryText
    mainHistoryText.set("做样时间:"+datetime(year, month, day, hour, minitue, second).strftime("%Y-%m-%d %H:%M:%S")+"\n" +
                 "做样数据:"+str(value)+"mg/L\n" +
                 "报警状态:"+stateString(state))

class MainBoard(Frame):
    def __init__(self, master, header,data, **kargs):
        super().__init__(master, kargs)
        # concentration2Histories = list(dbGetConcentration2History(nPerPage = 0)); 
        # for index,concentration2History in enumerate(concentration2Histories):
        #     concentration2History['time'] = concentration2History['time'].strftime("%Y-%m-%d %H:%M:%S")
        #     concentration2HistoryTableDatas.insert(parent='',index='end',iid = index,text=str(index+1),values=tuple(concentration2History.values())[1:])
        self.mainHistoryText = StringVar()
        lastHistory = list(dbGetLastHistory()); 
        if len(lastHistory) == 1:
            lastHistory = lastHistory[0]
            self.mainHistoryText.set("做样时间:"+lastHistory['time'].strftime("%Y-%m-%d %H:%M:%S")+"\n" +
                 "做样数据:"+str(lastHistory['value'])+"mg/L\n" +
                 "报警状态:"+stateString(deviceInfo.warningInfo))
        else:
            self.mainHistoryText.set("""做样时间:
    做样数据:
    报警状态:""")
        headerFrame = Frame(self, bg="red")
        mainHistory = Label(headerFrame, textvariable=self.mainHistoryText, fg="black", bg="white")
        mainHistory.pack(side=LEFT)
        stopButton = Button(headerFrame, text="停止", fg="red", bg="white",command = self.stop)
        stopButton.pack(side=RIGHT)
        headerFrame.pack(side=TOP, fill=X)
        mainTable = SimpleTable(self, header=header, data=data)
        mainTable.pack(side=BOTTOM, fill=X)
        #
        #modelSelectGroup
        #
        modelSelectGroup = GroupLabelButton(self,title = "模式选择")
        # Line1
        modelSelectGroupLine1 = Frame(modelSelectGroup, bg="red")
        self.selectAutoButton = Button(modelSelectGroupLine1, text="自动做样",command = self.selectAuto)
        self.selectAutoButton.pack(side="left")
        self.selectIntervalButton = Button(modelSelectGroupLine1, text="间隔做样",command = self.selectInterval)
        self.selectIntervalButton.pack(side="left")
        self.selectHourButton = Button(modelSelectGroupLine1, text="整点做样",command = self.selectHour)
        self.selectHourButton.pack(side="left")
        modelSelectGroupLine1.pack(fill = X)
        # Line2
        modelSelectGroupLine2 = Frame(modelSelectGroup, bg="red")
        self.selectCalibrateButton = Button(modelSelectGroupLine2, text="标定模式",command = self.selectCalibrate)
        self.selectCalibrateButton.pack(side="left")
        self.selectOperateButton = Button(modelSelectGroupLine2, text="手动做样",command = self.selectOperate)
        self.selectOperateButton.pack(side="left")
        modelSelectGroupLine2.pack(fill = X)
        modelSelectGroup.pack(side=LEFT)
        # 
        #operationSelectGroup
        #  
        operationSelectGroup = GroupLabelButton(self,title = "手动做样")
        # Line1
        operationSelectGroupLine1 = Frame(operationSelectGroup, bg="red")
        self.operateSampleButton = Button(operationSelectGroupLine1, text="水样",command = self.operateSample)
        self.operateSampleButton.pack(side="left")
        self.operateConcentration1Button = Button(operationSelectGroupLine1, text="标一",command = self.operateConcentration1)
        self.operateConcentration1Button.pack(side="left")
        operationSelectGroupLine1.pack(fill = X)
        # Line2
        operationSelectGroupLine2 = Frame(operationSelectGroup, bg="red")
        self.operateConcentration2Button = Button(operationSelectGroupLine2, text="标二",command = self.operateConcentration2)
        self.operateConcentration2Button.pack(side="left")
        self.operateConcentration3Button = Button(operationSelectGroupLine2, text="标三",command = self.operateConcentration3)
        self.operateConcentration3Button.pack(side="left")
        operationSelectGroupLine2.pack(fill = X)
        operationSelectGroup.pack(side=RIGHT)
        self.lastSelectModelButton = self.selectModelButton(deviceController.modelSelect)
        self.lastSelectModelButton.configure(background=backgroundColors[1])
        self.lastSelectOperationButton = self.selectOperationButton(deviceController.operationSelect)
        self.lastSelectOperationButton.configure(background=backgroundColors[1])
    def selectModelButton(self,value):
        if value == 0:
            return self.selectAutoButton
        elif value == 1:
            return self.selectIntervalButton
        elif value == 2:
            return self.selectHourButton
        elif value == 3:
            return self.selectCalibrateButton
        elif value == 4:
            return self.selectOperateButton
    def selectAuto(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value, 0 , self.selectModelButton(0))
        return
    def selectInterval(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value, 1 , self.selectModelButton(1))
        return
    def selectHour(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value, 2 , self.selectModelButton(2))
        return
    def selectCalibrate(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value, 3 , self.selectModelButton(3))
        return
    def selectOperate(self):
        self.selectModel(DeviceAddr.modelSelectAddr.value, 4 , self.selectModelButton(4))
        return
    def selectModel(self,addr,value,button):
        write_single_register(addr, value, 
                lambda rec: self.lastSelectModelButton.configure(background=backgroundColors[0])
                    or button.configure(background=backgroundColors[1])
                    or setattr(self,'lastSelectModelButton' , button)
                    or setattr(deviceController,'modelSelect',value), repeatTimes = 0 , needMesBox = True)
        return
    def selectOperationButton(self,value):
        if value == 0:
            return self.operateSampleButton
        elif value == 1:
            return self.operateConcentration1Button
        elif value == 2:
            return self.operateConcentration1Button
        elif value == 3:
            return self.operateConcentration1Button
    def operateSample(self):
        self.selectOperation(DeviceAddr.operationSelectAddr.value, 0 , self.selectOperationButton(0))
        return
    def operateConcentration1(self):
        self.selectOperation(DeviceAddr.operationSelectAddr.value, 1 , self.selectOperationButton(1))
        return
    def operateConcentration2(self):
        self.selectOperation(DeviceAddr.operationSelectAddr.value, 2 , self.selectOperationButton(2))
        return
    def operateConcentration3(self):
        self.selectOperation(DeviceAddr.operationSelectAddr.value, 3 , self.selectOperationButton(3))
        return
    def selectOperation(self,addr,value,button):
        write_single_register(addr, value, 
                lambda rec: self.lastSelectOperationButton.configure(background=backgroundColors[0])
                    or button.configure(background=backgroundColors[1])
                    or setattr(self,'lastSelectOperationButton' , button)
                    or setattr(deviceController,'operationSelect',value), repeatTimes = 0 , needMesBox = True)
        return
    def stop(self):
        # write_single_coil
        write_single_coil(0, 1, lambda rec: None, repeatTimes = 0 , needMesBox = True)
        return
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())


# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)
