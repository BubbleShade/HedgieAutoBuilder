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
from . import PoseDisplay
from . import Arrow
import Styles
from Editor.bezierCurve import BezierCurve
class AutoBuilderScene(QGraphicsScene):

    def __init__(self):
        super().__init__(0,0,200,200)

        # Add the items to the scene. Items are stacked in the order they are added.
        pose1 = PoseDisplay(self)
        pose1.setPos(50, 20)
        
        pose2 = PoseDisplay(self)
        pose2.setPos(125, 100)

        curve = BezierCurve(pose1.center(), pose2.center())
        self.addItem(curve)
        self.context_menu = QMenu()


        
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
        
    
        # Set all items as moveable and selectable.
        #for item in self.items():
            
