from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import threading
from components.table import SimpleTable
from components.groupLabelButton import GroupLabelButton
from service.thread import thread_with_exception
from service.device import write_single_register, write_single_coil, DeviceAddr, deviceInfo, deviceController, waterDetect, \
        lastClickStartTime, lastSelectTime, \
        operatingAllStep, operatingAllStepCancel
from database.mongodb import dbGetLastFloatNineParametersHistory
from config.config import primaryColor, usingWaterDetect, deviceName, addrsID
mainHistoryText = None
backgroundColors = ["#ffffff", primaryColor]


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

def stepString(deviceAutoRun, deviceStep):
    stepStr = ""
    if deviceAutoRun:
        stepStr = "自动流程"
    elif deviceStep:
        stepStr = "手动流程"
    if deviceStep == 0x00:
        stepStr += "系统空闲"
    elif deviceStep == 0x01:
        stepStr += "(排空清水)"
    elif deviceStep == 0x02:
        stepStr += "(采集水样)"
    elif deviceStep == 0x03:
        stepStr += "(读取数据)"
    elif deviceStep == 0x04:
        stepStr += "(排空水样)"
    elif deviceStep == 0x05:
        stepStr += "(填充清水)"
    elif deviceStep == 0x06:
        stepStr += "(清洗滤膜)"
    elif deviceStep == 0x0A:
        stepStr += "(读取GPS)"
    return stepStr

def intToHex(a):
  return ('0'+str(hex(a)[2:]))[0:2]

class MainBoard(Frame):
    def __init__(self, master, header, data, **kargs):
        super().__init__(master, kargs)
        # concentration2Histories = list(dbGetConcentration2History(nPerPage = 0))
        # for index,concentration2History in enumerate(concentration2Histories):
        #     concentration2History['time'] = concentration2History['time'].strftime("%Y-%m-%d %H:%M:%S")
        #     concentration2HistoryTableDatas.insert(parent='',index='end',iid = index,text=str(index+1),values=tuple(concentration2History.values())[1:])
        self.mainHistoryText = StringVar()
        lastHistory = list(dbGetLastFloatNineParametersHistory())
        if len(lastHistory) == 1:
            lastHistory = lastHistory[0]
            self.mainHistoryText.set("设备名称:"+deviceName+"\n" +
                                    "设备ID:"+''.join(map(intToHex, addrsID))+"\n" +
                                    "做样时间:"+lastHistory['time'].strftime("%Y-%m-%d %H:%M:%S")+"\n" +
                                     "PH:"+str(round(lastHistory['PH'], 3))+"\n" +
                                     "温度:"+str(round(lastHistory['temp'], 2))+"°C\n" +
                                     "电导率:"+str(round(lastHistory['ele'], 3))+"uS/cm\n" +
                                     "浊度:"+str(round(lastHistory['tur'], 3))+"NTU\n" +
                                     "溶解氧:"+str(round(lastHistory['O2'], 3))+"mg/L\n" +
                                     "COD:"+str(round(lastHistory['COD'], 3))+"mg/L\n" +
                                     "氨氮:"+str(round(lastHistory['NH3'], 3))+"mg/L\n" +
                                     "硝氮:"+str(round(lastHistory['NO3'], 3))+"mg/L\n" +
                                     "叶绿素:"+str(round(lastHistory['chl'], 3))+"ug/L\n" +
                                     "位置:"+lastHistory['dataInfo']+"\n" +
                                     "仪器状态:"+stepString(deviceController.deviceAutoRun, deviceController.deviceStep)+"\n" +
                                     "报警状态:"+stateString(deviceInfo.warningInfo))
        else:
            self.mainHistoryText.set(
                "设备名称:"+deviceName+"\n" +
                "设备ID:"+''.join(map(intToHex, addrsID))+"\n" +
                """做样时间:
PH:
温度:
电导率:
浊度:
溶解氧:
COD:
氨氮:
硝氮:
叶绿素:
位置:
仪器状态:"""+stepString(deviceController.deviceAutoRun, deviceController.deviceStep)+"\n" +
                "报警状态:"+stateString(deviceInfo.warningInfo))
        #
        beforeHeaderFrame = Frame(self, bg=primaryColor)
        beforeHeaderFrame.pack(side=TOP, fill=X, pady=30)
        headerFrame = Frame(self, bg=primaryColor)
        mainHistory = Label(headerFrame, textvariable=self.mainHistoryText,
                            fg="white", bg=primaryColor, font=(None, 16), justify="left")
        mainHistory.pack(side=LEFT, padx=40)
        #  -after, -anchor, -before, -expand, -fill, -in, -ipadx, -ipady, -padx, -pady, or -side
        # stopButton = Button(headerFrame, text="设备急停", fg="white", bg="red", font=(None, 20),command = self.stop,activebackground="darkred",activeforeground = "white")
        # # stopButton = Button(headerFrame, text="设备急停", fg="white", bg="red", font=(None, 20), command=test, activebackground="darkred", activeforeground="white")
        # stopButton.pack(side=LEFT, padx=10)
        self.operationButton = Button(headerFrame, text="开启设备", fg="white", bg="red", font=(
            None, 20), command=self.operating, activebackground="darkred", activeforeground="white")
        self.operationButton.pack(side=LEFT, padx=40)
        if deviceController.deviceAutoRun == 1:
            self.operationButton.configure(
                background="green", text="关闭设备", activebackground="darkgreen")
        else:
            self.operationButton.configure(
                background="red", text="开启设备", activebackground="darkred")
        #
        headerFrame.pack(side=TOP, fill=X, pady=10)
    def operating(self):
        global lastClickStartTime, lastSelectTime,deviceController
        if deviceController.deviceAutoRun == 0:
            deviceController.deviceAutoRun = 1
            lastClickStartTime = datetime.now()
            # 
            deviceController.threadDate = datetime.now()
            self.operationButton.configure(
                background="green", text="关闭设备", activebackground="darkgreen")
            self.mainThread = threading.Thread(
                target=operatingAllStep, args=(deviceController.threadDate,))
            self.mainThread.start()
            # self.funcCancel = funcCancel
            # if hasattr(self, 'thread') and self.thread and self.thread.is_alive():
            #     if funcCancel == self.funcCancel:
            #         self.thread.raise_exception()
            #         time.sleep(0.2)
            #         self.funcCancel()
            #         self.thread = None
            #         # print("stop thread")
            #         slectItem.configure(background="", text=slectItemText)
            #         return
            #     else:
            #         if messagebox.askokcancel("更换步骤", "确定终止未完成步骤,并开始新的步骤吗?"):
            #             return
            #         else:
            #             return
            # self.thread = thread_with_exception(func)
            # self.thread.start()
            # self.funcCancel = funcCancel
        else:
            deviceController.deviceAutoRun = 0
            lastClickStartTime = lastSelectTime
            self.operationButton.configure(
                background="red", text="开启设备", activebackground="darkred")
            # if hasattr(self, 'mainThread') and self.mainThread and self.mainThread.is_alive():
                # self.mainThread.raise_exception()
                # print("stop mainThread")
            deviceController.threadDate = datetime.now()
            operatingAllStepCancel()
            self.refreshPage()
        return
    def refreshPage(self):
        if deviceController.deviceAutoRun == 0:
            self.operationButton.configure(
                background="red", text="开启设备", activebackground="darkred")
        else:
            self.operationButton.configure(
                background="green", text="关闭设备", activebackground="darkgreen")
        lastHistory = list(dbGetLastFloatNineParametersHistory())
        if len(lastHistory) == 1:
            lastHistory = lastHistory[0]
            self.mainHistoryText.set(
                "设备名称:"+deviceName+"\n" +
                "设备ID:"+''.join(map(intToHex, addrsID))+"\n" +
                "做样时间:"+lastHistory['time'].strftime("%Y-%m-%d %H:%M:%S")+"\n" +
                "PH:"+str(round(lastHistory['PH'], 3))+"\n" +
                "温度:"+str(round(lastHistory['temp'], 2))+"°C\n" +
                "电导率:"+str(round(lastHistory['ele'], 3))+"uS/cm\n" +
                "浊度:"+str(round(lastHistory['tur'], 3))+"NTU\n" +
                "溶解氧:"+str(round(lastHistory['O2'], 3))+"mg/L\n" +
                "COD:"+str(round(lastHistory['COD'], 3))+"mg/L\n" +
                "氨氮:"+str(round(lastHistory['NH3'], 3))+"mg/L\n" +
                "硝氮:"+str(round(lastHistory['NO3'], 3))+"mg/L\n" +
                "叶绿素:"+str(round(lastHistory['chl'], 3))+"ug/L\n" +
                "位置:"+lastHistory['dataInfo']+"\n" +
                "仪器状态:"+stepString(deviceController.deviceAutoRun, deviceController.deviceStep)+"\n" +
                "报警状态:"+stateString(deviceInfo.warningInfo))
        else:
            self.mainHistoryText.set(
                "设备名称:"+deviceName+"\n" +
                "设备ID:"+''.join(map(intToHex, addrsID))+"\n" +
                """做样时间:
PH:
温度:
电导率:
浊度:
溶解氧:
COD:
氨氮:
硝氮:
叶绿素:
位置:
仪器状态:"""+stepString(deviceController.deviceAutoRun, deviceController.deviceStep)+"\n" +
                "报警状态:"+stateString(deviceInfo.warningInfo))
        # self.lastSelectOperationButton = operationButton
        #
        return
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())


# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)

