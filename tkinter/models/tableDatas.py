from tkinter import *
from tkinter import ttk
from PIL import Image
from config.config import *

class TableDatas():
    def __init__(self):
        self.columnConfigs = []
        self.headingConfigs = []
        self.datas = []
        pass
    def setColumns(self, *columns):
        self.columns = columns
    def column(self, name, **attrs):
        self.columnConfigs.append({
            "name":name,
            "attrs":attrs
        })
    def heading(self, name, **attrs):
        self.headingConfigs.append({
            "name":name,
            "attrs":attrs
        })
    def insert(self, **data):
        self.datas.append(data)
    def clearDatas(self):
        self.datas.clear()