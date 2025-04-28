import os
import json
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,QMessageBox,
QLabel,QCheckBox,QHBoxLayout,QSlider,QGridLayout,QComboBox,QScrollArea,QVBoxLayout,QPushButton

)
from PyQt6.QtGui import QPixmap
from const import ROOT_DIR
from core.fileHandler import readTextFileToList,readJson,appendJson

class NoScrollSlider(QSlider):
    def wheelEvent(self, event):
        event.ignore()
   
class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore() 
        
from PyQt6.QtCore import(Qt)
from functools import partial



class EchoStatTab(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()

        self.mainLayout = QVBoxLayout(self)
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.contentWidget = QWidget()
        self.contentLayout = QVBoxLayout(self.contentWidget)
        
        # Select UID
        self.UIDCombobox=NoScrollComboBox()
        UIDList=readJson("config.json",ROOT_DIR)
        UIDList=UIDList["UID"]
        self.UIDCombobox.addItems(UIDList)
        UIDWidget=QWidget()
        UIDLayout=QVBoxLayout(UIDWidget)
        UIDLayout.addWidget(self.UIDCombobox)
        

        self.echoName=readJson("data/echo.json",ROOT_DIR)
        
        # Prepare substat
        self.subStat=["Crit Rate","Crit DMG","Atk%","Atk","Hp%","Hp","Def%","Def","BA Bonus",
                    "HA Bonus","RS Bonus","RL Bonus","Energy Regen"]
        self.subStatDict={
            "Crit Rate":["cr",[6.3,6.9,7.5,8.1,8.7,9.3,9.9,10.5]],
            "Crit DMG":["cd",[12.6,13.8,15,16.2,17.4,18.6,19.8,21]],
            "Hp":["Hp",[320,360,390,430,470,510,540,580]],
            "Def%":["bonusDef",[8.1,9,10,10.9,11.8,12.8,13.8,14.7]],
            "Energy Regen":["er",[6.8,7.6,8.4,9.2,10,10.8,11.6,12.4]],
            "Atk":["Atk",[30,40,50,60]],
            "Def":["Def",[40,50,60,70]],
            "Hp%":["Hp",[6.4,7.1,7.9,8.6,9.4,10.1,10.9,11.6]],
            "BA Bonus":["bonusBA",[6.4,7.1,7.9,8.6,9.4,10.1,10.9,11.6]],
            "HA Bonus":["bonusHA",[6.4,7.1,7.9,8.6,9.4,10.1,10.9,11.6]],
            "RS Bonus":["bonusRS",[6.4,7.1,7.9,8.6,9.4,10.1,10.9,11.6]],
            "RL Bonus":["bonusRL",[6.4,7.1,7.9,8.6,9.4,10.1,10.9,11.6]],
            "Atk%":["bonusAtk",[6.4,7.1,7.9,8.6,9.4,10.1,10.9,11.6] ] 
        }
        
        
        self.mainStatDict={
            "Atk 18%":["Atk%","bonusAtk",18],
            "Def 18%":["Def%","bonusDef",18],
            "Hp 22.8%":["Hp%","bonusHp",22.8],
            
            "Atk 30%":["Atk%","bonusAtk",30],
            "Def 38%":["Def%","bonusDef",38],
            "Hp 30%":["Hp%","bonusHp",30],
            "Spectro DMG Bonus 30%":["Spectro DMG bonus","bonusSpectro",30],
            "Aero DMG Bonus 30%":["Aero DMG bonus","bonusAero",30],
            "Glacio DMG Bonus 30%":["Glacio DMG bonus","bonusGlacio",30],
            "Electro DMG Bonus 30%":["Electro DMG bonus","bonusElectro",30],
            "Havoc DMG Bonus 30%":["Havoc DMG bonus","bonusHavoc",30],
            "Fushion DMG Bonus 30%":["Fushion DMG bonus","bonusFushion",30],
            "Energy Regen 32%":["Energy Regen","er",32],
            
            "Crit Rate 22%":["Crit Rate","cr",22],
            "Crit DMG 44%":["Crit DMG","cd",44],
            "Atk 33%":["Atk%","bonusAtk",33],
            "Def 41.8%":["Def%","bonusDef",41.8],
            "Hp 33%":["Hp%","bonusHp",33]
            
        }
        
        
        self.staticStatDict={
            "1":["Hp","Hp",2280],
            "3":["Atk","Atk",100],
            "4":["Atk","Atk",150]
        }
        
        self.echoSetName=readTextFileToList("/data/echoSet.txt")
        self.cost=["1","3","4"]
        self.mainStatCost1=["Atk 18%","Def 18%","Hp 22.8%"]
        self.mainStatCost3=["Atk 30%","Def 38%","Hp 30%","Spectro DMG Bonus 30%","Aero DMG Bonus 30%",
                            "Glacio DMG Bonus 30%","Electro DMG Bonus 30%","Fushion DMG Bonus 30%",
                            "Havoc DMG Bonus 30%","Energy Regen 32%"]
        self.mainStatCost4=["Crit Rate 22%", "Crit DMG 44%","Atk 33%","Def 41.8%","Hp 33%"]
        
        # Create combobox
        self.costCombobox=[]
        self.mainStatCombobox=[]
        for i in range(5):
            costCombobox=NoScrollComboBox()
            mainStatCombobox=NoScrollComboBox()
            
            costCombobox.addItems(self.cost)
            mainStatCombobox.addItems(self.mainStatCost1)
            
            # Add combobox to a list
            self.costCombobox.append(costCombobox)
            self.mainStatCombobox.append(mainStatCombobox)
            
            costCombobox.currentTextChanged.connect(partial(self.updateMainStatSelecter,i))
            


        # Current number of echo saved
        self.curEchoIndex=self.currentEchoIndex()

        self.contentLayout.addWidget(UIDWidget)
        
        self.contentLayout.addWidget(self.chooseSet())
                
        # Add widget of each echo to contentLayout
        self.contentLayout.addWidget(QLabel("Echo 1"))
        self.contentLayout.addWidget(self.echo(0))
        
        self.contentLayout.addWidget(QLabel("Echo 2"))
        self.contentLayout.addWidget(self.echo(1))
        
        self.contentLayout.addWidget(QLabel("Echo 3"))
        self.contentLayout.addWidget(self.echo(2))
        
        self.contentLayout.addWidget(QLabel("Echo 4"))
        self.contentLayout.addWidget(self.echo(3))
        
        self.contentLayout.addWidget(QLabel("Echo 5"))
        self.contentLayout.addWidget(self.echo(4))
    

        self.scroll.setWidget(self.contentWidget)


        self.mainLayout.addWidget(self.scroll)


    

    def currentEchoIndex(self):
        uid=self.UIDCombobox.currentText()
        if os.path.exists(f"{ROOT_DIR}/save/{uid}/echo.json"):
            
            data=readJson(f"save/{uid}/echo.json",ROOT_DIR)
            if data==None:
                return 0
            else:
                i=0
                for key,val in data.items():
                    i+=1
                return i
        else:
            return 0
        
        
    def chooseSet(self):
        widget=QWidget()
        layout=QVBoxLayout(widget)
        
        self.setSelecter=NoScrollComboBox()
        self.setSelecter.addItems(self.echoSetName)
        buff=[QCheckBox("None") for _ in range(5)]

        
        def removeAllCheckboxes(layout):
            for i in reversed(range(layout.count())):
                item = layout.itemAt(i)
                widget = item.widget()
                if isinstance(widget, QCheckBox):
                    layout.removeWidget(widget)
                    widget.setParent(None)
                elif isinstance(widget, QWidget):
                    # Nếu là widget khác, kiểm tra xem nó có layout con không
                    childLayout = widget.layout()
                    if childLayout:
                        removeAllCheckboxes(childLayout)
        
        
        
        def setNone(checkboxARR):
            for cb in checkboxARR:
                cb.setText("None")
        def updateBuff():
            data=readJson(f"data/echo/{self.setSelecter.currentText()}.json",ROOT_DIR)
            if data!=None:
                i=0
                for tag,val in data.items():
                    if tag.startswith("Buff"):
                        buff[i].setText(val[0])
                    i+=1
            else:
                setNone(buff)
            removeAllCheckboxes(layout)
            addCheckBox()
        
        self.setSelecter.currentTextChanged.connect(updateBuff)
        layout.addWidget(self.setSelecter)
        
        def addCheckBox():
            for i in range(5):
                if buff[i].text()!="None":
                    layout.addWidget(buff[i])   
                            

        
        return widget
        

    def cost4Buff(self):
        self.cost4BuffCombobox=NoScrollComboBox()
        self.cost4BuffCombobox.addItems(self.subStat)

        widget=QWidget()
        layout=QHBoxLayout(widget)
        layout.addWidget(self.cost4BuffCombobox)
        return widget


    def updateMainStatSelecter(self,idx):
        if self.costCombobox[idx].currentText()=="1":
            self.mainStatCombobox[idx].clear()
            self.mainStatCombobox[idx].addItems(self.mainStatCost1)
            
        if self.costCombobox[idx].currentText()=="3":
            self.mainStatCombobox[idx].clear()
            self.mainStatCombobox[idx].addItems(self.mainStatCost3)
            
        if self.costCombobox[idx].currentText()=="4":
            self.mainStatCombobox[idx].clear()
            self.mainStatCombobox[idx].addItems(self.mainStatCost4)       


    def echo(self,idx):
        
        echoWidget=QWidget()
        layout=QVBoxLayout(echoWidget)
        a,a1,a2=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.subStat)
        b,b1,b2=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.subStat)
        c,c1,c2=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.subStat)
        d,d1,d2=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.subStat)
        e,e1,e2=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.subStat)


        
        def saveEcho():
            data={
                "Set name":self.setSelecter.currentText(),
                "Name":name.currentText(),
                "Cost":int(self.costCombobox[idx].currentText()),
                "Main stat 1":self.mainStatDict[self.mainStatCombobox[idx].currentText()],
                
                "Main stat 2":self.staticStatDict[self.costCombobox[idx].currentText()],
                
                "Sub stat 1":[a2.currentText(),self.subStatDict[a2.currentText()][0],self.subStatDict[a2.currentText()][1][a1.value()]],
                
                "Sub stat 2":[b2.currentText(),self.subStatDict[b2.currentText()][0],self.subStatDict[b2.currentText()][1][b1.value()]],
                
                "Sub stat 3":[c2.currentText(),self.subStatDict[c2.currentText()][0],self.subStatDict[c2.currentText()][1][c1.value()]],
                
                "Sub stat 4":[d2.currentText(),self.subStatDict[d2.currentText()][0],self.subStatDict[d2.currentText()][1][d1.value()]],
                
                "Sub stat 5":[e2.currentText(),self.subStatDict[e2.currentText()][0],self.subStatDict[e2.currentText()][1][e1.value()]]
            }
            reply = QMessageBox.question(None, "Save", 
                           "Do you want to save echo",
                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                self.curEchoIndex=self.currentEchoIndex()
                appendJson(self.curEchoIndex,data,f"save/{self.UIDCombobox.currentText()}/echo.json",ROOT_DIR)
                self.curEchoIndex=self.currentEchoIndex()
        
        saveBtn=QPushButton("Save")
        saveBtn.clicked.connect(partial(saveEcho))
        widget,name=self.chooseMainStat(idx)
        layout.addWidget(widget)
        layout.addWidget(a)
        layout.addWidget(b)
        layout.addWidget(c)
        layout.addWidget(d)
        layout.addWidget(e)
        layout.addWidget(saveBtn)
        
        return echoWidget
    
    
    
    def chooseMainStat(self,idx):
        mainStatWiget=QWidget()
        layout=QGridLayout(mainStatWiget)           
        layout.addWidget(self.costCombobox[idx],1,0)
        layout.addWidget(self.mainStatCombobox[idx],1,1)
        mainStatLabel=QLabel("")
        mainStatVal=QLabel("")
        nameCombobox=QComboBox()
        nameCombobox.addItems(["None"])
        
        
        mainStatLabel.setText(self.staticStatDict[self.costCombobox[idx].currentText()][0])
        mainStatVal.setText(str(self.staticStatDict[self.costCombobox[idx].currentText()][1]))
                    
        def updateLabel():
            mainStatLabel.setText(self.staticStatDict[self.costCombobox[idx].currentText()][0])
            mainStatVal.setText(str(self.staticStatDict[self.costCombobox[idx].currentText()][1]))

        def updateName():
            if self.setSelecter.currentText() in self.echoName:
                nameCombobox.clear()
                nameCombobox.addItems(self.echoName[self.setSelecter.currentText()])

        self.setSelecter.currentTextChanged.connect(updateName)
        self.costCombobox[idx].currentTextChanged.connect(updateLabel)   
        layout.addWidget(nameCombobox,0,0,1,2)
        layout.addWidget(mainStatLabel,2,0,1,1)
        layout.addWidget(mainStatVal,2,1,1,1)   

        return mainStatWiget,nameCombobox
         
        
    
        
        
    def createSteppedSliderWithComboBox(self, min_val: float, max_val: float, step: float, combo_options=None):
        if combo_options is None:
            combo_options = ["On", "Off"]

        steps = int((max_val - min_val) / step)

        # Tạo widget cha để chứa toàn bộ combo + label + slider
        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)

        # ComboBox
        combo = NoScrollComboBox()
        combo.addItems(combo_options)

        # Label và slider
        label = QLabel(f"{min_val:.1f}")
        slider = NoScrollSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(steps)
        slider.setSingleStep(1)
        slider.setTickInterval(2)
        slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        realVal=6.3

        critRateRange=[6.3,6.9,7.5,8.1,8.7,9.3,9.9,10.5]
        critDmgRange=[12.6,13.8,15,16.2,17.4,18.6,19.8,21]
        hpRange=[320,360,390,430,470,510,540,580]
        defPRange=[8.1,9,10,10.9,11.8,12.8,13.8,14.7]
        bonusRange=[6.4,7.1,7.9,8.6,9.4,10.1,10.9,11.6]
        erRange=[6.8,7.6,8.4,9.2,10,10.8,11.6,12.4]
        atkFlatRange=[30,40,50,60]
        defFlatRange=[40,50,60,70]

        def updateLabel(i):
            label.setText(str(self.subStatDict[combo.currentText()][1][slider.value()]))
            

        def comboChanged():
        
            if combo.currentText()=="Atk" or combo.currentText()=="Def":
                slider.setMinimum(0)
                slider.setMaximum(len(defFlatRange)-1)
                slider.setSingleStep(1)
                slider.setTickInterval(2)
                slider.setTickPosition(QSlider.TickPosition.TicksBelow)
            else:
                slider.setMinimum(0)
                slider.setMaximum(len(bonusRange)-1)
                slider.setSingleStep(1)
                slider.setTickInterval(2)
                slider.setTickPosition(QSlider.TickPosition.TicksBelow)                
                
            slider.setValue(0)
            updateLabel(0)

        slider.valueChanged.connect(partial(updateLabel))
        combo.currentIndexChanged.connect(comboChanged)

        # Thêm các widget vào layout
        layout.addWidget(combo)
        layout.addWidget(label)
        layout.addWidget(slider)

        return container,slider,combo

