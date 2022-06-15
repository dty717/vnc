from tkinter import *
from tkinter import ttk
from components.table import TreeTable

class SystemLogBoard(Frame):
    def __init__(self, master,**kargs):
        super().__init__(master,kargs)
        treeTable = TreeTable(self)
        treeTable.pack()
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