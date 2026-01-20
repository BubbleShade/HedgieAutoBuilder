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
    QMenu
)
import Styles
from Tools import Line
import math
#from . import Arrow
def magnitude(pos : QPointF): return math.sqrt(pow(pos.x(),2) + pow(pos.y(),2))
def unit(pos : QPointF): return pos / magnitude(pos)
class HandleGrip(QGraphicsEllipseItem):
    def __init__(self, parent, otherHandle : QGraphicsEllipseItem = None):
        super().__init__(0,0,10,10, parent)
        Styles.bezierHandleStyle.set_painter(self)
        self.parent = parent
        self.otherHandle = otherHandle
    def centerPos(self):
        return self.pos() + self.rect().center()
    def setCenterPos(self, pos : QPointF):
        self.setPos(pos - self.rect().center())
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if(not self.isSelected): return
        self.parent.parent.update()
        if(self.otherHandle != None): 
            otherPos = -unit(self.centerPos())*magnitude(self.otherHandle.centerPos())
            self.otherHandle.setCenterPos(otherPos)


class BezierHandle(QGraphicsItem):
    def __init__(self, parent : QGraphicsRectItem, pos : QPointF = QPointF(30,0)):
        super().__init__(parent)

        self.handle1 = HandleGrip(self)
        self.handle2 = HandleGrip(self, self.handle1)

        

        self.handle1.otherHandle = self.handle2

        # Draw a rectangle item, setting the dimensions.
        #self.arrow = Arrow(QPointF(15, 4), QPointF(15, 26), self)
        self.handle1.setCenterPos(pos + parent.center())
        self.handle1.setCenterPos(-pos + parent.center())
        self.setZValue(50)

        self.parent = parent


        self.line = Line(self.linePos1, self.linePos2, self)

        # Define the pen (line)
        #self.arrow.setPen(pen)

        
        pen = QPen(Styles.darkerGray)
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)

        self.line.setPen(pen)
        self.line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent)
        

        self.setTransformOriginPoint(self.boundingRect().center())

        self.handle1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.handle1.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.handle2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.handle2.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        #self.arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        #self.arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

    def linePos1(self):
        if(not self.handle1.isVisible()): return QPointF(0,0)
        return self.handle1.centerPos()
    def linePos2(self):
        if(not self.handle2.isVisible()): return QPointF(0,0)
        return self.handle2.centerPos()
        
        
    def wheelEvent(self, QWheelEvent):
        if(not self.isSelected()): return
        #print(QWheelEvent.delta() * 1)
        #self.setRotation(self.rotation() + ((1/8)*QWheelEvent.delta()))
    def mousePressEvent(self, e):
        super().mousePressEvent(e)
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
    
    def hideHandles(self):
        self.handle1.hide()
        self.handle2.hide()

    def setHandleMode(self,handle1 : bool, handle2 : bool):
        self.handle1.setVisible(handle1)
        self.handle2.setVisible(handle2)
    def paint(self, painter, option, widget = ...): pass   
    def boundingRect(self): return QRectF(0,0,0,0)

    def delete(self): self.hide()
    def center(self): return self.pos()
