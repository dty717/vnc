from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from components.groupLabelButton import GroupLabelButton
from components.labelButton import LabelTextButton, SwitchLabelButton
from PIL import Image
from config.config import *
from service.device import deviceController

class SettingBoard(Frame):
    def __init__(self, master, imgDicts, **kargs):
        super().__init__(master, kargs)
        #
        #fiveParametersSettingGroup
        #
        fiveParametersSettingGroup = GroupLabelButton(self, title="参数设置")
        fiveParametersSettingGroup.pack(pady=20)
        self.motorInitPWMLabelText = LabelTextButton(fiveParametersSettingGroup, text="电机初始PWM",
                                                         command=lambda content: self.setControllerValue("motorInitPWM", content))
        self.motorInitPWMLabelText.setText(
            deviceController.motorInitPWM)
        self.motorInitPWMLabelText.pack(anchor=W, pady=5)
        self.motorDownPWMLabelText = LabelTextButton(fiveParametersSettingGroup, text="电机向下PWM",
                                                          command=lambda content: self.setControllerValue("motorDownPWM", content))
        self.motorDownPWMLabelText.setText(
            deviceController.motorDownPWM)
        self.motorDownPWMLabelText.pack(anchor=W, pady=5)
        self.motorStopPWMLabelText = LabelTextButton(fiveParametersSettingGroup, text="电机静止PWM",
                                                         command=lambda content: self.setControllerValue("motorStopPWM", content))
        self.motorStopPWMLabelText.setText(
            deviceController.motorStopPWM)
        self.motorStopPWMLabelText.pack(anchor=W, pady=5)
        self.motorUpPWMLabelText = LabelTextButton(fiveParametersSettingGroup, text="电机向上PWM",
                                                         command=lambda content: self.setControllerValue("motorUpPWM", content))
        self.motorUpPWMLabelText.setText(
            deviceController.motorUpPWM)
        self.motorUpPWMLabelText.pack(anchor=W, pady=5)
        self.probePowerWaitingTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="电机启动等待时间",
                                                          command=lambda content: self.setControllerValue("probePowerWaitingTime", content))
        self.probePowerWaitingTimeLabelText.setText(
            deviceController.probePowerWaitingTime)
        self.probePowerWaitingTimeLabelText.pack(anchor=W, pady=5)
        self.motorInitTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="电机初始等待时间",
                                                           command=lambda content: self.setControllerValue("motorInitTime", content))
        self.motorInitTimeLabelText.setText(
            deviceController.motorInitTime)
        self.motorInitTimeLabelText.pack(anchor=W, pady=5)
        self.pumpSampleInTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="取水样时间",
                                                          command=lambda content: self.setControllerValue("pumpSampleInTime", content))
        self.pumpSampleInTimeLabelText.setText(
            deviceController.pumpSampleInTime)
        self.pumpSampleInTimeLabelText.pack(anchor=W, pady=5)
        self.motorDownTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="下降时间",
                                                         command=lambda content: self.setControllerValue("motorDownTime", content))
        self.motorDownTimeLabelText.setText(
            deviceController.motorDownTime)
        self.motorDownTimeLabelText.pack(anchor=W, pady=5)
        self.motorUpTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="上拉时间",
                                                        command=lambda content: self.setControllerValue("motorUpTime", content))
        self.motorUpTimeLabelText.setText(deviceController.motorUpTime)
        self.motorUpTimeLabelText.pack(anchor=W, pady=5)
        self.probeWaitingTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="等待读取时间",
                                                      command=lambda content: self.setControllerValue("probeWaitingTime", content))
        self.probeWaitingTimeLabelText.setText(deviceController.probeWaitingTime)
        self.probeWaitingTimeLabelText.pack(anchor=W, pady=5)
    def setControllerValue(self, attr, content):
        setattr(deviceController, attr, float(content))
        messagebox.showinfo("设置", "设置成功")
        return
    def refreshPage(self):
        self.motorInitPWMLabelText.setText(deviceController.motorInitPWM)
        self.motorDownPWMLabelText.setText(deviceController.motorDownPWM)
        self.motorStopPWMLabelText.setText(deviceController.motorStopPWM)
        self.motorUpPWMLabelText.setText(deviceController.motorUpPWM)
        self.probePowerWaitingTimeLabelText.setText(deviceController.probePowerWaitingTime)
        self.motorInitTimeLabelText.setText(deviceController.motorInitTime)
        self.pumpSampleInTimeLabelText.setText(deviceController.pumpSampleInTime)
        self.motorDownTimeLabelText.setText(deviceController.motorDownTime)
        self.motorUpTimeLabelText.setText(deviceController.motorUpTime)
        self.probeWaitingTimeLabelText.setText(deviceController.probeWaitingTime)
        return
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())


# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)
