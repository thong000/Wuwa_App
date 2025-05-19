import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout,QMessageBox,QSizePolicy,
QLabel,QCheckBox,QHBoxLayout,QSlider,QGridLayout,QComboBox,QScrollArea,QVBoxLayout,QPushButton,QTabWidget

)
from functools import partial
from PyQt6.QtCore import Qt,QSize
from watchdog.observers import Observer
from PyQt6.QtGui import QPixmap,QIcon
from const import ROOT_DIR
from core.fileHandler import (readTextFileToList,readJson,appendJson,
                              FileTracking,removeKeyByShift,getVal,change_val_json)
from PyQt6.QtCore import pyqtSignal

class NoScrollComboBox(QComboBox):
    def wheelEvent(self, event):
        event.ignore() 
class NoScrollSlider(QSlider):
    def wheelEvent(self, event):
        event.ignore()
   
class Inventory(QWidget):
    def __init__(self):
        super().__init__()
        self.tabs=QTabWidget()
        self.mainLayout=QVBoxLayout(self)
        self.mainLayout.addWidget(self.tabs)
        
        # Add tab to Inventory
        self.tabs.addTab(EchoInventory(),"Echo inventory")



class EchoStat(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.Dialog) 
        self.setWindowModality(Qt.WindowModality.ApplicationModal) 
        self.mainLayout = QVBoxLayout(self)

        self.sub_stat_list=["Crit Rate","Crit DMG","Atk%","Atk","Hp%","Hp","Def%","Def","BA Bonus",
                    "HA Bonus","RS Bonus","RL Bonus","Energy Regen"]
        self.sub_stat_dict={
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
        
        
        self.costCombobox=NoScrollComboBox() # Choose cost
        self.mainStatCombobox=NoScrollComboBox() # Choose main stat
        # Add value to comboboxs
        self.costCombobox.addItems(self.cost)
        self.mainStatCombobox.addItems(self.mainStatCost1)   
        self.costCombobox.currentTextChanged.connect(partial(self.updateMainStatSelecter))
        self.setSelect=NoScrollComboBox()
        self.setSelect.addItems(self.echoSetName)  
        # Add widget   
        self.mainLayout.addWidget(self.echo())

    

    def currentEchoIndex(self):
        uid=getVal("curUID","config.json",ROOT_DIR)
        print(f"{uid=}")
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
        
        

    def updateMainStatSelecter(self):
        if self.costCombobox.currentText()=="1":
            self.mainStatCombobox.clear()
            self.mainStatCombobox.addItems(self.mainStatCost1)
            
        if self.costCombobox.currentText()=="3":
            self.mainStatCombobox.clear()
            self.mainStatCombobox.addItems(self.mainStatCost3)
            
        if self.costCombobox.currentText()=="4":
            self.mainStatCombobox.clear()
            self.mainStatCombobox.addItems(self.mainStatCost4)       


    def setSelecter(self):
        setWidget=QWidget()
        setLayout=QVBoxLayout(setWidget)
        setLayout.addWidget(self.setSelect)
        return setWidget
         
    def echo(self):
        echoWidget=QWidget()
        layout=QVBoxLayout(echoWidget)

        
        sliderWidget_1,slider_1,subStat_1=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.sub_stat_list)
        sliderWidget_2,slider_2,subStat_2=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.sub_stat_list)
        sliderWidget_3,slider_3,subStat_3=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.sub_stat_list)
        sliderWidget_4,slider_4,subStat_4=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.sub_stat_list)
        sliderWidget_5,slider_5,subStat_5=self.createSteppedSliderWithComboBox(6.3,10.5,0.6,self.sub_stat_list)


        
        def saveEcho():
            data={
                "Set name":self.setSelect.currentText(),
                "Name":name.currentText(),
                "Cost":int(self.costCombobox.currentText()),
                "Main stat 1":self.mainStatDict[self.mainStatCombobox.currentText()],
                
                "Main stat 2":self.staticStatDict[self.costCombobox.currentText()],
                
                "Sub stat 1":[subStat_1.currentText(),self.sub_stat_dict[subStat_1.currentText()][0],self.sub_stat_dict[subStat_1.currentText()][1][slider_1.value()]],
                
                "Sub stat 2":[subStat_2.currentText(),self.sub_stat_dict[subStat_2.currentText()][0],self.sub_stat_dict[subStat_2.currentText()][1][slider_2.value()]],
                
                "Sub stat 3":[subStat_3.currentText(),self.sub_stat_dict[subStat_3.currentText()][0],self.sub_stat_dict[subStat_3.currentText()][1][slider_3.value()]],
                
                "Sub stat 4":[subStat_4.currentText(),self.sub_stat_dict[subStat_4.currentText()][0],self.sub_stat_dict[subStat_4.currentText()][1][slider_4.value()]],
                
                "Sub stat 5":[subStat_5.currentText(),self.sub_stat_dict[subStat_5.currentText()][0],self.sub_stat_dict[subStat_5.currentText()][1][slider_5.value()]]
            }
            reply = QMessageBox.question(None, "Save", 
                           "Do you want to save echo",
                           QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply == QMessageBox.StandardButton.Yes:
                appendJson(self.currentEchoIndex(),data,f"save/{getVal("curUID","config.json",ROOT_DIR)}/echo.json",ROOT_DIR)

        
        saveBtn=QPushButton("Save")
        saveBtn.clicked.connect(partial(saveEcho))
        widget,name=self.chooseMainStat()
        layout.addWidget(self.setSelecter())
        layout.addWidget(widget)
        layout.addWidget(sliderWidget_1)
        layout.addWidget(sliderWidget_2)
        layout.addWidget(sliderWidget_3)
        layout.addWidget(sliderWidget_4)
        layout.addWidget(sliderWidget_5)
        layout.addWidget(saveBtn)
        
        return echoWidget
    
    
    
    def chooseMainStat(self):
        self.echo_name_dict=readJson("data/echo.json",ROOT_DIR)
        mainStatWiget=QWidget()
        layout=QGridLayout(mainStatWiget)           
        layout.addWidget(self.costCombobox,1,0)
        layout.addWidget(self.mainStatCombobox,1,1)
        mainStatLabel=QLabel("")
        mainStatVal=QLabel("")
        nameCombobox=QComboBox()
        nameCombobox.addItems(["None"])
        
        
        mainStatLabel.setText(self.staticStatDict[self.costCombobox.currentText()][0])
        mainStatVal.setText(str(self.staticStatDict[self.costCombobox.currentText()][1]))
                    
        def updateLabel():
            mainStatLabel.setText(self.staticStatDict[self.costCombobox.currentText()][0])
            mainStatVal.setText(str(self.staticStatDict[self.costCombobox.currentText()][1]))

        def updateName():
            if self.setSelect.currentText() in self.echo_name_dict:
                nameCombobox.clear()
                nameCombobox.addItems(self.echo_name_dict[self.setSelect.currentText()])

        self.setSelect.currentTextChanged.connect(updateName)
        self.costCombobox.currentTextChanged.connect(updateLabel)   
        layout.addWidget(nameCombobox,0,0,1,2)
        layout.addWidget(mainStatLabel,2,0,1,1)
        layout.addWidget(mainStatVal,2,1,1,1)   

        return mainStatWiget,nameCombobox
         
        
    
        
        
    def createSteppedSliderWithComboBox(self, min_val: float, max_val: float, step: float, combo_options=None):
        if combo_options is None:
            combo_options = ["On", "Off"]

        steps = int((max_val - min_val) / step)


        container = QWidget()
        layout = QHBoxLayout()
        container.setLayout(layout)


        subStatSelecter = NoScrollComboBox()
        subStatSelecter.addItems(combo_options)


        label = QLabel(f"{min_val:.1f}")
        slider = NoScrollSlider(Qt.Orientation.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(steps)
        slider.setSingleStep(1)
        slider.setTickInterval(1)

        slider.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


        def updateLabel():
            print(f"The value os slider has been changed to {str(self.sub_stat_dict[subStatSelecter.currentText()][1][slider.value()])}")
            label.setText(str(self.sub_stat_dict[subStatSelecter.currentText()][1][slider.value()]))
            

        def comboChanged():
            print(f"The combobox has been changed to {subStatSelecter.currentText()}")
            if subStatSelecter.currentText()=="Atk" or subStatSelecter.currentText()=="Def":
                slider.setMinimum(0)
                slider.setMaximum(3)
                slider.setSingleStep(1)
                slider.setTickInterval(1)
            else:
                slider.setMinimum(0)
                slider.setMaximum(7)
                slider.setSingleStep(1)
                slider.setTickInterval(1)
              
                
            slider.setValue(0)
            updateLabel()

        slider.valueChanged.connect(partial(updateLabel))
        subStatSelecter.currentIndexChanged.connect(comboChanged)

        layout.addWidget(subStatSelecter)
        layout.addWidget(label)
        layout.addWidget(slider)

        return container,slider,subStatSelecter     


        
class EchoInventory(QWidget):
    updateSignal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        
        self.scroll=QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.mainLayout=QGridLayout(self)
        
        widget=QWidget()
        layout=QVBoxLayout(widget)
        self.condition=["All cost","All set"]
        
        
        self.UIDCombobox=NoScrollComboBox()
        UIDList=readJson("config.json",ROOT_DIR)
        UIDList=UIDList["UID"]
        self.UIDCombobox.addItems(UIDList)
        UIDWidget=QWidget()
        UIDLayout=QVBoxLayout(UIDWidget)
        UIDLayout.addWidget(self.UIDCombobox)
        self.UIDCombobox.currentTextChanged.connect(self.sendUpdateSignal)
        
        trackFile=[]
        for uid in UIDList:
            trackFile.append(f"{ROOT_DIR}/save/{uid}/echo.json")
        self.observer = Observer()
        self.handlers = []
        i=0
        for file in trackFile:
            handler = FileTracking(filePath=file, callback=self.sendUpdateSignal)
            self.observer.schedule(handler, path=f"{ROOT_DIR}/save/{UIDList[i]}", recursive=False)
            self.handlers.append(handler)
            i+=1
        self.observer.start()


        layout.addWidget(UIDWidget)
        layout.addWidget(self.utilButton())
        self.filter=self.filterWidget()
        self.filter.hide()

        self.echoWidget = self.echoInventory()
        layout.addWidget(self.echoWidget)
        self.scroll.setWidget(widget)
        self.mainLayout.setColumnStretch(0, 0) 
        self.mainLayout.setColumnStretch(1, 3)
        self.addEcho=EchoStat()
        self.addEcho.hide()
        self.mainLayout.addWidget(self.scroll,0,1,1,3)

        
        self.updateSignal.connect(self.update)


    def sendUpdateSignal(self):
        for a in self.condition:
            print (a)
        self.updateSignal.emit(4)
     
    def send_decrese_elem_per_line(self):  
        self.updateSignal.emit(4) 
        
    def update(self,elem_per_line:int=4):
        change_val_json(f"config.json",ROOT_DIR,"curUID",self.UIDCombobox.currentText())
        self.echoWidget.setParent(None)
        self.echoWidget.deleteLater()

        self.echoWidget = self.echoInventory(elem_per_line)

        widget = self.scroll.widget()
        layout = widget.layout()
        layout.addWidget(self.echoWidget)
        
        
    def utilButton(self):
        util_widget=QWidget()
        util_layout=QHBoxLayout(util_widget)
        util_layout.stretch(1)
        filter_button=QPushButton("Filter")
        
        def hideFilter():
            if self.filter.isVisible():
                self.filter.hide()
            else:
                self.filter.show()
                
        filter_button.clicked.connect(hideFilter)
        
        add_button=QPushButton("Add")
        util_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        util_layout.addWidget(add_button)
        util_layout.addWidget(filter_button)
        def hideAddEcho():
            if self.addEcho.isVisible():
                self.sendUpdateSignal()
                self.addEcho.hide()
            else:
                self.send_decrese_elem_per_line()
                self.addEcho.show()    
                  
        add_button.clicked.connect(hideAddEcho)
        
        return util_widget
    def deleteEcho(self,i):
        removeKeyByShift(self.echoPath,str(i),ROOT_DIR)
    
    def is_meet_conditons(self,data:dict,conditions:list[str])->bool:
        cost_conditon:bool=True
        set_conditon:bool=True
        
        for condition in conditions:
            if condition=="All cost":
                cost_conditon=True
                break
            elif condition.startswith("Cost "):
                if str(data["Cost"])!=condition[-1]:
                    cost_conditon=False
                else:
                    cost_conditon=True
                    break
        for condition in conditions:
            if condition=="All set":
                set_conditon=True
                break
            if condition==data["Set name"]:
                set_conditon=True
                break
            else:
                set_conditon=False
        return set_conditon and cost_conditon
                
                
    def echoInventory(self,elem_per_line:int=4):
        widget = QWidget()
        layout = QGridLayout(widget)
        widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        
        self.echoPath = f"save/{self.UIDCombobox.currentText()}/echo.json"
        i = 0
        
        if os.path.exists(self.echoPath):
            data = readJson(self.echoPath, ROOT_DIR)
            for key, val in data.items():
                if self.is_meet_conditons(val,self.condition):
                    deleteButton = QPushButton("Delete")
                    deleteButton.clicked.connect(partial(self.deleteEcho, i=i))

                    
                    selectButton = QPushButton("Select")

                    
                    echoImgLabel = QLabel("No image")
                    echoImgPath = ROOT_DIR + f"/data/echo/{data[key]['Name']}.webp"
                    
                    if os.path.exists(echoImgPath):
                        echoImg = QPixmap(echoImgPath)
                        echoImg = echoImg.scaledToWidth(150) 
                        echoImgLabel.setPixmap(echoImg)
                        echoImgLabel.setFixedSize(echoImg.size()*0.8)
                        echoImgLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    

                    wg = QWidget()
                    wg.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                    wgLayout = QGridLayout(wg)
                    

                    wgLayout.setColumnStretch(0, 1)
                    wgLayout.setColumnStretch(1, 2)
                    

                    info = f"{data[key]['Set name']}\n{data[key]['Name']}\n\nCost: {data[key]['Cost']}"
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
                    
                    echoLabel = QLabel(info)

                    echoLabel.setWordWrap(True)
                    echoLabel.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                    echoLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                    

                    wgLayout.addWidget(echoImgLabel, 0, 0, 1, 1)
                    wgLayout.addWidget(echoLabel, 0, 1, 4, 1)
                    wgLayout.addWidget(deleteButton, 2, 0, 1, 1)
                    wgLayout.addWidget(selectButton, 3, 0, 1, 1)
                    

                    layout.addWidget(wg, (i // elem_per_line), (i % elem_per_line), 1, 1)
                    i += 1
        
        return widget 
    
    def filterWidget(self):
        filter_widget=QWidget()
        filter_layout=QGridLayout(filter_widget)
        filter_widget.setWindowFlags(Qt.WindowType.Dialog)
        filter_widget.setWindowModality(Qt.WindowModality.ApplicationModal)
        cost_checkbox_list=[QCheckBox() for _ in range(4)]
        cost_checkbox_list[0].setText("All cost")
        cost_checkbox_list[0].click()
        cost_checkbox_list[1].setText("Cost 1")
        cost_checkbox_list[2].setText("Cost 3")
        cost_checkbox_list[3].setText("Cost 4")
        
        
        def updateFilter(text):
            if text in self.condition:
                self.condition.remove(text)
            else:
                self.condition.append(text)
            self.sendUpdateSignal()
        
        for cb in cost_checkbox_list:
            cb.clicked.connect(partial(updateFilter,text=cb.text()))
        
        filter_layout.addWidget(QLabel("Cost"),0,0,1,1)
        filter_layout.addWidget(cost_checkbox_list[0],1,0,1,1)
        filter_layout.addWidget(cost_checkbox_list[1],1,1,1,1)
        filter_layout.addWidget(cost_checkbox_list[2],1,2,1,1)
        filter_layout.addWidget(cost_checkbox_list[3],1,3,1,1)
        
        
        
        

        
        self.echoset=readTextFileToList("/data/echoSet.txt")
        self.echoset[0]="All set"
        echoset_length:int=len(self.echoset)
        echoset_checkbox_list=[QCheckBox() for _ in range(echoset_length)]
        echoset_checkbox_list[0].click()
        i:int=0
        for checkbox in echoset_checkbox_list:
            checkbox.setText(self.echoset[i])
            checkbox.clicked.connect(partial(updateFilter,text= self.echoset[i]))
            i+=1
            
        i=0
        
        filter_layout.setSpacing(10)
        filter_layout.addWidget(QLabel("Echo Set"),2,0,1,1)
        for i in range(echoset_length):
            filter_layout.addWidget(echoset_checkbox_list[i],int(i/5)+3,int(i%5),1,1)
            i+=1
            
        return filter_widget
        
           
                    
