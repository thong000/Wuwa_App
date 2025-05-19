import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
QLabel,QCheckBox,QHBoxLayout,QSlider,QGridLayout,QComboBox,QScrollArea,QVBoxLayout,QLineEdit

)
from PyQt6.QtGui import QPixmap
from const import ROOT_DIR
from core.fileHandler import readTextFileToList,readJson,printDictPretty

class NoScrollSlider(QSlider):
    def wheelEvent(self, event):
        event.ignore()
   
class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore() 
        
        
from PyQt6.QtCore import(Qt)
from functools import partial

class GachaHistory(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()
        self.mainLayout = QVBoxLayout(self)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(self.contentWidget)
        
        self.pityList=[]
        self.UIDCombobox=NoScrollComboBox()
        UIDList=readJson("config.json",ROOT_DIR)
        
        UIDList=UIDList["UID"]
        self.UIDCombobox.addItems(UIDList)

        self.contentLayout.addWidget(self.UIDCombobox)
        
        
        self.uid=self.UIDCombobox.currentText()
        self.historyFilePath=f"gachaHistory/wuwatracker-pulls_{self.uid}.json"
        self.history=readJson(self.historyFilePath,ROOT_DIR)
        self.history=self.history["data"]
        
        self.barnerSelecter=QComboBox()
        self.barnerTypeDict={
            "Featured Resonator":0,
            "Featured Weapon":1,
            "Permanent Resonator":2,
            "Permanent Weapon":3,
            "Novice Convene":4,
            "Beginner's Choice Convene":5,
            "Giveback Event Convene":6
        }
        barnerTypeList=[]
        for key, val in self.barnerTypeDict.items():
            barnerTypeList.append(key)
        self.barnerSelecter.addItems(barnerTypeList)
        self.contentLayout.addWidget(self.barnerSelecter)
        
        self.historyWg=QWidget()
        self.historyLayout=QVBoxLayout(self.historyWg)
        
        
        self.contentLayout.addWidget(self.summaryPity())
        self.contentLayout.addWidget(self.historyWidget())
        
        self.barnerSelecter.currentTextChanged.connect(self.updateHistoryWidget)

        self.scroll.setWidget(self.contentWidget)

        self.mainLayout.addWidget(self.scroll)
      
      
        
    def historyWidget(self):
        self.historyWidgetContainer = QWidget()
        self.historyLayout = QVBoxLayout(self.historyWidgetContainer)

        self.updateHistoryWidget()

        return self.historyWidgetContainer
        
        
        
        
    def summaryPity(self):
        def averageBeforeOne(arr):
            result = []
            for i in range(1, len(arr)):
                if arr[i] == 1:
                    result.append(arr[i - 1])
            if arr:  # kiểm tra mảng không rỗng
                result.append(arr[-1])  # thêm phần tử cuối
            return sum(result) / len(result) if result else 0
        
        avgPity=averageBeforeOne(self.pityList)
        widget=QWidget()
        layout=QVBoxLayout(widget)
        
        self.summaryWg=QLabel("No data")
        self.updateSummary(avgPity)
        layout.addWidget(self.summaryWg)
        return widget
        
    def  updateSummary(self,avg):
        self.summaryWg.setText(f"{"Average pity":15}{avg:.2f}")



    def updateHistoryWidget(self):
        # Xoá toàn bộ widget con trong layout
        while self.historyLayout.count():
            child = self.historyLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Lấy dữ liệu mới và thêm lại các QLabel
        
        historyList = self.history[self.barnerTypeDict[self.barnerSelecter.currentText()]][1]
        i=len(historyList)
        
        j=1
        self.pityList=[]
        for entry in historyList:
            self.pityList.append(j)
            if entry["qualityLevel"]==5:
                j=0
            j+=1
        

        for entry in reversed(historyList):
            tmp=QLabel( f"No.{i}\t\t{self.pityList[i-1]}\t\t{entry["name"]}" )
            if entry["qualityLevel"]==4:
                tmp.setStyleSheet("color:#c77dff;")
            if entry["qualityLevel"]==5:
                tmp.setStyleSheet("color:yellow;")
            if entry["qualityLevel"]==3:
                tmp.setStyleSheet("color:green;")
            self.historyLayout.addWidget(tmp)
            i-=1
            
        def averageBeforeOne(arr):
            result = []
            for i in range(1, len(arr)):
                if arr[i] == 1:
                    result.append(arr[i - 1])
            if arr: 
                result.append(arr[-1]) 
            return sum(result) / len(result) if result else 0
        self.updateSummary(averageBeforeOne(self.pityList))
