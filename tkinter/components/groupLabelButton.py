from tkinter import *
from tkinter import ttk
from PIL import Image
from config.config import primaryColor
class GroupLabelButton(Frame):
    def __init__(self, parent , title = "" , font=(None, 16), padx = 10):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background=primaryColor,relief=RIDGE,
            borderwidth=2)
        titleLabel = Label(self, text = title , font = font,bg = primaryColor)
        titleLabel.pack(anchor=W, padx = padx)
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
