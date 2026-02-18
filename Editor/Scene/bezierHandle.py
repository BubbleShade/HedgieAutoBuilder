import sys

from PyQt6.QtCore import Qt, QPointF, QEvent, QRectF, QRectF
from PyQt6.QtGui import QBrush, QPainter, QPen, QPainterPath
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
from Tools import Line, unit, magnitude
import math
from .. import Action

class HandleGrip(QGraphicsEllipseItem):
    def __init__(self, parent, otherHandle : QGraphicsEllipseItem = None):
        super().__init__(0,0,10,10, parent)
        Styles.bezierHandleStyle.set_painter(self)
        self.parent = parent
        self.otherHandle = otherHandle
        self.startPos = self.pos()
    def centerPos(self):
        return self.pos() + self.rect().center()
    
    def setOtherPos(self):
        if(self.otherHandle != None): 
            otherPos = -unit(self.centerPos())*magnitude(self.otherHandle.centerPos())
            self.otherHandle.setCenterPos(otherPos)
    def setBothPos(self, pos : QPointF):
        self.setPos(pos)
        self.setOtherPos()

    def setCenterPos(self, pos : QPointF):
        self.setPos(pos - self.rect().center())

    def mousePressEvent(self, event):
        self.startPos = self.pos()
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.setOtherPos()
    
    def mouseReleaseEvent(self, event):
        Action.addAction(Action.Action(lambda: self.setBothPos(self.startPos), lambda: self.setBothPos(self.pos())))
        return super().mouseReleaseEvent(event)
        


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
    def hide(self):
        super().hide()
        self.handle1.hide()
        self.handle2.hide()
    
    def linePos1(self):
        if(not self.handle1.isVisible()): return QPointF(0,0)
        return self.handle1.centerPos()
    def linePos2(self):
        if(not self.handle2.isVisible()): return QPointF(0,0)
        return self.handle2.centerPos()
        
        
    def wheelEvent(self, QWheelEvent):
        if(not self.isSelected()): return
        #self.setRotation(self.rotation() + ((1/8)*QWheelEvent.delta()))
    def mousePressEvent(self, e):
        super().mousePressEvent(e)
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
    
    def hideHandles(self):
        self.handle1.hide()
        self.handle2.hide()

    def setHandleMode(self,handle1 : bool, handle2 : bool):
        if(self.isVisible()):
            self.handle1.setVisible(handle1)
            self.handle2.setVisible(handle2)
    def paint(self, painter, option, widget = ...): pass   
    def boundingRect(self): return QRectF(0,0,0,0)

    def delete(self): self.hide()
    def center(self): return self.pos()
