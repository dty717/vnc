from tkinter import *
from tkinter import ttk
from components.groupLabelButton import GroupLabelButton
from components.labelButton import SwitchLabelButton
from PIL import Image
from config.config import *
from service.device import write_single_register,DeviceAddr,deviceInfo,deviceController
import os
class ControllingBoard(Frame):
    def __init__(self, master,imgDicts,**kargs):
        super().__init__(master,kargs)
        global deviceController
        # 
        #groupLabelButton1
        #  
        pumpLabelGroup = GroupLabelButton(self)
        pumpLabelGroup.pack()
        switchLabelPumpSampleButton = SwitchLabelButton(pumpLabelGroup,imgDicts,text = "手动进水样" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.samplePumpAddr.value,1, lambda rec:setattr(deviceController,'samplePump',1), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.samplePumpAddr.value,0, lambda rec:setattr(deviceController,'samplePump',0), repeatTimes = 0 , needMesBox = True),
        )

        switchLabelPumpSampleButton.pack()
        switchLabelButton11 = SwitchLabelButton(pumpLabelGroup,imgDicts)
        switchLabelButton11.pack()
        switchLabelButton12 = SwitchLabelButton(pumpLabelGroup,imgDicts)
        switchLabelButton12.pack()
        switchLabelButton13 = SwitchLabelButton(pumpLabelGroup,imgDicts)
        switchLabelButton13.pack()
        # 
        #groupLabelButton2
        #  
        # groupLabelButton2 = GroupLabelButton(self)
        # groupLabelButton2.pack(side="left", fill="x")
        # switchLabelButton20 = SwitchLabelButton(groupLabelButton2,imgDicts)
        # switchLabelButton20.pack()
        # switchLabelButton21 = SwitchLabelButton(groupLabelButton2,imgDicts)
        # switchLabelButton21.pack()
        # switchLabelButton22 = SwitchLabelButton(groupLabelButton2,imgDicts)
        # switchLabelButton22.pack()
        # switchLabelButton23 = SwitchLabelButton(groupLabelButton2,imgDicts)
        # switchLabelButton23.pack()
        # label2 = Label(self,image=imgDicts["redSignal"])
        # label2.pack()
        # self.pack()
        # self.entrythingy = Entry()
        # self.entrythingy.pack()
        # # Create the application variable.
        # self.contents = StringVar()
        # # Set it to some value.
        # self.contents.set("this is a variable")
        # # Tell the entry widget to watch this variable.
        # self.entrythingy["textvariable"] = self.contents
        # # Define a callback for when the user hits return.
        # # It prints the current value of the variable.
        # self.entrythingy.bind('<Key-Return>',
        #                      self.print_contents)
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())


# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)