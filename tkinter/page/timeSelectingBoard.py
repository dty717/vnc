from tkinter import *
from tkinter import ttk

class TimeSelectingBoard(Frame):
    def __init__(self, master,**kargs):
        super().__init__(master,kargs)
        buttonFrame = Frame(self, bg="red")
        buttonFrame.pack(side="top",anchor=E)
        button_select = Button(buttonFrame, text="全选")
        button_select.pack(side="left")
        button_reset = Button(buttonFrame, text="重置")
        button_reset.pack(side="left")
        # 
        # 24h
        #
        buttonHours = []
        button1_hour_Frame = Frame(self, bg="red")
        button1_hour_Frame.pack(side="top",anchor=W)
        for i in range(8):
            button_hour = Button(button1_hour_Frame,width=7, height=3, text=str(i))
            button_hour.pack(side="left")
            buttonHours.append(button_hour)
        button2_hour_Frame = Frame(self, bg="red")
        button2_hour_Frame.pack(side="top",anchor=W)
        for i in range(8,16):
            button_hour = Button(button2_hour_Frame,width=7, height=3, text=str(i))
            button_hour.pack(side="left")
            buttonHours.append(button_hour)
        button3_hour_Frame = Frame(self, bg="red")
        button3_hour_Frame.pack(side="top",anchor=W)
        for i in range(16,24):
            button_hour = Button(button3_hour_Frame,width=7, height=3, text=str(i))
            button_hour.pack(side="left")
            buttonHours.append(button_hour)
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