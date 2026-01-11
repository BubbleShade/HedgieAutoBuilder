import sys

from PyQt6.QtCore import Qt, QPointF, QPoint
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
    QMenu,
)
from . import PoseDisplay, SideBar, PoseLabel
import Styles
from Tools import BezierCurve
from .stuff import Pose, Auto, Path, Waypoint
class AutoBuilderScene(QGraphicsScene):

    def __init__(self, sideBar : SideBar):
        super().__init__(0,0,200,200)
        self.sideBar = sideBar

        # Add the items to the scene. Items are stacked in the order they are added.
        self.auto = Auto([Path(Pose(x=50,y=20), Pose(x=125,y=100),[Waypoint(x=200,y=200)])])

        self.auto.addToScene(self)
        self.auto.addToSideBar(self.sideBar)

        #pose1 = PoseDisplay(self)
        #pose1.setPos(50, 20)
        
        #pose2 = PoseDisplay(self)
        #pose2.setPos(125, 100)
        self.i = 3

        #self.sideBar.PathLabel1.addPose("Pose1", pose1)
        #self.sideBar.PathLabel1.addPose("Pose2", pose2)

        self.curves : list[BezierCurve] = []

        self.context_menu = QMenu()
        #self.sideBar.PathLabel1.poseLayout.orderChanged.connect(self.reBezier)
        #self.reBezier(self.sideBar.PathLabel1.poseLayout.get_item_data())


        
    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        if(event.isAccepted()): return
        context_menu = QMenu()
        context_menu.setAutoFillBackground(True)
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        addButton = context_menu.addAction("Add Pose")
        addWaypoint = context_menu.addAction("Add Waypoint")

        addButton.triggered.connect(lambda _:self.addPose(event.scenePos()))
        pos = AutoBuilderScene.calculateContextPosition(event.scenePos(), event.screenPos(), context_menu.width(), self.sceneRect().width())
        context_menu.exec(pos)
        
    def calculateContextPosition(eventScenePos : QPointF, eventScreenPos : QPoint, menuWidth : float, contextWidth: float) -> QPoint:
        print(f"scene pos: {eventScenePos}\n menu width: {menuWidth}\n context width: {contextWidth}")
        if(contextWidth + eventScenePos.x() > menuWidth):
            return (eventScreenPos- QPoint(menuWidth, 0))
        else: return eventScreenPos

    

    

    def addPose(self, position: QPointF):
        pose = PoseDisplay(self)
        pose.setPos(position)
        self.sideBar.PathLabel1.addPose(f"Pose {self.i}", pose=pose)
        self.i += 1
        
    
        # Set all items as moveable and selectable.
        #for item in self.items():
            
