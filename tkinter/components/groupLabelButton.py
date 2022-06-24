from tkinter import *
from tkinter import ttk
from PIL import Image
from config.config import *
class GroupLabelButton(Frame):
    def __init__(self, parent , title = ""):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background="pink")
        titleLabel = Label(self, text = title)
        titleLabel.pack(anchor=W)
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
