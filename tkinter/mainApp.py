from tkinter import *
from tkinter import ttk
from config.labelString import *
from page.mainBoard import MainBoard
from page.historyBoard import HistoryBoard
from page.controllingBoard import ControllingBoard
from page.timeSelectingBoard import TimeSelectingBoard
from page.settingBoard import SettingBoard
from page.systemLogBoard import SystemLogBoard

import threading

from PIL import Image
from config.config import *


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

# button = Button(tabNoteBook, text="ABC")

tabNoteBook.add(mainBoard, text="主显示面")
tabNoteBook.add(historyBoard, text="历史数据")
tabNoteBook.add(controllingBoard, text="设备调试")
tabNoteBook.add(timeSelectingBoard, text="整点做样")
tabNoteBook.add(settingBoard, text="参数设置")
tabNoteBook.add(systemLogBoard, text="运行日志")

# menuPanel = PanedWindow(bd=0, relief="raised", bg="red")
# menuPanel.resizable(False, False)
# menuPanel.pack(fill="both", expand=1)
# left_label = Label(menuPanel, text="Left")
# menuPanel.add(left_label)

# mainPanel = PanedWindow(menuPanel, orient=VERTICAL,bd=0, relief="raised", bg="red")
# # mainPanel.resizable(False, False)
# menuPanel.add(mainPanel)
# main_label = Label(mainPanel,text = "mainPanel")
# mainPanel.add(main_label)


# frame1 = Frame(master=root, width=100, height=100, bg="red")
# frame1.pack()

# frame2 = Frame(master=root, width=50, height=50, bg="yellow")
# frame2.pack()

# frame3 = Frame(master=root, width=25, height=25, bg="blue")
# frame3.pack()

# testIndex = 0


# def hello():
#     global testIndex
#     print(testIndex)
#     if testIndex % 6 == 0:
#         frame1.pack_forget()
#     elif testIndex % 6 == 1:
#         frame2.pack_forget()
#     elif testIndex % 6 == 2:
#         frame3.pack_forget()
#     elif testIndex % 6 == 3:
#         frame1.pack()
#     elif testIndex % 6 == 4:
#         frame2.pack()
#     elif testIndex % 6 == 5:
#         frame3.pack()
#     testIndex += 1


# PING_ON = threading.Event()

# def ping():
#   while not PING_ON.wait(1):
#     print("my thread %s" % str(threading.current_thread().ident))
#     hello()

# t = threading.Thread(target=ping)
# t.start()

# Run forever!
root.mainloop()
