import sys

from PyQt6.QtCore import Qt, QPointF, QEvent, QRectF
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
    QMenu,
)
import Styles
from Tools import Arrow, ArrowDrawer
from . import BezierHandle
class DraggableGraphicsItem(QGraphicsItem):
    def __init__(self, scene : QGraphicsScene, canRotate = True):
        super(DraggableGraphicsItem, self).__init__()
        self.canRotate = canRotate

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.scene : QGraphicsScene = scene
    
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

class PointDisplay(DraggableGraphicsItem):
    def poseRect(self): return QRectF(-15,-15,30,30)
    def waypointRect(self): return QRectF(-10,-10,20,20)
    def __init__(self, scene : QGraphicsScene, guy, has_rotation :bool = False):
        super(PointDisplay, self).__init__(scene)
        self.handle = BezierHandle(self)
        self.setHasRotation(has_rotation)
        self.arrow = ArrowDrawer(QPointF(0, -11), QPointF(0, 11))
        
        self.pen = QPen(Styles.toothPasteGray)
        self.pen.setWidth(3)
        
        
        print(scene)
        scene.addItem(self)
    def drawPose(self, painter : QPainter, option, widget = ...):
        painter.setPen(self.pen)
        painter.drawRect(self.boundingRect())
        self.arrow.paint(painter ,option)  
    def drawWapoint(self, painter : QPainter, option, widget = ...):
        painter.setPen(self.pen)
        painter.drawEllipse(self.boundingRect())

    def setHasRotation(self, has_rotation):
        self.has_rotation = has_rotation
        if(has_rotation):
            self.paint = self.drawPose
            self.boundingRect = self.poseRect
        else:
            self.paint = self.drawWapoint    
            self.boundingRect = self.waypointRect

        
        

    def contextMenuEvent(self, event):
        context_menu = QMenu()
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = context_menu.addAction("Delete")
        deleteButton.triggered.connect(self.delete)
        
        context_menu.exec(event.screenPos())

    
