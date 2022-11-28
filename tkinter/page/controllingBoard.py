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
    probeRelay, ultravioletLedRelay, valveRelay, pumpSampleMotor, cleanWaterInMotor, cleanWaterOutMotor,\
    pumpWaterOut, pumpWaterOutCancel, pumpSampleIn, pumpSampleInCancel, readProbe, readProbeCancel, \
    pumpSampleOut, pumpSampleOutCancel, pumpWaterIn, pumpWaterInCancel, cleanTube, cleanTubeCancel
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
        self.selectOperateButton = Button(
            modelSelectGroupLine1, text="排空清水", command=lambda: self.handleThread(pumpWaterOut, pumpWaterOutCancel,self.selectOperateButton,"排空清水","停止排空"), font=(None, 12))
        self.selectOperateButton.pack(side="left", padx=10, pady=10)
        self.selectIntervalButton = Button(
            modelSelectGroupLine1, text="采集水样", command=lambda: self.handleThread(pumpSampleIn, pumpSampleInCancel,self.selectIntervalButton,"采集水样","停止采集"), font=(None, 12))
        self.selectIntervalButton.pack(side="left", padx=10, pady=10)
        self.selectHourButton = Button(
            modelSelectGroupLine1, text="读取数据", command=lambda: self.handleThread(readProbe, readProbeCancel,self.selectHourButton,"读取数据","停止读取"), font=(None, 12))
        self.selectHourButton.pack(side="left", padx=10, pady=10)
        modelSelectGroupLine1.pack(fill=X)
        # Line2
        modelSelectGroupLine2 = Frame(modelSelectGroup, bg=primaryColor)
        self.selectCalibrateButton = Button(
            modelSelectGroupLine2, text="排空水样", command=lambda: self.handleThread(pumpSampleOut, pumpSampleOutCancel,self.selectCalibrateButton,"排空水样","停止排空"), font=(None, 12))
        self.selectCalibrateButton.pack(side="left", padx=10, pady=10)
        self.selectPumpButton = Button(
            modelSelectGroupLine2, text="填充清水", command=lambda: self.handleThread(pumpWaterIn, pumpWaterInCancel,self.selectPumpButton,"填充清水","停止填充"), font=(None, 12))
        self.selectPumpButton.pack(side="left", padx=10, pady=10)
        self.selectIdleButton = Button(
            modelSelectGroupLine2, text="清洗滤膜", command=lambda: self.handleThread(cleanTube, cleanTubeCancel,self.selectIdleButton,"清洗滤膜","停止清洗"), font=(None, 12))
        self.selectIdleButton.pack(side="left", padx=10, pady=10)
        modelSelectGroupLine2.pack(fill=X)
        #
        #cleanLabelGroup
        #
        cleanLabelGroup = GroupLabelButton(self, title="手动控制")
        cleanLabelGroup.pack(pady=10)
        self.switchPumpSampleIn = SwitchLabelButton(cleanLabelGroup, imgDicts, text="取水样",
                                                    textYES="启动", clickYES=lambda: self.checkIfAutoRun() and (pumpSampleMotor.forward(deviceController.pumpSampleInSpeed) or self.switchPumpSampleIn.open() or self.switchPumpSampleOut.close()),
                                                    textNO="停止", clickNO=lambda: self.checkIfAutoRun() and (pumpSampleMotor.stop() or self.switchPumpSampleIn.close()  or self.switchPumpSampleOut.close()),
                                                    )
        if pumpSampleMotor.value > 0:
            self.switchPumpSampleIn.open()
        else:
            self.switchPumpSampleIn.close()
        self.switchPumpSampleIn.pack(pady=5)
        self.switchPumpSampleOut = SwitchLabelButton(cleanLabelGroup, imgDicts, text="排水样",
                                               textYES="启动", clickYES=lambda: self.checkIfAutoRun() and (pumpSampleMotor.backward(deviceController.pumpSampleOutSpeed) or self.switchPumpSampleOut.open() or self.switchPumpSampleIn.close()),
                                               textNO="停止", clickNO=lambda: self.checkIfAutoRun() and (pumpSampleMotor.stop() or self.switchPumpSampleOut.close()  or self.switchPumpSampleIn.close()),
                                               )
        if pumpSampleMotor.value < 0:
            self.switchPumpSampleOut.open()
        else:
            self.switchPumpSampleOut.close()
        self.switchPumpSampleOut.pack(pady=5)
        self.switchPumpWaterIn = SwitchLabelButton(cleanLabelGroup, imgDicts, text="取清水",
                                             textYES="启动", clickYES=lambda: self.checkIfAutoRun() and (cleanWaterInMotor.forward(deviceController.pumpWaterInSpeed) or self.switchPumpWaterIn.open()),
                                             textNO="停止", clickNO=lambda: self.checkIfAutoRun() and (cleanWaterInMotor.stop() or self.switchPumpWaterIn.close()),
                                             )
        if cleanWaterInMotor.value > 0 :
            self.switchPumpWaterIn.open()
        else:
            self.switchPumpWaterIn.close()
        self.switchPumpWaterIn.pack(pady=5)
        self.switchPumpWaterOut = SwitchLabelButton(cleanLabelGroup, imgDicts, text="排清水",
                                                     textYES="启动", clickYES=lambda: self.checkIfAutoRun() and (cleanWaterOutMotor.forward(deviceController.pumpWaterOutSpeed) or self.switchPumpWaterOut.open()),
                                                     textNO="停止", clickNO=lambda: self.checkIfAutoRun() and (cleanWaterOutMotor.stop() or self.switchPumpWaterOut.close()),
                                                     )
        if cleanWaterOutMotor.value > 0:
            self.switchPumpWaterOut.open()
        else:
            self.switchPumpWaterOut.close()
        self.switchPumpWaterOut.pack(pady=5)
        self.switchFiveParametersProbe = SwitchLabelButton(cleanLabelGroup, imgDicts, text="五参探头",
                                                     textYES="启动", clickYES=lambda: self.checkIfAutoRun() and (probeRelay.on() or self.switchFiveParametersProbe.open()),
                                                     textNO="停止", clickNO=lambda: self.checkIfAutoRun() and (probeRelay.off() or self.switchFiveParametersProbe.close()),
                                                     )
        if probeRelay.value == 1:
            self.switchFiveParametersProbe.open()
        else:
            self.switchFiveParametersProbe.close()
        self.switchFiveParametersProbe.pack(pady=5)
        self.switchUltravioletLed = SwitchLabelButton(cleanLabelGroup, imgDicts, text="紫外灯",
                                                     textYES="启动", clickYES=lambda: self.checkIfAutoRun() and (ultravioletLedRelay.on() or self.switchUltravioletLed.open()),
                                                     textNO="停止", clickNO=lambda: self.checkIfAutoRun() and (ultravioletLedRelay.off() or self.switchUltravioletLed.close()),
                                                     )
        if ultravioletLedRelay.value == 1:
            self.switchUltravioletLed.open()
        else:
            self.switchUltravioletLed.close()
        self.switchUltravioletLed.pack(pady=5)
        self.switchValve = SwitchLabelButton(cleanLabelGroup, imgDicts, text="电磁阀",
                                                textYES="启动", clickYES=lambda: self.checkIfAutoRun() and (valveRelay.on() or self.switchValve.open()),
                                                textNO="停止", clickNO=lambda: self.checkIfAutoRun() and (valveRelay.off() or self.switchValve.close()),
                                                )
        if valveRelay.value == 1:
            self.switchValve.open()
        else:
            self.switchValve.close()
        self.switchValve.pack(pady=5)
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
        if pumpSampleMotor.value > 0:
            self.switchPumpSampleIn.open()
        else:
            self.switchPumpSampleIn.close()
        if pumpSampleMotor.value < 0:
            self.switchPumpSampleOut.open()
        else:
            self.switchPumpSampleOut.close()
        if cleanWaterInMotor.value > 0 :
            self.switchPumpWaterIn.open()
        else:
            self.switchPumpWaterIn.close()
        if cleanWaterOutMotor.value > 0:
            self.switchPumpWaterOut.open()
        else:
            self.switchPumpWaterOut.close()
        if probeRelay.value == 1:
            self.switchFiveParametersProbe.open()
        else:
            self.switchFiveParametersProbe.close()
        if ultravioletLedRelay.value == 1:
            self.switchUltravioletLed.open()
        else:
            self.switchUltravioletLed.close()
        if valveRelay.value == 1:
            self.switchValve.open()
        else:
            self.switchValve.close()
    def testFun(self):
        return
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())

# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)
