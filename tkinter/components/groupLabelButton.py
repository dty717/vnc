from tkinter import *
from tkinter import ttk
from PIL import Image
from config.config import *
class GroupLabelButton(Frame):
    def __init__(self, parent):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background="pink")
        # img = PhotoImage(master = parent, file = f"{sysPath}/assets/1.png")
        # label2 = Label(self, image=img)
        # label2.pack()
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
