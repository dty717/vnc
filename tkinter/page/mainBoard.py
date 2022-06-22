from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
from components.table import SimpleTable
from service.device import write_single_register,DeviceAddr,deviceInfo,deviceController

mainText = None

# date(2002, 12, 4).strftime("")


def test():
    messagebox.showinfo("设置", str(deviceController))
    updateMainDate(2022,12,12,1,1,32,121.2112,0)

def stateString(state):
    if state == 0:
        return "正常"
    return ""

def updateMainDate(year, month, day, hour, minitue, second, value, state):
    global mainText
    mainText.set("做样时间:"+datetime(year, month, day, hour, minitue, second).strftime("%Y-%m-%d %H:%M:%S")+"\n" +
                 "做样数据:"+str(value)+"mg/L\n" +
                 "报警状态:"+stateString(state))


class MainBoard(Frame):
    def __init__(self, master, **kargs):
        global mainText
        super().__init__(master, kargs)
        mainText = StringVar()
        mainText.set("""做样时间:
做样数据:
报警状态:""")
        mainLabel = Label(self, textvariable=mainText, fg="black", bg="white")
        mainLabel.pack(side="top", fill="x")
        mainTable = SimpleTable(self, header=['', '基值', '峰值', 'A值', 'C值'], data=[['标一', 'v1','v2', 'v3','v4'],['标二', 'v1','v2', 'v3','v4'],['标三', 'v1','v2', 'v3','v4'],['水样', 's1','s2', 's3','s4']])
        mainTable.pack(side="bottom", fill="x")
        button = Button(self, text="Button", command=test)
        button.pack()
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
