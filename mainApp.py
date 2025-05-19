from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,QTabWidget
)

from tabs.inventoryTab import Inventory
from tabs.gachaHistoryTab import GachaHistory
from tabs.dmgCalcTab import CalcTab

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl
import sys



class DashboardApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wuwa App")
        self.setGeometry(100, 60, 1200, 700)
        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        
        self.setCentralWidget(main_widget)

        main_layout = QHBoxLayout(main_widget)
        

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.tabs.addTab(Inventory(),"Inventory Tab")
        self.tabs.addTab(GachaHistory(),"Gacha History")
        self.tabs.addTab(CalcTab(),"Damage Calculator")

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardApp()
    
    window.show()
    app.exec()
