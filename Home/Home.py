import sys, os

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QBrush, QPainter, QPen
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
    QMenu,
    QGridLayout,
    QLabel
)
#from . import PoseDisplay
import Styles, Tools

from Window import CustomTitleBar, CustomWindow
from . import AutoBox
from Editor import Editor

class Home(QWidget):
    def __init__(self, parent : CustomWindow, editor : Editor):
        print("HOMME")
        super(Home, self).__init__(parent)
        Container = QVBoxLayout(self)
        Container.addWidget(QLabel("Autos"))
        self.editor = editor

        self.Autos = QGridLayout(self)
        Container.addLayout(self.Autos)
        

        self.setLayout(Container)
        self.fileMenu = QMenu()

        self.fileMenu.setStyleSheet(Styles.contextMenuStyle)
    
        networkButton = self.fileMenu.addAction("Connect to NetworkTables...")
        networkButton.triggered.connect(Tools.networkTables.doit(self))

        #openButton.triggered.connect(self.scene.open)

        self.fileMenu.addSection("Bannan")
        publishButton = self.fileMenu.addAction("Publish")
        self.fileFun = None
        self.back = None

        self.updateLayouts()
        
        #publishButton.triggered.connect(self.scene.publish)



        #self.show()
    def updateLayouts(self):
        Tools.clear_layout(self.Autos)
        i = 0
        with os.scandir("D:\\Programming\\HedgieAutoBuilder\\New folder\\") as entries:
            for entry in entries:
                if entry.is_file():
                    print(entry.path)
                    if(entry.path.endswith(".json")):
                        self.Autos.addLayout(AutoBox(self, entry.path), int(i/5), i%5)
                        i+= 1
                        print(entry.path) # entry.path gives the full path to the file


        self.Autos.addLayout(AutoBox(self), 0,0)
        self.Autos.addLayout(AutoBox(self, "D:\\Programming\\HedgieAutoBuilder\\New folder\\gerbabble.json"), 0,1)
        

        
        
    def show(self):
        super().show()
        titleBar : CustomTitleBar = self.parent().titleBar
        titleBar.backButton.setHidden(self.back == None)
        
        self.fileFun = lambda : self.fileMenu.exec(titleBar.fileButton.mapToGlobal(QPoint(0,32)))
        titleBar.fileButton.pressed.connect(self.fileFun)
        self.updateLayouts()

    def hide(self):
        super().hide()
        titleBar : CustomTitleBar = self.parent().titleBar
        if(self.fileFun != None):
            titleBar.fileButton.pressed.disconnect(self.fileFun)
    
        
        
    