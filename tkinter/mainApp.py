from tkinter import *
from tkinter import ttk
from PIL import Image
import time
import threading
import serial

from config.labelString import *
from config.config import *
from tool.crc import crc16,checkBuffer
from service.device import *
from page.mainBoard import MainBoard
from page.historyBoard import HistoryBoard
from page.controllingBoard import ControllingBoard
from page.timeSelectingBoard import TimeSelectingBoard
from page.settingBoard import SettingBoard
from page.systemLogBoard import SystemLogBoard

# Create the main window
root = Tk()
screenWidth = root.winfo_screenwidth()
screenHeightShift = 68
screenHeight = root.winfo_screenheight() - screenHeightShift

root.geometry("%dx%d+0+0" % (screenWidth, screenHeight))
root.title(titleLabel)
root.configure(background="#1fa1af")
styleConfig = ttk.Style()
# 'ne' as in compass direction
styleConfig.configure('TNotebook', tabposition='wn',background="blue")
styleConfig.configure('TNotebook.Tab',background="white", font=("Helvetica", 16))

images = (
    PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
    PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
    PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
)
styleConfig.element_create("close", "image", "img_close",
                           ("active", "pressed", "!disabled", "img_closepressed"),
                           ("active", "!disabled", "img_closeactive"), width = 130, padding = 30,sticky='')

styleConfig.layout("TNotebook", [
                   ("TNotebook.client", {"sticky": "nswe"})])
styleConfig.layout("TNotebook.Tab", [
    ("TNotebook.tab", {
        "sticky": "nswe",
        "children": [
            ("TNotebook.padding", {
                "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("TNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("TNotebook.label", {
                                     "side": "left", "sticky": ''}),
                                    ("TNotebook.close", {
                                     "side": "left", "sticky": ''}),
                                ]
                            })
                        ]
            })
        ]
    })
])

redSignal = PhotoImage(file = f"{sysPath}/assets/redSignal.png")
greenSignal = PhotoImage(file = f"{sysPath}/assets/greenSignal.png")

tabNoteBook = ttk.Notebook(root,width=screenWidth-300, height=screenHeight-50,padding = 10)
tabNoteBook.pack()

mainBoard = MainBoard(tabNoteBook,width=50, height=50, bg="red")
historyBoard = HistoryBoard(tabNoteBook, width=50, height=50, bg="yellow")
controllingBoard = ControllingBoard(tabNoteBook,{"greenSignal":greenSignal,"redSignal":redSignal}, width=50, height=50, bg="green")
timeSelectingBoard = TimeSelectingBoard(tabNoteBook, width=50, height=50, bg="blue")
settingBoard = SettingBoard(tabNoteBook, width=50, height=50, bg="black")
systemLogBoard = SystemLogBoard(tabNoteBook, width=50, height=50, bg="white")

tabNoteBook.add(mainBoard, text="主显示面")
tabNoteBook.add(historyBoard, text="历史数据")
tabNoteBook.add(controllingBoard, text="设备调试")
tabNoteBook.add(timeSelectingBoard, text="整点做样")
tabNoteBook.add(settingBoard, text="参数设置")
tabNoteBook.add(systemLogBoard, text="运行日志")

serName = '/dev/ttyUSB0'
ser = serial.Serial(serName,timeout=0.2) 

bufControlling= [0x01,0x03,0x00,0x00,0x00,0x2e]
crcCheck = crc16(bufControlling,0,len(bufControlling))
bufControlling.append(crcCheck>>8)
bufControlling.append(crcCheck&0xff)

bufQuery= [0x01,0x03,0x00,0x81,0x00,0x1f]
crcCheck = crc16(bufQuery,0,len(bufQuery))
bufQuery.append(crcCheck>>8)
bufQuery.append(crcCheck&0xff)

requestDeviceEvent = threading.Event()
deviceController = DeviceController()
deviceInfo = DeviceInfo()

def RequestDevice():
  global deviceController,deviceInfo
  while not requestDeviceEvent.wait(2):
    ser.write(bufQuery)
    queryRecv = ser.read(1000)
    if checkBuffer(queryRecv,bufQuery):
        deviceInfo.init = True
        getBytesInfo(queryRecv,deviceInfo)
    ser.write(bufControlling)
    controllingRecv = ser.read(1000)
    if checkBuffer(controllingRecv,bufControlling):
        deviceController.init = True
        getBytesControllingInfo(controllingRecv,deviceController)

requestDeviceThread = threading.Thread(target=RequestDevice)
requestDeviceThread.start()

# Run forever!
root.mainloop()
