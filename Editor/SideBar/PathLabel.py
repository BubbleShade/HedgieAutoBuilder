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
    QLabel
)
import Styles, Tools
from . import DragWidget, WaypointSidebarItem

class PathSidebarItem(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.poseLayout = DragWidget()
        self.poses = []
        self.pathLabel = QLabel("Follow Path: ")
        self.addWidget(self.pathLabel)
        self.poseLayout.setMaximumHeight(50)
        self.addWidget(self.poseLayout)
        self.i = 0
    def addPoseLabel(self, poseLabel):
        poseLabel.parentLayout = self
        self.poses.append(poseLabel)
        self.poseLayout.setMaximumHeight(50 * len(self.poses))

        self.poseLayout.add_item(poseLabel)
    def hide(self):
        Tools.clear_layout(self)

    def create_waypoint_label(self, waypoint, name = None):
        if(name == None):
            self.i += 1
            return WaypointSidebarItem(f"Waypoint {self.i}", waypoint)
        return WaypointSidebarItem(name, waypoint)
