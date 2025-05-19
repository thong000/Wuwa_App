from enum import Enum
#from core.fileHandler import printDictPretty




class Basic(Enum):
    BASE = 0
    BONUS = 1
    FLAT = 2
    IGNORE =3
    
class Element(Enum):
    BONUS=0
    AMP=1
    IGNORE=2
    DOTAMP=3
class Ability(Enum):
    BONUS=0
    AMP=1
    
class Store(Enum):
    NAME=0
    TYPE=1
    VAL=2
    STATUS=3

def is_float(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False

class Stat:
    def __init__(self):
        self.baseAtk=0
        self.bonusAtk=0
        self.flatAtk=0
        
        self.baseDef=0
        self.bonusDef=0
        self.flatDef=0
        
        self.baseHp=0
        self.bonusHp=0
        self.flatHp=0
        
        self.Atk=0
        self.Def=0
        self.Hp=0
        
        self.bonusBA=0
        self.ampBA=0
        
        self.bonusHA=0
        self.ampHA=0
        
        self.bonusRS=0
        self.ampRS=0
        
        self.bonusRL=0
        self.ampRL=0
        
        
        self.bonusSpectro=0
        self.ampSpectro=0
        self.ampSpectroFrazzle=0
        
        self.bonusGlacio=0
        self.ampGlacio=0
        self.ampGlacioChafe=0
        
        self.bonusHavoc=0
        self.ampHavoc=0
        self.ampHavocBane=0
        
        self.bonusAero=0
        self.ampAero=0
        self.ampAeroErosion=0
        
        self.bonusFusion=0
        self.ampFusion=0
        self.ampFusionBurst=0
        
        self.bonusElectro=0
        self.ampElectro=0   
        self.ampElectroFlare=0  
        self.ampIntro=0
        self.ampOutro=0
        self.cd=150
        self.cr=5
        self.er=100
        self.ignoreDef=0
        self.level=90
        self.healing=0
        self.mul=0
       
    def update(self):
        self.Atk=self.baseAtk*(1+self.bonusAtk/100)+self.flatAtk 
        self.Def=self.baseDef*(1+self.bonusDef/100)+self.flatDef
        self.Hp=self.baseHp*(1+self.bonusHp/100)+self.flatHp
    def setStat(self,type,value):
        if is_float(value):
            if hasattr(self,type):
                setattr(self,type,float(value))

        
    def dealDmg(self,data:dict)-> int:
        
        def sumBonus(arr:list):
            total=0
            for elem in arr:
                if hasattr(self,elem) and elem.startswith("bonus"):
                    total+=getattr(self,elem)
            return total
        
        def sumAmp(arr:list):
            total=0
            for elem in arr:
                if hasattr(self,elem)and elem.startswith("amp"):
                    total+=getattr(self,elem)
            return total  




        main=0
        if data["scaleType"]=="Atk":
            main=self.baseAtk*(1+self.bonusAtk/100) + self.flatAtk
        elif data["scaleType"]=="Hp":
            main=self.baseHp*(1+self.bonusHp/100) + self.flatHp
        elif data["scaleType"]=="Def":
            main=self.baseDef*(1+self.bonusDef/100) + self.flatDef
            
        bonus=sumBonus(data["buff"])
        amp=sumAmp(data["buff"])
        crit=getattr(self,"cd")
        res=20
        scale=data["scale"]*(1+getattr(self,"mul"))
        
        result=main*(1+bonus/100)*(1+amp/100)*(crit/100)*(1-res/100)*(scale/100)*((800+8*90)/(800+8*90+(792+8*100)*(1)))
        
        return round(result)
        
        
        
        
         
                
    def addStatFromData(self,data):
        if isinstance(data,dict):
            for key,val in data.items():
                if key.startswith("Base"):
                    self.addStat(val[1],val[2])
                    self.update()

                     
    def addStat(self,type,value):
        if hasattr(self,type):
            setattr(self,type,value+getattr(self,type))
            self.update()
            
    def subStat(self,type,value):
        if hasattr(self,type):
            setattr(self,type,getattr(self,type)-value)   
            self.update()  
    def show(self):
        for key in self.__dict__:
            print(f"{key} : {getattr(self,key)}")        
     
        
        

