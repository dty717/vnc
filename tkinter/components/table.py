from tkinter import *
from tkinter import ttk

class SimpleTable(Frame):
    def __init__(self, parent, header=[], data=[[]]):
        # use black background so it "peeks through" to
        # form grid lines
        Frame.__init__(self, parent, background="black")
        self._widgets = []
        rows = len(data)
        columns = len(data[0])
        current_row = []
        for column in range(columns):
            label = Label(self, text=header[column],
                          borderwidth=0, width=10)
            label.grid(row=0, column=column, sticky="nsew", padx=1, pady=1)
            current_row.append(label)
        self._widgets.append(current_row)
        for row in range(rows):
            current_row = []
            for column in range(columns):
                label = Label(self, text=data[row][column],
                              borderwidth=0, width=10)
                label.grid(row=row+1, column=column,
                           sticky="nsew", padx=1, pady=1)
                current_row.append(label)
            self._widgets.append(current_row)
        for column in range(columns):
            self.grid_columnconfigure(column, weight=1)
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)



class TreeTable(ttk.Treeview):
    def __init__(self, parent):
        # use black background so it "peeks through" to
        # form grid lines
        ttk.Treeview.__init__(self, parent)
        self['columns'] = ('type', 'time', 'value')
        self.column("#0", width=120, minwidth=25)
        self.column("type", anchor=W, width=120)
        self.column("time", anchor=CENTER, width=80)
        self.column("value", anchor=W, width=120)
        self.heading("#0",text="Label",anchor=W)
        self.heading("type",text="Type",anchor=W)
        self.heading("time",text="Time",anchor=CENTER)
        self.heading("value",text="Value",anchor=W)
        self.insert(parent='',index='end',iid=0,text="0",values=("水样",100,10))
        self.insert(parent='',index='end',iid=1,text="1",values=("水样",101,11))
        self.insert(parent='',index='end',iid=2,text="2",values=("水样",102,12))
        self.insert(parent='',index='end',iid=3,text="3",values=("水样",103,13))
        self.insert(parent='',index='end',iid=4,text="4",values=("水样",104,14))
        self.insert(parent='',index='end',iid=5,text="5",values=("水样",105,15))
        self.insert(parent='',index='end',iid=6,text="6",values=("水样",106,16))
        self.insert(parent='',index='end',iid=7,text="7",values=("水样",107,17))
        self.insert(parent='',index='end',iid=8,text="8",values=("水样",108,18))
        self.insert(parent='',index='end',iid=9,text="9",values=("水样",109,19))
        self.insert(parent='',index='end',iid=10,text="10",values=("水样",110,20))
        self.insert(parent='',index='end',iid=11,text="11",values=("水样",111,21))
        self.insert(parent='',index='end',iid=12,text="12",values=("水样",112,22))
        self.insert(parent='',index='end',iid=13,text="13",values=("水样",113,23))
        self.insert(parent='',index='end',iid=14,text="14",values=("水样",114,24))
        self.insert(parent='',index='end',iid=15,text="15",values=("水样",115,25))
        self.insert(parent='',index='end',iid=16,text="16",values=("水样",116,26))
        self.insert(parent='',index='end',iid=17,text="17",values=("水样",117,27))
        self.insert(parent='',index='end',iid=18,text="18",values=("水样",118,28))
        self.insert(parent='',index='end',iid=19,text="19",values=("水样",119,29))
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)

# Inserted at the root, program chooses id:
# tree.insert('', 'end', 'widgets', text='Widget Tour')
