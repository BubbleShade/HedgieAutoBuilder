import sys

from PyQt6.QtCore import Qt, QPointF, QEvent
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
    QGraphicsScene,
    QMenu
)
import Styles
from Tools import Arrow
from . import BezierHandle
class DraggableGraphicsItem(QGraphicsItem):
    def __init__(self, scene : QGraphicsScene, canRotate = True):
        super().__init__()
        self.canRotate = canRotate

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        
        self.scene : QGraphicsScene = scene
        scene.addItem(self)

    
    def wheelEvent(self, QWheelEvent):
        if(not self.isSelected()): return
        #print(QWheelEvent.delta() * 1)
        if(not self.canRotate): return
        self.rectangle.setRotation(self.rectangle.rotation() + ((1/8)*QWheelEvent.delta()))
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.scene.clearSelection()
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
            
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if(not self.isSelected()): return

    def delete(self):
        self.scene.removeItem(self)

    def center(self):
        return self.pos()
    
    def update(self):
        self.scene.update()
        


class PoseDisplay(DraggableGraphicsItem):
    def __init__(self, scene : QGraphicsScene, pose):
        super().__init__(scene, True)

        self.poseHandler = pose
        self.handle = BezierHandle(self)
        
        self.rectangle = QGraphicsRectItem(0,0,30,30, self)
        self.rectangle.setPos(-15,-15)
        self.arrow = Arrow(QPointF(15, 4), QPointF(15, 26), self.rectangle)

        brush = QBrush(Qt.GlobalColor.transparent)
        self.rectangle.setBrush(brush)

        # Define the pen (line)
        pen = QPen(Qt.GlobalColor.green) 
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        self.arrow.setPen(pen)

        self.rectangle.setPen(pen)
        self.rectangle.setTransformOriginPoint(self.rectangle.boundingRect().center())

        self.rectangle.mouseMoveEvent = self.mouseMoveEvent
        self.rectangle.mousePressEvent = self.mousePressEvent
        self.rectangle.mouseReleaseEvent = self.mouseReleaseEvent
        self.rectangle.wheelEvent = self.wheelEvent
        self.rectangle.contextMenuEvent = self.contextMenuEvent
    def contextMenuEvent(self, event):
        context_menu = QMenu()
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = context_menu.addAction("Delete")
        deleteButton.triggered.connect(self.delete)
        
        context_menu.exec(event.screenPos())
        #event.setAccepted(True)
        #return super().contextMenuEvent(event)
        
class WaypointDisplay(DraggableGraphicsItem):
    def __init__(self, scene : QGraphicsScene, waypoint):
        super().__init__(scene, False)

        self.handle = BezierHandle(self)
        
        self.circle = QGraphicsEllipseItem(0,0,15,15, self)
        self.circle.setPos(-7.5,-7.5)
        #self.arrow = Arrow(QPointF(15, 4), QPointF(15, 26), self.circle)

        brush = QBrush(Styles.toothpasteWhite)
        self.circle.setBrush(brush)

        # Define the pen (line)
        pen = QPen(Styles.darkerGray) 
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        #self.arrow.setPen(pen)

        self.circle.setPen(pen)
        self.circle.setTransformOriginPoint(self.circle.boundingRect().center())


        
        self.circle.mouseMoveEvent = self.mouseMoveEvent
        self.circle.mousePressEvent = self.mousePressEvent
        self.circle.mouseReleaseEvent = self.mouseReleaseEvent
        self.circle.wheelEvent = self.wheelEvent
        self.circle.contextMenuEvent = self.contextMenuEvent

    def contextMenuEvent(self, event):
        context_menu = QMenu()
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = context_menu.addAction("Delete")
        deleteButton.triggered.connect(self.delete)
        
        context_menu.exec(event.screenPos())
        #event.setAccepted(True)
        #return super().contextMenuEvent(event)

    
    
