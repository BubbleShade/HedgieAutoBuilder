import sys

from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QBrush, QPainter, QPen, QContextMenuEvent, QDrag, QPixmap
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
    QLabel,
    QMenu,
    QLayout
    
)
import Styles
from . import WaypointLabel

class SideBar(QVBoxLayout):
    def __init__(self, parent = None):
        super().__init__(parent)         
        self.i = 0

    def addPathLabel(self, pathLabel):
        self.addLayout(pathLabel)
    def create_waypoint_label(self, waypoint, name = None):
        if(name == None):
            self.i += 1
            return WaypointLabel(f"Waypoint {self.i}", waypoint)
        return WaypointLabel(name, waypoint)