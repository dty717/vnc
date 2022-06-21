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
    def __init__(self, parent,tableDatas,**kargs):
        # use black background so it "peeks through" to
        # form grid lines
        ttk.Treeview.__init__(self, parent,**kargs)
        self['columns'] = tableDatas.columns
        for columnConfig in tableDatas.columnConfigs:
            self.column(columnConfig["name"], **columnConfig["attrs"])
        for headingConfig in tableDatas.headingConfigs:
            self.heading(headingConfig["name"], **headingConfig["attrs"])
        for tableData in tableDatas.datas:
            self.insert(**tableData)
    def set(self, row, column, value):
        widget = self._widgets[row][column]
        widget.configure(text=value)
    def refreshDate(self,tableDatas):
        for tableData in tableDatas.datas:
            self.insert(**tableData)


# Inserted at the root, program chooses id:
# tree.insert('', 'end', 'widgets', text='Widget Tour')
