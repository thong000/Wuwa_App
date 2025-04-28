from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,QTabWidget
)

from tabs.echoTab import EchoStatTab
from tabs.inventoryTab import Inventory
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

        self.tabs.addTab(EchoStatTab(),"Echo Tab")
        self.tabs.addTab(Inventory(),"Inventory Tab")
        

if __name__ == "__main__":
    app = QApplication([])
    window = DashboardApp()
    app.setStyleSheet("""
    QWidget {
        color: white;
        font-size: 14px;
        background-color: #212529;
    }
    QComboBox{
        border: 2px solid #6c757d;
        border-radius: 10px;
        padding: 5px;
    }
    QComboBox::drop-down { border: 0px; }
    QComboBox::down-arrow { width: 0px; height: 0px; }
    QPushButton {
        background-color: #4CAF50;  /* Màu xanh lá */
        color: white;
        border: none;
        padding: 8px 16px;
        font-size: 14px;
    }
    QPushButton:hover {
        background-color: #45a049;  /* Màu khi di chuột qua */
    }
    
    QPushButton:pressed {
        background-color: #3e8e41;  /* Màu khi nhấn */
    }
""")
    window.show()
    app.exec()
