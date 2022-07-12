from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import threading

from config.labelString import titleLabel
from config.config import sysPath,primaryColor,primaryDarkColor,primaryLightColor
from tool.crc import crc16
from service.logger import Logger
from service.device import sendReq,deviceController,deviceInfo,getBytesControllingInfo,getBytesInfo,requestDeviceEvent,timeSelectEvent,saveSetting
from service.gps import gpsData,getGpsInfo,saveGpsEvent,saveLocation
from page.mainBoard import MainBoard
from page.historyBoard import HistoryBoard
from page.controllingBoard import ControllingBoard
from page.timeSelectingBoard import TimeSelectingBoard
from page.settingBoard import SettingBoard
from page.systemLogBoard import SystemLogBoard
from page.cameraBoard import CameraBoard
from page.locationBoard import LocationBoard

Logger.logWithOutDuration("系统状态", "程序打开", "")
# Create the main window
root = Tk()
screenWidth = root.winfo_screenwidth()
screenHeightShift = 68
screenHeight = root.winfo_screenheight() - screenHeightShift

root.geometry("%dx%d+0+0" % (screenWidth, screenHeight))
root.title(titleLabel)
root.configure(background=primaryDarkColor)
styleConfig = ttk.Style()
# 'ne' as in compass direction
styleConfig.configure('MainMenu', tabposition='wn',background=primaryDarkColor)
styleConfig.configure('MainMenu.Tab',background=primaryLightColor, font=("Helvetica", 16))
styleConfig.map('MainMenu.Tab',background = [('selected',primaryDarkColor)],foreground= [('selected','white')])
styleConfig.configure('HistoryBoard', background=primaryColor)
styleConfig.configure('HistoryBoard.Tab',background=primaryLightColor, font=("Helvetica", 12),padding = 4)
styleConfig.map('HistoryBoard.Tab',background = [('selected',primaryDarkColor)],foreground= [('selected','white')])
styleConfig.configure('Treeview',background="#D3D3D3",foreground="black",rowheight = 25,fieldbackground="#D3D3D3")
styleConfig.map('Treeview',background = [('selected',primaryColor)])

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

styleConfig.layout("MainMenu", [
                   ("MainMenu.client", {"sticky": "nswe"})])
styleConfig.layout("HistoryBoard", [
                   ("HistoryBoard.client", {"sticky": "nswe"})])                   
styleConfig.layout("MainMenu.Tab", [
    ("MainMenu.tab", {
        "sticky": "nswe",
        "children": [
            ("MainMenu.padding", {
                "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("MainMenu.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("MainMenu.label", {
                                     "side": "left", "sticky": ''}),
                                    ("MainMenu.close", {
                                     "side": "left", "sticky": ''}),
                                ]
                            })
                        ]
            })
        ]
    })
])

redSignal = ImageTk.PhotoImage(Image.open(f"{sysPath}/assets/redSignal.png").resize((30, 30)))
greenSignal = ImageTk.PhotoImage(Image.open(f"{sysPath}/assets/greenSignal.png").resize((30, 30)))
# redSignal = PhotoImage(file = f"{sysPath}/assets/redSignal.png")
# greenSignal = PhotoImage(file = f"{sysPath}/assets/greenSignal.png")
imgDicts = {"greenSignal":greenSignal,"redSignal":redSignal}
mainMenu = ttk.Notebook(root,width=screenWidth-300, height=screenHeight-50,padding = 10,style = "MainMenu")
mainMenu.pack()

mainBoard = MainBoard(mainMenu,header=['', '基值', '峰值', 'A值', 'C值'], data=[
    ['标一', deviceInfo.concentration1Value,deviceInfo.concentration1MaxValue, deviceInfo.concentration1AValue,deviceInfo.concentration1CValue],
    ['标二', deviceInfo.concentration2Value,deviceInfo.concentration2MaxValue, deviceInfo.concentration2AValue,deviceInfo.concentration2CValue],
    ['标三', deviceInfo.concentration3Value,deviceInfo.concentration3MaxValue, deviceInfo.concentration3AValue,deviceInfo.concentration3CValue],
    ['水样', deviceInfo.sampleValue,deviceInfo.sampleMaxValue, deviceInfo.sampleAValue,deviceInfo.sampleCValue]],
    width=50, height=50, bg=primaryColor)
historyBoard = HistoryBoard(mainMenu, width=50, height=50, bg=primaryColor)
controllingBoard = ControllingBoard(mainMenu,imgDicts, width=50, height=50, bg=primaryColor)
timeSelectingBoard = TimeSelectingBoard(mainMenu, width=50, height=50, bg=primaryColor)
settingBoard = SettingBoard(mainMenu,imgDicts, width=50, height=50, bg=primaryColor)
systemLogBoard = SystemLogBoard(mainMenu, width=50, height=50, bg=primaryColor)
cameraBoard = CameraBoard(mainMenu, width=50, height=50, bg=primaryColor)
locationBoard = LocationBoard(mainMenu, width=50, height=50, bg=primaryColor)

mainMenu.add(mainBoard, text="主显示面")
mainMenu.add(historyBoard, text="历史数据")
mainMenu.add(controllingBoard, text="设备调试")
mainMenu.add(timeSelectingBoard, text="整点做样")
mainMenu.add(settingBoard, text="参数设置")
mainMenu.add(systemLogBoard, text="运行日志")
mainMenu.add(cameraBoard, text="视频监控")
mainMenu.add(locationBoard, text="位置监测")

lastMenuName = ".!notebook.!mainboard"

def getMenu(menuName):
    if menuName == ".!notebook.!mainboard":
        return mainBoard
    elif menuName == ".!notebook.!historyboard":
        return historyBoard
    elif menuName == ".!notebook.!controllingboard":
        return controllingBoard
    elif menuName == ".!notebook.!timeselectingboard":
        return timeSelectingBoard
    elif menuName == ".!notebook.!settingboard":
        return settingBoard
    elif menuName == ".!notebook.!systemlogboard":
        return systemLogBoard
    elif menuName == ".!notebook.!cameraboard":
        return cameraBoard
    elif menuName == ".!notebook.!locationboard":
        return locationBoard


def changeMenuTab(event):
    global lastMenuName
    currentMenuName = mainMenu.select()
    # currentMenu = getMenu(currentMenuName)
    if lastMenuName == ".!notebook.!cameraboard" and currentMenuName != ".!notebook.!cameraboard":
        cameraBoard.pauseLoop()
    lastMenuName = currentMenuName
    if currentMenuName == ".!notebook.!systemlogboard":
        systemLogBoard.refreshPage()
    elif  currentMenuName == ".!notebook.!historyboard":
        pass
    elif  currentMenuName == ".!notebook.!cameraboard":
        cameraBoard.continueLoop()

mainMenu.bind("<<NotebookTabChanged>>", changeMenuTab)

bufControlling= [0x01,0x03,0x00,0x00,0x00,0x2e]
crcCheck = crc16(bufControlling,0,len(bufControlling))
bufControlling.append(crcCheck>>8)
bufControlling.append(crcCheck&0xff)

bufQuery= [0x01,0x03,0x00,0x81,0x00,0x1f]
crcCheck = crc16(bufQuery,0,len(bufQuery))
bufQuery.append(crcCheck>>8)
bufQuery.append(crcCheck&0xff)

def queryHandle(queryRecv):
    if getBytesInfo(queryRecv,deviceInfo,lastMenuName):
        updatePage()

def updatePage():
    if lastMenuName == ".!notebook.!mainboard":
        mainBoard.refreshPage()
    elif lastMenuName == ".!notebook.!historyboard":
        pass
    elif lastMenuName == ".!notebook.!controllingboard":
        pass
    elif lastMenuName == ".!notebook.!timeSelectingboard":
        pass
    elif lastMenuName == ".!notebook.!settingboard":
        pass
    elif lastMenuName == ".!notebook.!systemLogboard":
        pass
    elif lastMenuName == ".!notebook.!cameraboard":
        pass
    elif lastMenuName == ".!notebook.!locationboard":
        pass

def RequestDevice():
  global deviceController,deviceInfo
  while not requestDeviceEvent.wait(5):
    sendReq(bufQuery, queryHandle, repeatTimes = 0 , needMesBox = False)
    # sendReq(bufControlling, lambda controllingRecv : getBytesControllingInfo(controllingRecv,deviceController,lastMenuName), repeatTimes = 0 , needMesBox = False)
    # print(deviceInfo.measureMinute)
    # ser.write(bufQuery)
    # queryRecv = ser.read(1000)
    # if checkBuffer(queryRecv,bufQuery):
    #     deviceInfo.init = True
    #     getBytesInfo(queryRecv,deviceInfo)
    # ser.write(bufControlling)
    # controllingRecv = ser.read(1000)
    # if checkBuffer(controllingRecv,bufControlling):
    #     deviceController.init = True
    #     getBytesControllingInfo(controllingRecv,deviceController)

requestDeviceThread = threading.Thread(target=RequestDevice)
requestDeviceThread.start()

def getGPS():
    while True:
        getGpsInfo()
getGpsThread = threading.Thread(target=getGPS)
getGpsThread.start()

def saveGPS():
  global gpsData
  while not saveGpsEvent.wait(5*60):
    if gpsData.active == True:
        saveLocation(gpsData.year,gpsData.month,gpsData.date,gpsData.hour,gpsData.minute,gpsData.second,gpsData.latitude,gpsData.longitude)
        pass

saveGpsThread = threading.Thread(target=saveGPS)
saveGpsThread.start()

def selectTime():
  global deviceController 
  while not timeSelectEvent.wait(10*60):
    # datetime
    now = datetime.now()
    if now.minute + 20 > 60:
        during = 60 * 60 - now.minute * 60 - now.second -now.microsecond / 1000000
        timeSelectEvent.wait(during)
        print(datetime.now())
        hour = datetime.now().hour
        if deviceController.selectingHours[hour]:
            Logger.logWithOutDuration("系统测试", "整点做样", str(hour))
        timeSelectEvent.wait(60)
    pass

selectTimeThread = threading.Thread(target=selectTime)
selectTimeThread.start()


def on_closing():
    if messagebox.askokcancel("退出", "确定退出吗?"):
        saveSetting()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
# Run forever!
root.mainloop()
