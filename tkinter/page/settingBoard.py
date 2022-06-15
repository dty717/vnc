from tkinter import *
from tkinter import ttk
from components.groupLabelButton import GroupLabelButton
from components.labelButton import LabelTextButton
from PIL import Image
from config.config import *

class SettingBoard(Frame):
    def __init__(self, master,**kargs):
        super().__init__(master,kargs)
        # 
        #groupLabelButton1
        #  
        groupLabelButton1 = GroupLabelButton(self)
        groupLabelButton1.pack()
        labelTextButton10 = LabelTextButton(groupLabelButton1)
        labelTextButton10.pack()
        labelTextButton11 = LabelTextButton(groupLabelButton1)
        labelTextButton11.pack()
        labelTextButton12 = LabelTextButton(groupLabelButton1)
        labelTextButton12.pack()
        labelTextButton13 = LabelTextButton(groupLabelButton1)
        labelTextButton13.pack()
        # 
        #groupLabelButton2
        #  
        groupLabelButton2 = GroupLabelButton(self)
        groupLabelButton2.pack(side="left", fill="x")
        labelTextButton20 = LabelTextButton(groupLabelButton2)
        labelTextButton20.pack()
        labelTextButton21 = LabelTextButton(groupLabelButton2)
        labelTextButton21.pack()
        labelTextButton22 = LabelTextButton(groupLabelButton2)
        labelTextButton22.pack()
        labelTextButton23 = LabelTextButton(groupLabelButton2)
        labelTextButton23.pack()
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