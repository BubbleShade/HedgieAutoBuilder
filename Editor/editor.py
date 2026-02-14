import sys

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
    QMenu
)
#from . import PoseDisplay
from . import AutoBuilderScene, SideBar
import Styles
from Window import CustomTitleBar, CustomWindow
class Editor(QWidget):
    def __init__(self, parent : CustomWindow):
        super().__init__(parent)
        self.parent : CustomWindow
        Container = QVBoxLayout(self)
        topGuy = QHBoxLayout(self)

        # Define our layout.
        sidBar = SideBar(self)

        self.scene = AutoBuilderScene(sidBar)


        
        

        view = QGraphicsView(self.scene)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)

        hbox = QHBoxLayout(self)
        hbox.addWidget(sidBar)
        hbox.addWidget(view)
        self.setStyleSheet(Styles.editorStyle)
        Container.addLayout(topGuy)
        Container.addLayout(hbox)

        self.setLayout(Container)

        self.fileMenu = QMenu()
        self.fileMenu.setStyleSheet(Styles.contextMenuStyle)
        saveAsButton = self.fileMenu.addAction("Save As...")
        saveAsButton.triggered.connect(self.scene.save_as)
        saveButton = self.fileMenu.addAction("Save")
        saveButton.triggered.connect(self.scene.save)

        self.fileMenu.addSection("Bannan")

        openButton = self.fileMenu.addAction("Open File...")
        openButton.triggered.connect(self.scene.open)

        self.fileMenu.addSection("Bannan")
        publishButton = self.fileMenu.addAction("Publish")
        publishButton.triggered.connect(self.scene.publish)
        self.fileFun = None
        self.backFun = None
        self.back = None

        self.hide()
        
        
    def show(self):
        super().show()
        titleBar : CustomTitleBar = self.parent().titleBar
        self.fileFun = lambda : self.fileMenu.exec(titleBar.fileButton.mapToGlobal(QPoint(0,32)))
        titleBar.fileButton.pressed.connect(self.fileFun)
        titleBar.backButton.setHidden(self.back == None)
        if(self.back != None):
            self.backFun = lambda : self.parent().setFocus(self.back)
            titleBar.backButton.pressed.connect(self.backFun)


        
    def hide(self):
        super().hide()
        titleBar : CustomTitleBar = self.parent().titleBar
        if(self.fileFun != None):
            titleBar.fileButton.pressed.disconnect(self.fileFun)
        if(self.backFun != None):
            titleBar.backButton.pressed.disconnect(self.backFun)

        
        
    