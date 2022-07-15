from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, timedelta
import threading
import asyncio
import json
import websocket
from config.labelString import titleLabel
from config.config import sysPath, primaryColor, primaryDarkColor, primaryLightColor, wsHostname, url, deviceID
from tool.crc import crc16
from service.logger import Logger
from service.device import DeviceAddr, write_single_register, sendReq, deviceController, deviceInfo, getBytesControllingInfo, getBytesInfo, requestDeviceEvent, timeSelectEvent, saveSetting, lastClickStartTime, lastSelectTime, power
from service.gps import gpsData, getGpsInfo, saveGpsEvent, saveLocation
from page.mainBoard import MainBoard
from page.historyBoard import HistoryBoard
from page.controllingBoard import ControllingBoard
from page.timeSelectingBoard import TimeSelectingBoard
from page.settingBoard import SettingBoard
from page.systemLogBoard import SystemLogBoard
from page.cameraBoard import CameraBoard
from page.locationBoard import LocationBoard
from database.mongodb import dbGetLastHistory

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
styleConfig.configure('MainMenu', tabposition='wn',
                      background=primaryDarkColor)
styleConfig.configure(
    'MainMenu.Tab', background=primaryLightColor, font=("Helvetica", 16))
styleConfig.map('MainMenu.Tab', background=[
                ('selected', primaryDarkColor)], foreground=[('selected', 'white')])
styleConfig.configure('HistoryBoard', background=primaryColor)
styleConfig.configure('HistoryBoard.Tab', background=primaryLightColor, font=(
    "Helvetica", 12), padding=4)
styleConfig.map('HistoryBoard.Tab', background=[
                ('selected', primaryDarkColor)], foreground=[('selected', 'white')])
styleConfig.configure('Treeview', background="#D3D3D3",
                      foreground="black", rowheight=25, fieldbackground="#D3D3D3")
styleConfig.map('Treeview', background=[('selected', primaryDarkColor)])

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
                           ("active", "!disabled", "img_closeactive"), width=130, padding=30, sticky='')

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

redSignal = ImageTk.PhotoImage(Image.open(
    f"{sysPath}/assets/redSignal.png").resize((30, 30)))
greenSignal = ImageTk.PhotoImage(Image.open(
    f"{sysPath}/assets/greenSignal.png").resize((30, 30)))
# redSignal = PhotoImage(file = f"{sysPath}/assets/redSignal.png")
# greenSignal = PhotoImage(file = f"{sysPath}/assets/greenSignal.png")
imgDicts = {"greenSignal": greenSignal, "redSignal": redSignal}
mainMenu = ttk.Notebook(root, width=screenWidth-300,
                        height=screenHeight-50, padding=10, style="MainMenu")
mainMenu.pack()

mainBoard = MainBoard(mainMenu, header=['', '基值', '峰值', 'A值', 'C值'], data=[
    ['标一', round(deviceInfo.concentration1Value, 4), round(deviceInfo.concentration1MaxValue, 4), round(
        deviceInfo.concentration1AValue, 4), round(deviceInfo.concentration1CValue, 4)],
    ['标二', round(deviceInfo.concentration2Value, 4), round(deviceInfo.concentration2MaxValue, 4), round(
        deviceInfo.concentration2AValue, 4), round(deviceInfo.concentration2CValue, 4)],
    ['标三', round(deviceInfo.concentration3Value, 4), round(deviceInfo.concentration3MaxValue, 4), round(
        deviceInfo.concentration3AValue, 4), round(deviceInfo.concentration3CValue, 4)],
    ['水样', round(deviceInfo.sampleValue, 4), round(deviceInfo.sampleMaxValue, 4), round(deviceInfo.sampleAValue, 4), round(deviceInfo.sampleCValue, 4)]],
    width=50, height=50, bg=primaryColor)
historyBoard = HistoryBoard(mainMenu, width=50, height=50, bg=primaryColor)
controllingBoard = ControllingBoard(
    mainMenu, imgDicts, width=50, height=50, bg=primaryColor)
timeSelectingBoard = TimeSelectingBoard(
    mainMenu, width=50, height=50, bg=primaryColor,padx = 20)
settingBoard = SettingBoard(
    mainMenu, imgDicts, width=50, height=50, bg=primaryColor)
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
    elif currentMenuName == ".!notebook.!historyboard":
        historyBoard.refreshPage()
    elif currentMenuName == ".!notebook.!mainboard":
        mainBoard.refreshPage()
    elif currentMenuName == ".!notebook.!controllingboard":
        controllingBoard.refreshPage()
    elif currentMenuName == ".!notebook.!timeselectingboard":
        timeSelectingBoard.refreshPage()
    elif currentMenuName == ".!notebook.!settingboard":
        settingBoard.refreshPage()
    elif currentMenuName == ".!notebook.!locationboard":
        locationBoard.refreshPage()
    elif currentMenuName == ".!notebook.!cameraboard":
        cameraBoard.continueLoop()

mainMenu.bind("<<NotebookTabChanged>>", changeMenuTab)

bufControlling = [0x01, 0x03, 0x00, 0x00, 0x00, 0x2e]
crcCheck = crc16(bufControlling, 0, len(bufControlling))
bufControlling.append(crcCheck >> 8)
bufControlling.append(crcCheck & 0xff)

bufQuery = [0x01, 0x03, 0x00, 0x81, 0x00, 0x23]
crcCheck = crc16(bufQuery, 0, len(bufQuery))
bufQuery.append(crcCheck >> 8)
bufQuery.append(crcCheck & 0xff)

def updatePage():
    if lastMenuName == ".!notebook.!mainboard":
        mainBoard.refreshPage()
    elif lastMenuName == ".!notebook.!historyboard":
        historyBoard.refreshPage()
    elif lastMenuName == ".!notebook.!controllingboard":
        controllingBoard.refreshPage()
    elif lastMenuName == ".!notebook.!timeSelectingboard":
        timeSelectingBoard.refreshPage()
    elif lastMenuName == ".!notebook.!settingboard":
        settingBoard.refreshPage()
    elif lastMenuName == ".!notebook.!systemLogboard":
        pass
    elif lastMenuName == ".!notebook.!cameraboard":
        pass
    elif lastMenuName == ".!notebook.!locationboard":
        pass

def queryHandle(queryRecv):
    if getBytesInfo(queryRecv, deviceInfo, lastMenuName):
        updatePage()
    Logger.logWithOutDuration(
        "系统测试", "dataFlag:"+str(deviceInfo.dataFlag), ' '.join([str(e) for e in queryRecv]))

def controllingHandle(controllingRecv):
    if getBytesControllingInfo(controllingRecv,deviceController,lastMenuName):
        updatePage()
    Logger.logWithOutDuration(
        "系统测试", "controlling rec", ' '.join([str(e) for e in controllingRecv]))

def RequestDevice():
  global deviceController, deviceInfo
  while not requestDeviceEvent.wait(5):
    sendReq(bufQuery, queryHandle, repeatTimes=0, needMesBox=False)
    sendReq(bufControlling, controllingHandle, repeatTimes = 0 , needMesBox = False)
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
        saveLocation(gpsData.year, gpsData.month, gpsData.date, gpsData.hour,
                     gpsData.minute, gpsData.second, gpsData.latitude, gpsData.longitude)
        pass

saveGpsThread = threading.Thread(target=saveGPS)
saveGpsThread.start()

def checkLastSelectTime():
    global lastSelectTime, lastClickStartTime
    now = datetime.now()
    if lastSelectTime > lastClickStartTime and now > lastSelectTime + timedelta(hours=1, minutes=40) and power.value == 1:
        lastHistory = list(dbGetLastHistory())
        if len(lastHistory) == 0:
            return False
        else:
            lastHistory = lastHistory[0]
            if now > lastHistory['time'] + timedelta(hours=1, minutes=40):
                return False
    return True

def selectTime():
  global deviceController, lastSelectTime
  while not timeSelectEvent.wait(10*60):
    # datetime
    now = datetime.now()
    if not checkLastSelectTime():
        # error
        Logger.log("设备异常", "设备做样异常,未能整点做样", "", 3600)
        continue
    if now.minute + 20 > 60:
        during = 60 * 60 - now.minute * 60 - now.second - now.microsecond / 1000000
        timeSelectEvent.wait(during)
        print(datetime.now())
        hour = datetime.now().hour
        if deviceController.selectingHours[hour]:
            if checkLastSelectTime():
                lastSelectTime = datetime.now()
                # start select time
                power.value = 1
                timeSelectEvent.wait(60)
                write_single_register(DeviceAddr.modelSelectAddr.value, 1,
                                      lambda rec: None, repeatTimes=3, needMesBox=False)
                write_single_register(DeviceAddr.operationSelectAddr.value, 1,
                                      lambda rec: None, repeatTimes=3, needMesBox=False)
        timeSelectEvent.wait(60)
    pass
selectTimeThread = threading.Thread(target=selectTime)
selectTimeThread.start()

jsonDecoder = json.JSONDecoder()

wid = None

def on_message(ws, message):
    global wid
    jsonObj = jsonDecoder.decode(message)
    wType = jsonObj["type"]
    if wType == 'id':
        wid = jsonObj["id"]
        ws.send("{\"type\":\"deviceID\",\"name\":\"" +
                deviceID+"\",\"id\":"+str(wid)+"}")

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")
# websocket.enableTrace(True)
ws = websocket.WebSocketApp(url,
                            subprotocols=["json"],
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)
websocketThread = threading.Thread(target=ws.run_forever)
websocketThread.start()

# asyncio.run(connectWebsocket())

# connectWebsocketLoop = asyncio.get_event_loop()
# try:
#     connectWebsocketLoop.run_until_complete(connectWebsocket())
# finally:
#     connectWebsocketLoop.close()

def on_closing():
    if messagebox.askokcancel("退出", "确定退出吗?"):
        saveSetting()
        root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
# Run forever!
root.mainloop()
