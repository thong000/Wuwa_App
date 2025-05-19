from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,QTabWidget,QGridLayout
)
import traceback

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout,QPushButton,QScrollArea,QLineEdit,QLabel
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import sys
from core.statManager import Stat
from functools import partial


class InputStat(QWidget):
  def __init__(self,):
    super().__init__()
    self.main_layout=QVBoxLayout(self)
    self.content_widget=QWidget()
    self.content_layout=QGridLayout(self.content_widget)
    
    self.input=[]
    self.stat=["Mul increase","Base Atk","Base Hp","Base Def","Atk","Hp","Def","Atk%","Hp%","Def%","Crit Rate","Crit DMG",
               "Energy Regen",
               "Basic Attack DMG Bonus","Basic Attack DMG Amplify",
               "Heavy Attack DMG Bonus","Heavy Attack DMG Amplify",
               "Resonance Skill DMG Bonus","Resonance Skill DMG Amplify",
               "Resonance Liberation DMG Bonus","Resonance Liberation DMG Amplify",
               "Glacio DMG Bonus","Glacio DMG Amplify",
               "Fusion DMG Bonus","Fusion DMG Amplify",
               "Electro DMG Bonus","Electro DMG Amplify",
               "Aero DMG Bonus","Aero DMG Amplify",
               "Spectro DMG Bonus" ,"Spectro DMG Amplify",
               "Havoc DMG Bonus","Havoc DMG Amplify",
               "Healing Bonus",
               "Spectro Frazzle Amplify","Fusion Burst Amplify","Aero Erosion Amplify"]
    
    
    
    self.result=QLabel("0") 
    self.scale=QLineEdit()
    self.buff=QLineEdit()
    
    self.content_layout.addWidget(self.scale,0,3,1,3)
    self.content_layout.addWidget(self.buff,1,3,1,3)
    self.content_layout.addWidget(self.result,2,3,1,3)
     
    
    self.char_stat=Stat()
    def changeStat(attr:str,edit:QLineEdit):
        class_attr=["Mul","baseAtk","baseHp","baseDef","flatAtk","flatHp","flatDef","bonusAtk","bonusHp","bonusDef",
                  "cr","cd","er",
                  "bonusBA","ampBA","bonusHA","ampHA","bonusRS","ampRS",
                  "bonusRL","ampRL","bonusGlacio","ampGlacio","bonusFusion",
                  "ampFusion","bonusElectro","ampElectro","bonusAero","ampAero",
                  "bonusSpectro","ampSpectro","bonusHavoc","ampHavoc","healing",
                  "ampSpectroFrazzle","ampFusionBurst","ampAeroErosion"]
        index=self.stat.index(attr)
        self.char_stat.setStat(class_attr[index],edit.text())
        
        try:
          a={
            "scale":float(self.scale.text()),
            "scaleType":"Atk",
            "buff":self.buff.text().split(";")
          }
          self.result.setText(str(self.char_stat.dealDmg(a)))
        except Exception as e:
            print("Lỗi chi tiết:")
            traceback.print_exc() 
        
      

      
    
    i:int=0
    for label in self.stat:
      tmp2=QLineEdit("0")
      tmp2.textChanged.connect(partial(changeStat,attr=label,edit=tmp2))
      self.input.append(tmp2)
      tmp=QLabel(label)
      tmp.setStyleSheet("font: 15px;")
      self.content_layout.addWidget(tmp,i,0,1,1)
      self.content_layout.addWidget(tmp2,i,1,1,1)
      i+=1
    
    
    self.content_layout.setSpacing(20)
    self.scroll=QScrollArea(self)
    self.scroll.setWidget(self.content_widget)
    self.main_layout.addWidget(self.scroll)
    
    
    
     
     

        
class CalcTab (QWidget):
    def __init__(self,):
        super().__init__()
        

        
        self.main_layout=QGridLayout(self)
        
        self.main_layout.addWidget(InputStat())