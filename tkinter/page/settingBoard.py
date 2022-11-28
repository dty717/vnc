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
        self.pumpWaterOutSpeedLabelText = LabelTextButton(fiveParametersSettingGroup, text="排空清水速度",
                                                          command=lambda content: self.setControllerValue("pumpWaterOutSpeed", content))
        self.pumpWaterOutSpeedLabelText.setText(
            deviceController.pumpWaterOutSpeed)
        self.pumpWaterOutSpeedLabelText.pack(anchor=W, pady=5)
        self.pumpWaterOutTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="排空清水时间",
                                                         command=lambda content: self.setControllerValue("pumpWaterOutTime", content))
        self.pumpWaterOutTimeLabelText.setText(
            deviceController.pumpWaterOutTime)
        self.pumpWaterOutTimeLabelText.pack(anchor=W, pady=5)
        self.pumpSampleInSpeedLabelText = LabelTextButton(fiveParametersSettingGroup, text="取水样速度",
                                                          command=lambda content: self.setControllerValue("pumpSampleInSpeed", content))
        self.pumpSampleInSpeedLabelText.setText(
            deviceController.pumpSampleInSpeed)
        self.pumpSampleInSpeedLabelText.pack(anchor=W, pady=5)
        self.pumpSampleInTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="取水样时间",
                                                         command=lambda content: self.setControllerValue("pumpSampleInTime", content))
        self.pumpSampleInTimeLabelText.setText(
            deviceController.pumpSampleInTime)
        self.pumpSampleInTimeLabelText.pack(anchor=W, pady=5)
        self.probeWaitingTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="等待读取时间",
                                                         command=lambda content: self.setControllerValue("probeWaitingTime", content))
        self.probeWaitingTimeLabelText.setText(
            deviceController.probeWaitingTime)
        self.probeWaitingTimeLabelText.pack(anchor=W, pady=5)
        self.pumpSampleOutSpeedLabelText = LabelTextButton(fiveParametersSettingGroup, text="排水样速度",
                                                           command=lambda content: self.setControllerValue("pumpSampleOutSpeed", content))
        self.pumpSampleOutSpeedLabelText.setText(
            deviceController.pumpSampleOutSpeed)
        self.pumpSampleOutSpeedLabelText.pack(anchor=W, pady=5)
        self.pumpSampleOutTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="排水样时间",
                                                          command=lambda content: self.setControllerValue("pumpSampleOutTime", content))
        self.pumpSampleOutTimeLabelText.setText(
            deviceController.pumpSampleOutTime)
        self.pumpSampleOutTimeLabelText.pack(anchor=W, pady=5)
        self.pumpWaterInSpeedLabelText = LabelTextButton(fiveParametersSettingGroup, text="填充清水速度",
                                                         command=lambda content: self.setControllerValue("pumpWaterInSpeed", content))
        self.pumpWaterInSpeedLabelText.setText(
            deviceController.pumpWaterInSpeed)
        self.pumpWaterInSpeedLabelText.pack(anchor=W, pady=5)
        self.pumpWaterInTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="填充清水时间",
                                                        command=lambda content: self.setControllerValue("pumpWaterInTime", content))
        self.pumpWaterInTimeLabelText.setText(deviceController.pumpWaterInTime)
        self.pumpWaterInTimeLabelText.pack(anchor=W, pady=5)
        self.cleanTubeInSpeedLabelText = LabelTextButton(fiveParametersSettingGroup, text="洗膜进水速度",
                                                         command=lambda content: self.setControllerValue("cleanTubeInSpeed", content))
        self.cleanTubeInSpeedLabelText.setText(
            deviceController.cleanTubeInSpeed)
        self.cleanTubeInSpeedLabelText.pack(anchor=W, pady=5)
        self.cleanTubeOutSpeedLabelText = LabelTextButton(fiveParametersSettingGroup, text="洗膜出水速度",
                                                          command=lambda content: self.setControllerValue("cleanTubeOutSpeed", content))
        self.cleanTubeOutSpeedLabelText.setText(
            deviceController.cleanTubeOutSpeed)
        self.cleanTubeOutSpeedLabelText.pack(anchor=W, pady=5)
        self.cleanTubeTimeLabelText = LabelTextButton(fiveParametersSettingGroup, text="洗膜时间",
                                                      command=lambda content: self.setControllerValue("cleanTubeTime", content))
        self.cleanTubeTimeLabelText.setText(deviceController.cleanTubeTime)
        self.cleanTubeTimeLabelText.pack(anchor=W, pady=5)
    def setControllerValue(self, attr, content):
        setattr(deviceController, attr, float(content))
        messagebox.showinfo("设置", "设置成功")
        return
    def refreshPage(self):
        self.pumpWaterOutSpeedLabelText.setText(deviceController.pumpWaterOutSpeed)
        self.pumpWaterOutTimeLabelText.setText(deviceController.pumpWaterOutTime)
        self.pumpSampleInSpeedLabelText.setText(deviceController.pumpSampleInSpeed)
        self.pumpSampleInTimeLabelText.setText(deviceController.pumpSampleInTime)
        self.probeWaitingTimeLabelText.setText(deviceController.probeWaitingTime)
        self.pumpSampleOutSpeedLabelText.setText(deviceController.pumpSampleOutSpeed)
        self.pumpSampleOutTimeLabelText.setText(deviceController.pumpSampleOutTime)
        self.pumpWaterInSpeedLabelText.setText(deviceController.pumpWaterInSpeed)
        self.pumpWaterInTimeLabelText.setText(deviceController.pumpWaterInTime)
        self.cleanTubeInSpeedLabelText.setText(deviceController.cleanTubeInSpeed)
        self.cleanTubeOutSpeedLabelText.setText(deviceController.cleanTubeOutSpeed)
        self.cleanTubeTimeLabelText.setText(deviceController.cleanTubeTime)
        return
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())


# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)
