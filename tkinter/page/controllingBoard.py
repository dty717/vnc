import time
from tkinter import *
from tkinter import ttk
import threading
from datetime import datetime
from tkinter import messagebox
from PIL import Image

from components.groupLabelButton import GroupLabelButton
from components.labelButton import SwitchLabelButton
from config.config import *
from service.device import write_single_register, DeviceAddr, deviceController, \
    probeRelay, \
    readProbe, readProbeCancel

class ControllingBoard(Frame):
    def __init__(self, master, imgDicts, **kargs):
        super().__init__(master, kargs)
        global deviceController
        # self.thread.is_alive = False
        #
        #modelSelectGroup
        #
        modelSelectGroup = GroupLabelButton(self, title="手动步骤")
        modelSelectGroup.pack(pady=30)
        # Line1
        modelSelectGroupLine1 = Frame(modelSelectGroup, bg=primaryColor)
        # self.selectOperateButton = Button(
        #     modelSelectGroupLine1, text="排空清水", command=self.testFun, font=(None, 12))
        # self.selectOperateButton.pack(side="left", padx=10, pady=10)
        self.selectHourButton = Button(
            modelSelectGroupLine1, text="读取数据", command=lambda: self.handleThread(readProbe, readProbeCancel,self.selectHourButton,"读取数据","停止读取"), font=(None, 12))
        self.selectHourButton.pack(side="left", padx=10, pady=10)
        modelSelectGroupLine1.pack(fill=X)
        # Line2
        modelSelectGroupLine2 = Frame(modelSelectGroup, bg=primaryColor)
        # 
        modelSelectGroupLine2.pack(fill=X)
        #
        #cleanLabelGroup
        #
        cleanLabelGroup = GroupLabelButton(self, title="手动控制")
        cleanLabelGroup.pack(pady=10)
        self.switchFiveParametersProbe = SwitchLabelButton(cleanLabelGroup, imgDicts, text="五参探头",
                                                     textYES="启动", clickYES=lambda: self.checkIfAutoRun() and (probeRelay.on() or self.switchFiveParametersProbe.open()),
                                                     textNO="停止", clickNO=lambda: self.checkIfAutoRun() and (probeRelay.off() or self.switchFiveParametersProbe.close()),
                                                     )
        if probeRelay.value == 1:
            self.switchFiveParametersProbe.open()
        else:
            self.switchFiveParametersProbe.close()
        self.switchFiveParametersProbe.pack(pady=5)
    def checkIfAutoRun(self):
        if deviceController.deviceAutoRun:
            messagebox.showerror("设备繁忙","设备正在自动做样,请等待做样结束或者停止自动做样,否则无法手动控制")
            return False
        else:
            if deviceController.deviceStep:
                messagebox.showerror("设备繁忙","设备正在手动做样,请等待做样结束或者停止手动做样,否则无法手动控制")
                return False
            else:
                return True
    def handleThread(self, func, funcCancel,slectItem,slectItemText,cancelItemText):
        global lastSelectItem, deviceController
        if deviceController.deviceAutoRun:
            messagebox.showerror("设备繁忙","设备正在自动做样,请等待做样结束或者停止自动做样,否则无法手动做样")
            return
        # if power.value == 0:
        #     power.on()
        #     if power.value == 1:
        #         lastClickStartTime = datetime.now()
        #         self.powerButton.configure(
        #             background="green", text="关闭设备", activebackground="darkgreen")
        # else:
        #     power.off()
        #     if power.value == 0:
        #         lastClickStartTime = lastSelectTime
        #         self.powerButton.configure(
        #             background="red", text="开启设备", activebackground="darkred")
        # return
        if hasattr(self, 'thread') and self.thread and self.thread.is_alive():
            if funcCancel == self.funcCancel:
                # self.thread.raise_exception()
                time.sleep(0.2)
                self.funcCancel()
                self.thread = None
                # print("stop thread")
                slectItem.configure(background="#d9d9d9", text=slectItemText, fg="black", activebackground="#ececec")
                # slectItem.configure(background="", text=slectItemText)
                return
            else:
                if messagebox.askokcancel("更换步骤", "确定终止未完成步骤,并开始新的步骤吗?"):
                    return
                else:
                    return
        slectItem.configure(background="green", text=cancelItemText, fg="white", activebackground="darkgreen")
        deviceController.threadDate = datetime.now()
        self.thread = threading.Thread(target=lambda date: func(date) or setattr(deviceController, 'deviceAutoRun', 0) or setattr(deviceController, 'deviceStep', 0) 
            or slectItem.configure(background="#d9d9d9", text=slectItemText, fg="black", activebackground="#ececec") , args=(deviceController.threadDate,))
        self.thread.start()
        self.funcCancel = funcCancel
        return
    def refreshPage(self):
        global deviceController
        if probeRelay.value == 1:
            self.switchFiveParametersProbe.open()
        else:
            self.switchFiveParametersProbe.close()
    def testFun(self):
        return
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())

# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)
