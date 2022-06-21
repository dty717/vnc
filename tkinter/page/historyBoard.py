from tkinter import *
from tkinter import ttk
from components.table import TreeTable
from models.tableDatas import TableDatas
from database.mongodb import dbGetLogging


class HistoryBoard(Frame):
    def __init__(self, master,**kargs):
        super().__init__(master,kargs)
        self.tableDatas = TableDatas()
        tableDatas = self.tableDatas
        tableDatas.setColumns('time', 'systemType', 'info','otherInfo')
        # column
        tableDatas.column("#0", width=50, minwidth=25)
        tableDatas.column("time",anchor=W, width=200)
        tableDatas.column("systemType",anchor=CENTER, width=80)
        tableDatas.column("info", anchor=W, width=180)
        tableDatas.column("otherInfo", anchor=W, width=180)
        # headingConfigs
        tableDatas.heading("#0",text="序号",anchor=W)
        tableDatas.heading("time",text="时间",anchor=W)
        tableDatas.heading("systemType",text="日志类型",anchor=CENTER)
        tableDatas.heading("info",text="详细信息",anchor=W)
        tableDatas.heading("otherInfo",text="其他信息",anchor=W)
        # data
        loggings = list(dbGetLogging(nPerPage = 0)); 
        for index,logInfo in enumerate(loggings):
            logInfo['time'] = logInfo['time'].strftime("%Y-%m-%d %H:%M:%S")
            tableDatas.insert(parent='',index='end',iid = index,text=str(index+1),values=tuple(logInfo.values())[1:])
        tableFrame = Frame(self)
        tableScrollBar = Scrollbar(tableFrame)
        tableScrollBar.pack(side = RIGHT,fill = Y)
        self.treeTable = TreeTable(tableFrame,tableDatas, yscrollcommand = tableScrollBar.set)
        self.treeTable.pack()
        tableScrollBar.config(command = self.treeTable.yview)
        tableFrame.pack()
    def refreshPage(self):
        self.treeTable.delete(*self.treeTable.get_children())
        tableDatas = self.tableDatas
        tableDatas.clearDatas()
        loggings = list(dbGetLogging(nPerPage = 0)); 
        for index,logInfo in enumerate(loggings):
            logInfo['time'] = logInfo['time'].strftime("%Y-%m-%d %H:%M:%S")
            tableDatas.insert(parent='',index='end',iid = index,text=str(index+1),values=tuple(logInfo.values())[1:])
        self.treeTable.refreshDate(tableDatas)
# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)