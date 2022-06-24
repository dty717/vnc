from tkinter import *
from tkinter import ttk
from PIL import Image
from config.config import sysPath

class SwitchLabelButton(Frame):
    def __init__(self, parent ,imgDicts, text = "" , textYES = "YES" ,textNO = "NO",clickYES = lambda : 0,clickNO = lambda : 0, ):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background="red")
        label = Label(self, text=text, fg="black", bg="white",width = 10)
        label.pack(side="left", fill="x")
        self.imageLabel = Label(self,image=imgDicts["redSignal"])
        self.imageLabel.pack(side="left", fill="x")
        button_yes = Button(self, text=textYES , command = clickYES)
        button_yes.pack(side="left", fill="x")
        button_no = Button(self, text=textNO, command = clickNO)
        button_no.pack(side="left", fill="x")
        self.imgDicts = imgDicts
        # img = PhotoImage(master = parent, file = f"{sysPath}/assets/1.png")
        # label2 = Label(self, image=img)
        # label2.pack()
    def open(self):
        self.imageLabel.configure(image=self.imgDicts["greenSignal"])
    def close(self):
        self.imageLabel.configure(image=self.imgDicts["redSignal"])
        

class LabelTextButton(Frame):
    def __init__(self, parent,text = "",command = lambda content:None):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background="red")
        label = Label(self, text=text, fg="black", bg="white")
        label.pack(side="left", fill="x")
        self.text = Entry(self, width=15)
        self.text .pack(side="left", fill="x")
        button_set = Button(self, text="设置",command = lambda :command(self.text.get()))
        button_set.pack(side="left", fill="x")
        # img = PhotoImage(master = parent, file = f"{sysPath}/assets/1.png")
        # label2 = Label(self, image=img)
        # label2.pack()
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)