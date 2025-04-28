import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,QMessageBox,QSizePolicy,
QLabel,QCheckBox,QHBoxLayout,QSlider,QGridLayout,QComboBox,QScrollArea,QVBoxLayout,QPushButton,QTabWidget

)
from functools import partial
from PyQt6.QtCore import Qt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PyQt6.QtGui import QPixmap
from const import ROOT_DIR
from core.fileHandler import readTextFileToList,readJson,appendJson,FileTracking,deleteKeyFromJson,removeKeyByShift
from PyQt6.QtCore import pyqtSignal

class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore() 

        
class Inventory(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs=QTabWidget()
        self.mainLayout=QVBoxLayout(self)
        self.mainLayout.addWidget(self.tabs)
        
        self.tabs.addTab(EchoShow(),"Echo inventory")
        
class EchoShow(QWidget):
    updateSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        
        self.scroll=QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.mainLayout=QVBoxLayout(self)
        
        widget=QWidget()
        layout=QVBoxLayout(widget)
        
        
        
        self.UIDCombobox=NoScrollComboBox()
        UIDList=readJson("config.json",ROOT_DIR)
        UIDList=UIDList["UID"]
        self.UIDCombobox.addItems(UIDList)
        UIDWidget=QWidget()
        UIDLayout=QVBoxLayout(UIDWidget)
        UIDLayout.addWidget(self.UIDCombobox)
        self.UIDCombobox.currentTextChanged.connect(self.update)
        
        trackFile=[]
        for uid in UIDList:
            trackFile.append(f"{ROOT_DIR}/save/{uid}/echo.json")
            
            
        self.observer = Observer()

        self.handlers = []
        i=0
        for file in trackFile:
            print(file)
            print(f"{ROOT_DIR}/save/{UIDList[i]}")
            handler = FileTracking(filePath=file, callback=self.sendUpdateSignal)
            self.observer.schedule(handler, path=f"{ROOT_DIR}/save/{UIDList[i]}", recursive=False)
            self.handlers.append(handler)
            i+=1

        self.observer.start()
        
        layout.addWidget(UIDWidget)
        self.echoWidget = self.echoInventory()
        layout.addWidget(self.echoWidget)
        self.scroll.setWidget(widget)
        self.mainLayout.addWidget(self.scroll)
        
        self.updateSignal.connect(self.update)

    def sendUpdateSignal(self):
        self.updateSignal.emit()
        
    def update(self):
        self.echoWidget.setParent(None)
        self.echoWidget.deleteLater()

        self.echoWidget = self.echoInventory()

        widget = self.scroll.widget()
        layout = widget.layout()
        layout.addWidget(self.echoWidget)
        
        

    def deleteEcho(self,i):
        removeKeyByShift(self.echoPath,str(i),ROOT_DIR)
    
    def echoInventory(self):
        widget=QWidget()
        layout=QGridLayout(widget)
        self.echoPath=f"save/{self.UIDCombobox.currentText()}/echo.json"
        i=0
        if os.path.exists(self.echoPath):
            data=readJson(self.echoPath,ROOT_DIR)
            for key,val in data.items():
                
                deleteButton=QPushButton("Delete")
                deleteButton.clicked.connect(partial(self.deleteEcho,i=i))
                deleteButton.setStyleSheet( """border: 2px solid #6c757d;
                 border-radius: 10px;""")
                selectButton=QPushButton("Select")
                selectButton.setStyleSheet( """border: 2px solid #6c757d;
                 border-radius: 10px;""")
                
                echoImgLabel=QLabel("No image")
                echoImgPath=ROOT_DIR+f"/data/echo/{data[key]["Name"]}.webp"
                if os.path.exists(echoImgPath):
                    echoImg=QPixmap(echoImgPath)
                    echoImgLabel.setPixmap(echoImg)
                    echoImgLabel.setFixedWidth(int((echoImg.width())*0.8))
                wg=QWidget()
                wgLayout=QGridLayout(wg)
                wgLayout.addWidget(echoImgLabel,0,0,1,1)
                
                info=f"{data[key]["Set name"]}"
                info=info+f"\n{data[key]["Name"]}"
                info=info+f"\n\nCost: {data[key]["Cost"]}"
                info=info+(f"\n\n{data[key]["Main stat 1"][0]}: {data[key]["Main stat 1"][2]}")
                info=info+(f"\n{data[key]["Main stat 2"][0]}: {data[key]["Main stat 2"][2]}")
                info=info+(f"\n\n{data[key]["Sub stat 1"][0]}: {data[key]["Sub stat 1"][2]}")
                info=info+(f"\n{data[key]["Sub stat 2"][0]}: {data[key]["Sub stat 2"][2]}")
                info=info+(f"\n{data[key]["Sub stat 3"][0]}: {data[key]["Sub stat 3"][2]}")
                info=info+(f"\n{data[key]["Sub stat 4"][0]}: {data[key]["Sub stat 4"][2]}")
                info=info+(f"\n{data[key]["Sub stat 5"][0]}: {data[key]["Sub stat 5"][2]}")
                
                echoLabel=QLabel(info)
                echoLabel.setStyleSheet("""border: 2px solid #6c757d;
                 border-radius: 10px;""")
                wgLayout.addWidget(echoLabel,0,1,1,1)
                wgLayout.addWidget(deleteButton,1,0,1,1)
                wgLayout.addWidget(selectButton,1,1,1,1)
                
                layout.addWidget(wg,int(i/3),i%3,1,1)
                i+=1
          
        return widget      
                    
                    
                    