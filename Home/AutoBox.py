import sys

from PyQt6.QtCore import Qt, QPoint, QRectF, QSize
from PyQt6.QtGui import QBrush, QPainter, QPen, QMouseEvent
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
    QBoxLayout,
)
import json
from Editor import AutoViewer
#from . import PoseDisplay
import Styles
from Window import CustomTitleBar, CustomWindow

from Editor import Editor, Auto
class AutoBox(QVBoxLayout):
    def __init__(self, parent : QWidget, AutoJsonPath = "D:\\Programming\\HedgieAutoBuilder\\New folder\\banana.json"):
        super().__init__(parent)
        #autos : QGridLayout = self.parent.Autos
        #autos.addItem(self)
        self.name = QLabel(AutoJsonPath.split("\\")[-1].split(".")[0])
        self.path = AutoJsonPath
        self.addWidget(self.name)
        with open(AutoJsonPath, "r") as f:
            self.autoViewer = AutoViewer.fromJson(self, json.load(f), QRectF(0,0,190,170))
        self.view = QGraphicsView(self.autoViewer)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setMaximumSize(QSize(200,180))
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.guyFellow = parent

        self.addWidget(self.view)
        self.view.mouseReleaseEvent = self.mouseReleaseEvent
    def mouseReleaseEvent(self, event : QMouseEvent):
        if(event.button() == Qt.MouseButton.LeftButton):
            ed : Editor =self.guyFellow.editor
            ed.scene.changeAutoFromFile(self.path)
            ed.back = self.guyFellow
            self.guyFellow.parent().setFocus(self.guyFellow.editor)
        
    