import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QPainter, QPen, QContextMenuEvent
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
    QMenu
)
#from . import PoseDisplay
from . import PoseDisplay
import Styles



class PoseLabel(QLabel):
    def __init__(self, name : str, pose = None, parent : QVBoxLayout = None):
        super().__init__(name)
        self.pose = pose
        self.parentGuy = parent
    def contextMenuEvent(self, event : QContextMenuEvent):
        context_menu = QMenu()
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = context_menu.addAction("Delete")
        deleteButton.triggered.connect(self.delete)
        context_menu.exec(event.globalPos()) 
        print(event.pos())
    def delete(self):
        if(self.pose != None): self.pose.delete()
        print("hello")
        self.parentGuy.removeWidget(self)

class PathLabel(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.poseLayout = QVBoxLayout()
        self.poses = []
        self.addWidget(QLabel("Follow Path: "))
        self.addLayout(self.poseLayout)
    def addPose(self, name : str, pose : PoseDisplay = None):
        poseLabel = PoseLabel(name, pose=pose, parent=self.poseLayout)
        self.poses.append(poseLabel)
        self.poseLayout.addWidget(poseLabel)

class SideBar(QVBoxLayout):
    def __init__(self, parent = None):
        super().__init__(parent) 

        self.PathLabel1  = PathLabel()
        self.addLayout(self.PathLabel1)
        

        up = QPushButton("Up")
        #up.clicked.connect(self.up)
        self.addWidget(up)

        down = QPushButton("Down")
        #down.clicked.connect(self.down)
        self.addWidget(down)

        rotate = QSlider()
        rotate.setRange(0, 360)
        #rotate.valueChanged.connect(self.rotate)
        self.addWidget(rotate)
    def CreatePoseLabel(self, name, pose):
        PoseLabel(name, pose)
