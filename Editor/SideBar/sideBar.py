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
    QLayout,
    QScrollArea
    
)
import Styles
from . import WaypointSidebarItem, CommandGroupSideBarItem, NamedCommandSidebarItem

class SideBar(QScrollArea):
    def __init__(self, parent = None):
        super().__init__(parent)         
        self.i = 0
        self.lay = QVBoxLayout()
        self.seqCommandGroup = CommandGroupSideBarItem("Whar")
        self.lay.addWidget(self.seqCommandGroup)
        self.setLayout(self.lay)
        self.setMaximumWidth(400)
        self.scene = None
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    
    def addSideBarWidget(self, sidebarWidget):
        self.seqCommandGroup.lay.addWidget(sidebarWidget)
    def addSideBarLayout(self, sidebarLayout):
        self.seqCommandGroup.lay.addLayout(sidebarLayout)
        #self.lay.setParent(self)

    def create_waypoint_label(self, waypoint, name = None):
        if(name == None):
            self.i += 1
            return WaypointSidebarItem(f"Waypoint {self.i}", waypoint)
        return WaypointSidebarItem(name, waypoint)
    def mousePressEvent(self, a0):
        a0.accept()
        return super().mousePressEvent(a0)