from tkinter import *
from tkinter import ttk
from PIL import Image
from config.config import primaryColor
from components.keyboard import show_keyboard
from mainApp import root_keyboard
class SwitchLabelButton(Frame):
    def __init__(self, parent, imgDicts, text="", textYES="YES", textNO="NO", clickYES=lambda: 0, clickNO=lambda: 0, ):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background=primaryColor, padx=10)
        label = Label(self, text=text, anchor=W, fg="black",
                      bg=primaryColor, width=12, font=("Helvetica", 12))
        label.pack(side="left", fill="x")
        self.imageLabel = Label(
            self, image=imgDicts["redSignal"], bg=primaryColor)
        self.imageLabel.pack(side="left", fill="x")
        button_yes = Button(self, text=textYES,
                            command=clickYES, font=("Helvetica", 12))
        button_yes.pack(side="left", fill="x", padx=25)
        button_no = Button(self, text=textNO, command=clickNO,
                           font=("Helvetica", 12))
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
    def __init__(self, parent, text="", command=lambda content: None):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background=primaryColor, padx=10)
        label = Label(self, text=text, anchor=W, fg="black",
                      bg=primaryColor, width=12, font=("Helvetica", 12))
        label.pack(side="left", fill="x")
        self.text = Entry(self, width=15)
        self.text.bind("<FocusIn>", lambda event:show_keyboard(root_keyboard,event))
        self.text .pack(side="left", fill="x")
        button_set = Button(self, text="设置", command=lambda: command(
            self.text.get()), font=("Helvetica", 12))
        button_set.pack(side="left", fill="x", padx=15)
        # img = PhotoImage(master = parent, file = f"{sysPath}/assets/1.png")
        # label2 = Label(self, image=img)
        # label2.pack()
    def setText(self, value):
        self.text.delete(0, END)
        self.text.insert(0, value)
