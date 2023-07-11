from tkinter import *
from tkinter import ttk
from components.table import TreeTable
from models.tableDatas import TableDatas
from database.mongodb import dbGetHistory, dbGetConcentration1History, dbGetConcentration2History, dbGetTestHistory,dbGetConcentration3History

class HistoryBoard(Frame):
    def __init__(self, master, **kargs):
        super().__init__(master, kargs)
        historyTabs = ttk.Notebook(self, padding=10, style="HistoryBoard")
        historyTabs.pack(fill=BOTH)
        ##
        ## sampleHistory
        ##
        self.historyTableDatas = TableDatas()
        historyTableDatas = self.historyTableDatas
        historyTableDatas.setColumns(
            'time', 'value', 'maxValue', 'AValue', 'CValue')
        # column
        historyTableDatas.column("#0", width=50, minwidth=25)
        historyTableDatas.column("time", anchor=W, width=200)
        historyTableDatas.column("value", anchor=CENTER, width=110)
        historyTableDatas.column("maxValue", anchor=W, width=110)
        historyTableDatas.column("AValue", anchor=W, width=110)
        historyTableDatas.column("CValue", anchor=W, width=110)
        # headingConfigs
        historyTableDatas.heading("#0", text="序号", anchor=W)
        historyTableDatas.heading("time", text="时间", anchor=W)
        historyTableDatas.heading("value", text="基值", anchor=CENTER)
        historyTableDatas.heading("maxValue", text="峰值", anchor=W)
        historyTableDatas.heading("AValue", text="A值", anchor=W)
        historyTableDatas.heading("CValue", text="C值", anchor=W)
        # data
        histories = list(dbGetHistory(nPerPage=0))
        for index, history in enumerate(histories):
            history['time'] = history['time'].strftime("%Y-%m-%d %H:%M:%S")
            history['AValue'] = round(history['AValue'], 4)
            history['CValue'] = round(history['CValue'], 4)
            historyTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(history.values())[1:])
        historyTab = Frame(self)
        historyTableScrollBar = Scrollbar(historyTab)
        historyTableScrollBar.pack(side=RIGHT, fill=Y)
        self.historyTreeTable = TreeTable(
            historyTab, historyTableDatas, yscrollcommand=historyTableScrollBar.set, height=20)
        self.historyTreeTable.pack()
        historyTableScrollBar.config(command=self.historyTreeTable.yview)
        historyTab.pack()
        ##
        ## concentration1History
        ##
        self.concentration1HistoryTableDatas = TableDatas()
        concentration1HistoryTableDatas = self.concentration1HistoryTableDatas
        concentration1HistoryTableDatas.setColumns(
            'time', 'value', 'maxValue', 'AValue', 'CValue')
        # column
        concentration1HistoryTableDatas.column("#0", width=50, minwidth=25)
        concentration1HistoryTableDatas.column("time", anchor=W, width=200)
        concentration1HistoryTableDatas.column(
            "value", anchor=CENTER, width=110)
        concentration1HistoryTableDatas.column("maxValue", anchor=W, width=110)
        concentration1HistoryTableDatas.column("AValue", anchor=W, width=110)
        concentration1HistoryTableDatas.column("CValue", anchor=W, width=110)
        # headingConfigs
        concentration1HistoryTableDatas.heading("#0", text="序号", anchor=W)
        concentration1HistoryTableDatas.heading("time", text="时间", anchor=W)
        concentration1HistoryTableDatas.heading(
            "value", text="基值", anchor=CENTER)
        concentration1HistoryTableDatas.heading(
            "maxValue", text="峰值", anchor=W)
        concentration1HistoryTableDatas.heading("AValue", text="A值", anchor=W)
        concentration1HistoryTableDatas.heading("CValue", text="C值", anchor=W)
        # data
        concentration1Histories = list(dbGetConcentration1History(nPerPage=0))
        for index, concentration1History in enumerate(concentration1Histories):
            concentration1History['time'] = concentration1History['time'].strftime(
                "%Y-%m-%d %H:%M:%S")
            concentration1History['AValue'] = round(
                concentration1History['AValue'], 4)
            concentration1History['CValue'] = round(
                concentration1History['CValue'], 4)
            concentration1HistoryTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(concentration1History.values())[1:])
        concentration1HistoryTab = Frame(self)
        concentration1HistoryTableScrollBar = Scrollbar(
            concentration1HistoryTab)
        concentration1HistoryTableScrollBar.pack(side=RIGHT, fill=Y)
        self.concentration1HistoryTreeTable = TreeTable(concentration1HistoryTab, concentration1HistoryTableDatas,
                                                        yscrollcommand=concentration1HistoryTableScrollBar.set, height=20)
        self.concentration1HistoryTreeTable.pack()
        concentration1HistoryTableScrollBar.config(
            command=self.concentration1HistoryTreeTable.yview)
        concentration1HistoryTab.pack()
        ##
        ## concentration2History
        ##
        self.concentration2HistoryTableDatas = TableDatas()
        concentration2HistoryTableDatas = self.concentration2HistoryTableDatas
        concentration2HistoryTableDatas.setColumns(
            'time', 'value', 'maxValue', 'AValue', 'CValue')
        # column
        concentration2HistoryTableDatas.column("#0", width=50, minwidth=25)
        concentration2HistoryTableDatas.column("time", anchor=W, width=200)
        concentration2HistoryTableDatas.column(
            "value", anchor=CENTER, width=110)
        concentration2HistoryTableDatas.column("maxValue", anchor=W, width=110)
        concentration2HistoryTableDatas.column("AValue", anchor=W, width=110)
        concentration2HistoryTableDatas.column("CValue", anchor=W, width=110)
        # headingConfigs
        concentration2HistoryTableDatas.heading("#0", text="序号", anchor=W)
        concentration2HistoryTableDatas.heading("time", text="时间", anchor=W)
        concentration2HistoryTableDatas.heading(
            "value", text="基值", anchor=CENTER)
        concentration2HistoryTableDatas.heading(
            "maxValue", text="峰值", anchor=W)
        concentration2HistoryTableDatas.heading("AValue", text="A值", anchor=W)
        concentration2HistoryTableDatas.heading("CValue", text="C值", anchor=W)
        # data
        concentration2Histories = list(dbGetConcentration2History(nPerPage=0))
        for index, concentration2History in enumerate(concentration2Histories):
            concentration2History['time'] = concentration2History['time'].strftime(
                "%Y-%m-%d %H:%M:%S")
            concentration2History['AValue'] = round(
                concentration2History['AValue'], 4)
            concentration2History['CValue'] = round(
                concentration2History['CValue'], 4)
            concentration2HistoryTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(concentration2History.values())[1:])
        concentration2HistoryTab = Frame(self)
        concentration2HistoryTableScrollBar = Scrollbar(
            concentration2HistoryTab)
        concentration2HistoryTableScrollBar.pack(side=RIGHT, fill=Y)
        self.concentration2HistoryTreeTable = TreeTable(concentration2HistoryTab, concentration2HistoryTableDatas,
                                                        yscrollcommand=concentration2HistoryTableScrollBar.set, height=20)
        self.concentration2HistoryTreeTable.pack()
        concentration2HistoryTableScrollBar.config(
            command=self.concentration2HistoryTreeTable.yview)
        concentration2HistoryTab.pack()
        ##
        ## concentration3History
        ##
        self.concentration3HistoryTableDatas = TableDatas()
        concentration3HistoryTableDatas = self.concentration3HistoryTableDatas
        concentration3HistoryTableDatas.setColumns(
            'time', 'value', 'maxValue', 'AValue', 'CValue')
        # column
        concentration3HistoryTableDatas.column("#0", width=50, minwidth=25)
        concentration3HistoryTableDatas.column("time", anchor=W, width=200)
        concentration3HistoryTableDatas.column(
            "value", anchor=CENTER, width=110)
        concentration3HistoryTableDatas.column("maxValue", anchor=W, width=110)
        concentration3HistoryTableDatas.column("AValue", anchor=W, width=110)
        concentration3HistoryTableDatas.column("CValue", anchor=W, width=110)
        # headingConfigs
        concentration3HistoryTableDatas.heading("#0", text="序号", anchor=W)
        concentration3HistoryTableDatas.heading("time", text="时间", anchor=W)
        concentration3HistoryTableDatas.heading(
            "value", text="基值", anchor=CENTER)
        concentration3HistoryTableDatas.heading(
            "maxValue", text="峰值", anchor=W)
        concentration3HistoryTableDatas.heading("AValue", text="A值", anchor=W)
        concentration3HistoryTableDatas.heading("CValue", text="C值", anchor=W)
        # data
        concentration3Histories = list(dbGetConcentration3History(nPerPage=0))
        for index, concentration3History in enumerate(concentration3Histories):
            concentration3History['time'] = concentration3History['time'].strftime(
                "%Y-%m-%d %H:%M:%S")
            concentration3History['AValue'] = round(
                concentration3History['AValue'], 4)
            concentration3History['CValue'] = round(
                concentration3History['CValue'], 4)
            concentration3HistoryTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(concentration3History.values())[1:])
        concentration3HistoryTab = Frame(self)
        concentration3HistoryTableScrollBar = Scrollbar(
            concentration3HistoryTab)
        concentration3HistoryTableScrollBar.pack(side=RIGHT, fill=Y)
        self.concentration3HistoryTreeTable = TreeTable(concentration3HistoryTab, concentration3HistoryTableDatas,
                                                        yscrollcommand=concentration3HistoryTableScrollBar.set, height=20)
        self.concentration3HistoryTreeTable.pack()
        concentration3HistoryTableScrollBar.config(
            command=self.concentration3HistoryTreeTable.yview)
        concentration3HistoryTab.pack()
        ##
        ## testHistory
        ##
        self.testHistoryTableDatas = TableDatas()
        testHistoryTableDatas = self.testHistoryTableDatas
        testHistoryTableDatas.setColumns(
            'time', 'value', 'maxValue', 'AValue', 'CValue')
        # column
        testHistoryTableDatas.column("#0", width=50, minwidth=25)
        testHistoryTableDatas.column("time", anchor=W, width=200)
        testHistoryTableDatas.column(
            "value", anchor=CENTER, width=110)
        testHistoryTableDatas.column("maxValue", anchor=W, width=110)
        testHistoryTableDatas.column("AValue", anchor=W, width=110)
        testHistoryTableDatas.column("CValue", anchor=W, width=110)
        # headingConfigs
        testHistoryTableDatas.heading("#0", text="序号", anchor=W)
        testHistoryTableDatas.heading("time", text="时间", anchor=W)
        testHistoryTableDatas.heading(
            "value", text="基值", anchor=CENTER)
        testHistoryTableDatas.heading(
            "maxValue", text="峰值", anchor=W)
        testHistoryTableDatas.heading("AValue", text="A值", anchor=W)
        testHistoryTableDatas.heading("CValue", text="C值", anchor=W)
        # data
        concentration3Histories = list(dbGetTestHistory(nPerPage=0))
        for index, testHistory in enumerate(concentration3Histories):
            testHistory['time'] = testHistory['time'].strftime(
                "%Y-%m-%d %H:%M:%S")
            testHistory['AValue'] = round(
                testHistory['AValue'], 4)
            testHistory['CValue'] = round(
                testHistory['CValue'], 4)
            testHistoryTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(testHistory.values())[1:])
        testHistoryTab = Frame(self)
        testHistoryTableScrollBar = Scrollbar(
            testHistoryTab)
        testHistoryTableScrollBar.pack(side=RIGHT, fill=Y)
        self.testHistoryTreeTable = TreeTable(testHistoryTab, testHistoryTableDatas,
                                                        yscrollcommand=testHistoryTableScrollBar.set, height=20)
        self.testHistoryTreeTable.pack()
        testHistoryTableScrollBar.config(
            command=self.testHistoryTreeTable.yview)
        testHistoryTab.pack()

        #
        # historyTab = Frame(self,width=50, height=50, bg="red")
        # concentration1Tab = Frame(self, width=50, height=50, bg="yellow")
        historyTabs.add(historyTab, text="水样历史")
        historyTabs.add(concentration1HistoryTab, text="标一历史")
        historyTabs.add(concentration2HistoryTab, text="标二历史")
        historyTabs.add(concentration3HistoryTab, text="标三历史")
        historyTabs.add(testHistoryTab, text="标核历史")
    def refreshPage(self):
        ##
        ## sampleHistory
        ##
        self.historyTreeTable.delete(*self.historyTreeTable.get_children())
        historyTableDatas = self.historyTableDatas
        historyTableDatas.clearDatas()
        # data
        histories = list(dbGetHistory(nPerPage=0))
        for index, history in enumerate(histories):
            history['time'] = history['time'].strftime("%Y-%m-%d %H:%M:%S")
            history['AValue'] = round(history['AValue'], 4)
            history['CValue'] = round(history['CValue'], 4)
            historyTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(history.values())[1:])
        self.historyTreeTable.refreshDate(historyTableDatas)
        ##
        ## concentration1History
        ##
        self.concentration1HistoryTreeTable.delete(
            *self.concentration1HistoryTreeTable.get_children())
        concentration1HistoryTableDatas = self.concentration1HistoryTableDatas
        concentration1HistoryTableDatas.clearDatas()
        # data
        concentration1Histories = list(dbGetConcentration1History(nPerPage=0))
        for index, concentration1History in enumerate(concentration1Histories):
            concentration1History['time'] = concentration1History['time'].strftime(
                "%Y-%m-%d %H:%M:%S")
            concentration1History['AValue'] = round(
                concentration1History['AValue'], 4)
            concentration1History['CValue'] = round(
                concentration1History['CValue'], 4)
            concentration1HistoryTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(concentration1History.values())[1:])
        self.concentration1HistoryTreeTable.refreshDate(
            concentration1HistoryTableDatas)
        ##
        ## concentration2History
        ##
        self.concentration2HistoryTreeTable.delete(
            *self.concentration2HistoryTreeTable.get_children())
        concentration2HistoryTableDatas = self.concentration2HistoryTableDatas
        concentration2HistoryTableDatas.clearDatas()
        # data
        concentration2Histories = list(dbGetConcentration2History(nPerPage=0))
        for index, concentration2History in enumerate(concentration2Histories):
            concentration2History['time'] = concentration2History['time'].strftime(
                "%Y-%m-%d %H:%M:%S")
            concentration2History['AValue'] = round(
                concentration2History['AValue'], 4)
            concentration2History['CValue'] = round(
                concentration2History['CValue'], 4)
            concentration2HistoryTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(concentration2History.values())[1:])
        self.concentration2HistoryTreeTable.refreshDate(
            concentration2HistoryTableDatas)
        ##
        ## concentration3History
        ##
        self.concentration3HistoryTreeTable.delete(
            *self.concentration3HistoryTreeTable.get_children())
        concentration3HistoryTableDatas = self.concentration3HistoryTableDatas
        concentration3HistoryTableDatas.clearDatas()
        # data
        concentration3Histories = list(dbGetConcentration3History(nPerPage=0))
        for index, concentration3History in enumerate(concentration3Histories):
            concentration3History['time'] = concentration3History['time'].strftime(
                "%Y-%m-%d %H:%M:%S")
            concentration3History['AValue'] = round(
                concentration3History['AValue'], 4)
            concentration3History['CValue'] = round(
                concentration3History['CValue'], 4)
            concentration3HistoryTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(concentration3History.values())[1:])
        self.concentration3HistoryTreeTable.refreshDate(
            concentration3HistoryTableDatas)
        ##
        ## testHistoryHistory
        ##
        self.testHistoryTreeTable.delete(
            *self.testHistoryTreeTable.get_children())
        testHistoryTableDatas = self.testHistoryTableDatas
        testHistoryTableDatas.clearDatas()
        # data
        testHistoryHistories = list(dbGetTestHistory(nPerPage=0))
        for index, testHistory in enumerate(testHistoryHistories):
            testHistory['time'] = testHistory['time'].strftime(
                "%Y-%m-%d %H:%M:%S")
            testHistory['AValue'] = round(
                testHistory['AValue'], 4)
            testHistory['CValue'] = round(
                testHistory['CValue'], 4)
            testHistoryTableDatas.insert(parent='', index='end', iid=index, text=str(
                index+1), values=tuple(testHistory.values())[1:])
        self.testHistoryTreeTable.refreshDate(
            testHistoryTableDatas)
# mianBoard = Frame(tabNoteBook, width=100, height=100, bg="red")
# mianBoard.pack(fill=BOTH, expand=1)
