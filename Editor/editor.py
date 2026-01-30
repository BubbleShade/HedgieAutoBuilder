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
        vbox = SideBar()

        self.scene = AutoBuilderScene(vbox)
    
        

        view = QGraphicsView(self.scene)
        view.setRenderHint(QPainter.RenderHint.Antialiasing)

        hbox = QHBoxLayout(self)
        hbox.addLayout(vbox)
        hbox.addWidget(view)
        self.setStyleSheet(Styles.editorStyle)
        Container.addLayout(topGuy)
        Container.addLayout(hbox)

        self.setLayout(Container)

        self.fileMenu = QMenu()
        self.fileMenu.setStyleSheet(Styles.contextMenuStyle)
        saveButton = self.fileMenu.addAction("Save As...")
        saveButton.triggered.connect(self.scene.save_as)
        openButton = self.fileMenu.addAction("Open File...")
        openButton.triggered.connect(self.scene.open)
        self.show()
        
        
    def show(self):
        super().show()
        titleBar : CustomTitleBar = self.parent().titleBar
        titleBar.fileButton.pressed.connect(lambda : self.fileMenu.exec(titleBar.fileButton.mapToGlobal(QPoint(0,32))))
        
        
    