import sys

from PyQt6.QtCore import Qt
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
)
#from . import PoseDisplay
from . import AutoBuilderScene, SideBar
import Styles
class Editor(QWidget):
    def __init__(self, parent : None):
        super().__init__(parent)
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


    def printHi(self): print("hi")
    def up(self):
        """ Iterate all selected items in the view, moving them forward. """
        items = self.scene.selectedItems()
        for item in items:
            z = item.zValue()
            item.setZValue(z + 1)

    def down(self):
        """ Iterate all selected items in the view, moving them backward. """
        items = self.scene.selectedItems()
        for item in items:
            z = item.zValue()
            item.setZValue(z - 1)

    def rotate(self, value):
        """ Rotate the object by the received number of degrees. """
        items = self.scene.selectedItems()
        for item in items:
            item.setRotation(value)