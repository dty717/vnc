from tkinter import *
from tkinter import ttk
from components.groupLabelButton import GroupLabelButton
from components.labelButton import SwitchLabelButton
from PIL import Image
from config.config import *
from service.device import write_single_register, DeviceAddr, deviceInfo, deviceController


class ControllingBoard(Frame):
    def __init__(self, master, imgDicts, **kargs):
        super().__init__(master, kargs)
        global deviceController
        #
        #pumpLabelGroup
        #
        pumpLabelGroup = GroupLabelButton(self, title="手动进样")
        pumpLabelGroup.pack(pady=30)
        self.switchSamplePump = SwitchLabelButton(pumpLabelGroup, imgDicts, text="手动进水样",
                                                  textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.samplePumpAddr.value, lambda rec: setattr(deviceController, 'samplePump', 1) or self.switchSamplePump.open(), repeatTimes=0, needMesBox=True),
                                                  textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'samplePump', 0) or self.switchSamplePump.close(), repeatTimes=0, needMesBox=True),
                                                  )
        if deviceController.samplePump == 1:
            self.switchSamplePump.open()
        else:
            self.switchSamplePump.close()
        self.switchSamplePump.pack(pady=5)
        self.switchConcentration1Pump = SwitchLabelButton(pumpLabelGroup, imgDicts, text="手动进标一",
                                                          textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.concentration1PumpAddr.value, lambda rec: setattr(deviceController, 'concentration1Pump', 1) or self.switchConcentration1Pump.open(), repeatTimes=0, needMesBox=True),
                                                          textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'concentration1Pump', 0) or self.switchConcentration1Pump.close(), repeatTimes=0, needMesBox=True),
                                                          )
        if deviceController.concentration1Pump == 1:
            self.switchConcentration1Pump.open()
        else:
            self.switchConcentration1Pump.close()
        self.switchConcentration1Pump.pack(pady=5)
        self.switchConcentration2Pump = SwitchLabelButton(pumpLabelGroup, imgDicts, text="手动进标二",
                                                          textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.concentration2PumpAddr.value, lambda rec: setattr(deviceController, 'concentration2Pump', 1) or self.switchConcentration2Pump.open(), repeatTimes=0, needMesBox=True),
                                                          textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'concentration2Pump', 0) or self.switchConcentration2Pump.close(), repeatTimes=0, needMesBox=True),
                                                          )
        if deviceController.concentration2Pump == 1:
            self.switchConcentration2Pump.open()
        else:
            self.switchConcentration2Pump.close()
        self.switchConcentration2Pump.pack(pady=5)
        self.switchConcentration3Pump = SwitchLabelButton(pumpLabelGroup, imgDicts, text="手动进标三",
                                                          textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.concentration3PumpAddr.value, lambda rec: setattr(deviceController, 'concentration3Pump', 1) or self.switchConcentration3Pump.open(), repeatTimes=0, needMesBox=True),
                                                          textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'concentration3Pump', 0) or self.switchConcentration3Pump.close(), repeatTimes=0, needMesBox=True),
                                                          )
        if deviceController.concentration3Pump == 1:
            self.switchConcentration3Pump.open()
        else:
            self.switchConcentration3Pump.close()
        self.switchConcentration3Pump.pack(pady=5)
        self.switchChemical1Pump = SwitchLabelButton(pumpLabelGroup, imgDicts, text="手动进试剂一",
                                                     textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.chemical1PumpAddr.value, lambda rec: setattr(deviceController, 'chemical1Pump', 1) or self.switchChemical1Pump.open(), repeatTimes=0, needMesBox=True),
                                                     textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'chemical1Pump', 0) or self.switchChemical1Pump.close(), repeatTimes=0, needMesBox=True),
                                                     )
        if deviceController.chemical1Pump == 1:
            self.switchChemical1Pump.open()
        else:
            self.switchChemical1Pump.close()
        self.switchChemical1Pump.pack(pady=5)
        self.switchChemical2Pump = SwitchLabelButton(pumpLabelGroup, imgDicts, text="手动进试剂二",
                                                     textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.chemical2PumpAddr.value, lambda rec: setattr(deviceController, 'chemical2Pump', 1) or self.switchChemical2Pump.open(), repeatTimes=0, needMesBox=True),
                                                     textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'chemical2Pump', 0) or self.switchChemical2Pump.close(), repeatTimes=0, needMesBox=True),
                                                     )
        if deviceController.chemical2Pump == 1:
            self.switchChemical2Pump.open()
        else:
            self.switchChemical2Pump.close()
        self.switchChemical2Pump.pack(pady=5)
        self.switchChemical3Pump = SwitchLabelButton(pumpLabelGroup, imgDicts, text="手动进试剂三",
                                                     textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.chemical3PumpAddr.value, lambda rec: setattr(deviceController, 'chemical3Pump', 1) or self.switchChemical3Pump.open(), repeatTimes=0, needMesBox=True),
                                                     textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'chemical3Pump', 0) or self.switchChemical3Pump.close(), repeatTimes=0, needMesBox=True),
                                                     )
        if deviceController.chemical3Pump == 1:
            self.switchChemical3Pump.open()
        else:
            self.switchChemical3Pump.close()
        self.switchChemical3Pump.pack(pady=5)
        #
        #cleanLabelGroup
        #
        cleanLabelGroup = GroupLabelButton(self, title="手动清洗")
        cleanLabelGroup.pack(pady=10)
        self.switchReactionTubeClean = SwitchLabelButton(cleanLabelGroup, imgDicts, text="一键排空",
                                                         textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.reactionTubeEmptyAddr.value, lambda rec: setattr(deviceController, 'reactionTubeClean', 1) or self.switchReactionTubeClean.open(), repeatTimes=0, needMesBox=True),
                                                         textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'reactionTubeClean', 0) or self.switchReactionTubeClean.close(), repeatTimes=0, needMesBox=True),
                                                         )
        if deviceController.reactionTubeClean == 1:
            self.switchReactionTubeClean.open()
        else:
            self.switchReactionTubeClean.close()
        self.switchReactionTubeClean.pack(pady=5)


        self.switchPumpInWater = SwitchLabelButton(cleanLabelGroup, imgDicts, text="手动进蒸馏水",
                                                    textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.pumpInWaterAddr.value, lambda rec: setattr(deviceController, 'pumpInWater', 1) or self.switchPumpInWater.open(), repeatTimes=0, needMesBox=True),
                                                    textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'pumpInWater', 0) or self.switchSuctionClean.close(), repeatTimes=0, needMesBox=True),
                                                    )
        if deviceController.pumpInWater == 1:
            self.switchPumpInWater.open()
        else:
            self.switchPumpInWater.close()
        self.switchPumpInWater.pack(pady=5)

        self.switchSuctionClean = SwitchLabelButton(cleanLabelGroup, imgDicts, text="清洗储液环",
                                                    textYES="启动", clickYES=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, DeviceAddr.suctionCleanAddr.value, lambda rec: setattr(deviceController, 'suctionClean', 1) or self.switchSuctionClean.open(), repeatTimes=0, needMesBox=True),
                                                    textNO="停止", clickNO=lambda: write_single_register(DeviceAddr.pumpSelectAddr.value, 0, lambda rec: setattr(deviceController, 'suctionClean', 0) or self.switchSuctionClean.close(), repeatTimes=0, needMesBox=True),
                                                    )
        if deviceController.suctionClean == 1:
            self.switchSuctionClean.open()
        else:
            self.switchSuctionClean.close()
        self.switchSuctionClean.pack(pady=5)

    def refreshPage(self):
        global deviceController
        if deviceController.samplePump == 1:
            self.switchSamplePump.open()
        else:
            self.switchSamplePump.close()
        if deviceController.concentration1Pump == 1:
            self.switchConcentration1Pump.open()
        else:
            self.switchConcentration1Pump.close()
        if deviceController.concentration2Pump == 1:
            self.switchConcentration2Pump.open()
        else:
            self.switchConcentration2Pump.close()
        if deviceController.concentration3Pump == 1:
            self.switchConcentration3Pump.open()
        else:
            self.switchConcentration3Pump.close()
        if deviceController.chemical1Pump == 1:
            self.switchChemical1Pump.open()
        else:
            self.switchChemical1Pump.close()
        if deviceController.chemical2Pump == 1:
            self.switchChemical2Pump.open()
        else:
            self.switchChemical2Pump.close()
        if deviceController.chemical3Pump == 1:
            self.switchChemical3Pump.open()
        else:
            self.switchChemical3Pump.close()
        if deviceController.reactionTubeClean == 1:
            self.switchReactionTubeClean.open()
        else:
            self.switchReactionTubeClean.close()
        if deviceController.suctionClean == 1:
            self.switchSuctionClean.open()
        else:
            self.switchSuctionClean.close()
        return
    # def print_contents(self, event):
    #     print("Hi. The current entry content is:",
    #           self.contents.get())

# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)
