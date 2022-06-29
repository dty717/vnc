from tkinter import *
from tkinter import ttk
from service.device import write_single_register,write_multiple_registers,DeviceAddr,deviceInfo,deviceController

backgroundColors = ["#ffffff","#1fa1af"]
class TimeSelectingBoard(Frame):
    def __init__(self, master,**kargs):
        super().__init__(master,kargs)
        global deviceController
        buttonFrame = Frame(self, bg = "#1fa1af")
        buttonFrame.pack(side="top",anchor=E ,pady = 20)
        button_select = Button(buttonFrame, text="全选",command = self.selectAll)
        button_select.pack(side="left")
        button_reset = Button(buttonFrame, text="重置",command = self.resetAll)
        button_reset.pack(side="left",padx = 10)
        # 
        # 24h
        #
        self.buttonHours = []
        button1_hour_Frame = Frame(self, bg = "#1fa1af")
        button1_hour_Frame.pack(side="top",anchor=E)
        for i in range(8):
            button_hour = Button(button1_hour_Frame,width=7, height=3, text=str(i),command = self.timeSelectClick(i))
            if deviceController.selectingHours[i] == 0:
                button_hour.configure(background=backgroundColors[0])
            else:
                button_hour.configure(background=backgroundColors[1])
            button_hour.pack(side="left")
            self.buttonHours.append(button_hour)
        button2_hour_Frame = Frame(self, bg = "#1fa1af")
        button2_hour_Frame.pack(side="top",anchor=E)
        for i in range(8,16):
            button_hour = Button(button2_hour_Frame,width=7, height=3, text=str(i),command = self.timeSelectClick(i))
            if deviceController.selectingHours[i] == 0:
                button_hour.configure(background=backgroundColors[0])
            else:
                button_hour.configure(background=backgroundColors[1])            
            button_hour.pack(side="left")
            self.buttonHours.append(button_hour)
        button3_hour_Frame = Frame(self, bg = "#1fa1af")
        button3_hour_Frame.pack(side="top",anchor=E)
        for i in range(16,24):
            button_hour = Button(button3_hour_Frame,width=7, height=3, text=str(i),command = self.timeSelectClick(i))
            if deviceController.selectingHours[i] == 0:
                button_hour.configure(background=backgroundColors[0])
            else:
                button_hour.configure(background=backgroundColors[1])            
            button_hour.pack(side="left")
            self.buttonHours.append(button_hour)
    #
    # timeSelectClick
    #
    def timeSelectClick(self,index):
        global deviceController
        return lambda:write_single_register(DeviceAddr.selectingHoursAddr.value + index, int(not deviceController.selectingHours[index]), 
                lambda rec:self.buttonHours[index].configure(background=backgroundColors[int(not deviceController.selectingHours[index])]) 
                    or deviceController.selectingHours.__setitem__(index,int(not deviceController.selectingHours[index])) , repeatTimes = 0 , needMesBox = True)
    def selectAll(self):
        write_multiple_registers(DeviceAddr.selectingHoursAddr.value, [1 for i in range(24)], 
                lambda rec:[self.buttonHours[index].configure(background=backgroundColors[1]) for index in range(24) ] 
                    and setattr(deviceController,'selectingHours',[1 for i in range(24)]) , repeatTimes = 0 , needMesBox = True)
        # 
        return
    def resetAll(self):
        write_multiple_registers(DeviceAddr.selectingHoursAddr.value, [0 for i in range(24)], 
                lambda rec:[self.buttonHours[index].configure(background=backgroundColors[0]) for index in range(24) ] 
                    and setattr(deviceController,'selectingHours',[0 for i in range(24)]) , repeatTimes = 0 , needMesBox = True)
        return
        # lambda : print(self.buttonHours[index])
        # 
        # lambda :write_single_register(DeviceAddr.reactionTubeCleanAddr.value,1, lambda rec:setattr(deviceController,'reactionTubeClean',1) or switchReactionTubeClean.open(), repeatTimes = 0 , needMesBox = True),

# mianBoard = Frame(tabNoteBook, width=100, height=100, bg = "#1fa1af"))
# mianBoard.pack(fill=BOTH, expand=1)
