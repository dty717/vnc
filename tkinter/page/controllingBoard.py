from tkinter import *
from tkinter import ttk
from components.groupLabelButton import GroupLabelButton
from components.labelButton import SwitchLabelButton
from PIL import Image
from config.config import *
from service.device import write_single_register,DeviceAddr,deviceInfo,deviceController

class ControllingBoard(Frame):
    def __init__(self, master,imgDicts,**kargs):
        super().__init__(master,kargs)
        global deviceController
        #
        #pumpLabelGroup
        #
        pumpLabelGroup = GroupLabelButton(self,title = "手动进样")
        pumpLabelGroup.pack()
        switchSamplePump = SwitchLabelButton(pumpLabelGroup,imgDicts,text = "手动进水样" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.samplePumpAddr.value,1, lambda rec:setattr(deviceController,'samplePump',1) or switchSamplePump.open(), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.samplePumpAddr.value,0, lambda rec:setattr(deviceController,'samplePump',0)or switchSamplePump.close(), repeatTimes = 0 , needMesBox = True),
        )
        switchSamplePump.pack()
        switchConcentration1Pump = SwitchLabelButton(pumpLabelGroup,imgDicts,text = "手动进标一" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.concentration1PumpAddr.value,1, lambda rec:setattr(deviceController,'concentration1Pump',1) or switchConcentration1Pump.open(), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.concentration1PumpAddr.value,0, lambda rec:setattr(deviceController,'concentration1Pump',0)or switchConcentration1Pump.close(), repeatTimes = 0 , needMesBox = True),
        )
        switchConcentration1Pump.pack()
        switchConcentration2Pump = SwitchLabelButton(pumpLabelGroup,imgDicts,text = "手动进标二" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.concentration2PumpAddr.value,1, lambda rec:setattr(deviceController,'concentration2Pump',1) or switchConcentration2Pump.open(), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.concentration2PumpAddr.value,0, lambda rec:setattr(deviceController,'concentration2Pump',0)or switchConcentration2Pump.close(), repeatTimes = 0 , needMesBox = True),
        )
        switchConcentration2Pump.pack()
        switchConcentration3Pump = SwitchLabelButton(pumpLabelGroup,imgDicts,text = "手动进标三" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.concentration3PumpAddr.value,1, lambda rec:setattr(deviceController,'concentration3Pump',1) or switchConcentration3Pump.open(), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.concentration3PumpAddr.value,0, lambda rec:setattr(deviceController,'concentration3Pump',0)or switchConcentration3Pump.close(), repeatTimes = 0 , needMesBox = True),
        )
        switchConcentration3Pump.pack()
        switchChemical1Pump = SwitchLabelButton(pumpLabelGroup,imgDicts,text = "手动进试剂一" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.chemical1PumpAddr.value,1, lambda rec:setattr(deviceController,'chemical1Pump',1) or switchChemical1Pump.open(), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.chemical1PumpAddr.value,0, lambda rec:setattr(deviceController,'chemical1Pump',0)or switchChemical1Pump.close(), repeatTimes = 0 , needMesBox = True),
        )
        switchChemical1Pump.pack()
        switchChemical2Pump = SwitchLabelButton(pumpLabelGroup,imgDicts,text = "手动进试剂二" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.chemical2PumpAddr.value,1, lambda rec:setattr(deviceController,'chemical2Pump',1) or switchChemical2Pump.open(), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.chemical2PumpAddr.value,0, lambda rec:setattr(deviceController,'chemical2Pump',0)or switchChemical2Pump.close(), repeatTimes = 0 , needMesBox = True),
        )
        switchChemical2Pump.pack()
        switchChemical3Pump = SwitchLabelButton(pumpLabelGroup,imgDicts,text = "手动进试剂三" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.chemical3PumpAddr.value,1, lambda rec:setattr(deviceController,'chemical3Pump',1) or switchChemical3Pump.open(), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.chemical3PumpAddr.value,0, lambda rec:setattr(deviceController,'chemical3Pump',0)or switchChemical3Pump.close(), repeatTimes = 0 , needMesBox = True),
        )
        #
        #cleanLabelGroup
        #
        cleanLabelGroup = GroupLabelButton(self,title = "手动清洗")
        cleanLabelGroup.pack(pady = 10)
        switchReactionTubeClean= SwitchLabelButton(cleanLabelGroup,imgDicts,text = "清洗消解池" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.reactionTubeCleanAddr.value,1, lambda rec:setattr(deviceController,'reactionTubeClean',1) or switchReactionTubeClean.open(), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.reactionTubeCleanAddr.value,0, lambda rec:setattr(deviceController,'reactionTubeClean',0)or switchReactionTubeClean.close(), repeatTimes = 0 , needMesBox = True),
        )
        switchReactionTubeClean.pack()
        switchSuctionClean = SwitchLabelButton(cleanLabelGroup,imgDicts,text = "清洗储液环" , 
            textYES = "启动" , clickYES = lambda :write_single_register(DeviceAddr.suctionCleanAddr.value,1, lambda rec:setattr(deviceController,'suctionClean',1) or switchSuctionClean.open(), repeatTimes = 0 , needMesBox = True),
            textNO = "停止" , clickNO = lambda :write_single_register(DeviceAddr.suctionCleanAddr.value,0, lambda rec:setattr(deviceController,'suctionClean',0)or switchSuctionClean.close(), repeatTimes = 0 , needMesBox = True),
        )
        switchSuctionClean.pack()
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())


# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)