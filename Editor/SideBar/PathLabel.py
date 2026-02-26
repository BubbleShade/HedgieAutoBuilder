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
    QFrame, QMenu
)
import Styles, Tools
from . import DragWidget, WaypointSidebarItem

class PathSidebarItem(QFrame):
    def __init__(self, handler):
        super().__init__()
        self.handler = handler
        self.poseLayout = DragWidget()
        self.poses = []
        self.pathLabel = QLabel("Follow Path: ")
        self.lay = QHBoxLayout()
        self.lay.addWidget(self.pathLabel)
        self.poseLayout.setMaximumHeight(50)
        self.lay.addWidget(self.poseLayout)
        self.setLayout(self.lay)
        self.i = 0
        self.context = QMenu()
        self.addPathBelow = self.context.addAction("Add Path Below")
        self.context.addSection("Bannana")
        self.deleteButton = self.context.addAction("Delete Path")
        self.context.setStyleSheet(Styles.contextMenuStyle)

    def contextMenuEvent(self, event):
        self.context.exec(event.globalPos()) 

    def addPoseLabel(self, poseLabel):
        poseLabel.parentLayout = self
        self.poses.append(poseLabel)
        self.poseLayout.setMaximumHeight(50 * len(self.poses))

        self.poseLayout.add_item(poseLabel)
    def hide(self):
        super().hide()
        #self.hide()
        #Tools.clear_layout(self.lay)

    def create_waypoint_label(self, waypoint, name = None):
        if(name == None):
            self.i += 1
            return WaypointSidebarItem(f"Waypoint {self.i}", waypoint)
        return WaypointSidebarItem(name, waypoint)
