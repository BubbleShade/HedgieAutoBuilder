import sys, os

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QBrush, QPainter, QPen, QIcon, QCursor
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
    QLabel,
    QFrame,
    QToolButton
)
#from . import PoseDisplay
import Styles, Tools

from Window import CustomTitleBar, CustomWindow
from . import AutoBox
from Editor import Editor


class Home(QFrame):
    def newAuto(self):
        self.editor.scene.changeAutoTo()
    def __init__(self, parent : CustomWindow, editor : Editor):
        super(Home, self).__init__(parent)
        Container = QVBoxLayout(self)
        TopBar = QHBoxLayout(self)
        TopBar.addWidget(QLabel("Autos"))
        self.addButton = QPushButton("+")
        self.addButton.setFixedSize(44,44)
        self.addButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.addButton.setToolTip("Create a new auto...")
        self.setStyleSheet(Styles.homeStyle)
        TopBar.addWidget(self.addButton)

        Container.addLayout(TopBar)

        self.editor = editor

        self.Autos = QGridLayout(self)
        self.Autos.setAlignment(Qt.AlignmentFlag.AlignTop)
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
                    if(entry.path.endswith(".json")):
                        self.Autos.addWidget(AutoBox(self, entry.path), int(i/5), i%5)
                        i+= 1


        
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
    
        
        
    