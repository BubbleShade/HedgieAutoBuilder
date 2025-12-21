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
from . import Arrow
from . import BezierHandle
class PoseDisplay(QGraphicsItem):
    def __init__(self, scene : QGraphicsScene):
        super().__init__()

        self.handle1 = BezierHandle(self)

        # Draw a rectangle item, setting the dimensions.
        self.rectangle = QGraphicsRectItem(0,0,30,30, self)
        self.rectangle.setPos(-15,-15)
        self.arrow = Arrow(QPointF(15, 4), QPointF(15, 26), self.rectangle)


        #self.arrow.setPos(50, 20)
        #scene.addItem(self.arrow)
        brush = QBrush(Qt.GlobalColor.transparent)
        self.rectangle.setBrush(brush)

        # Define the pen (line)
        pen = QPen(Qt.GlobalColor.green)
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        self.arrow.setPen(pen)

        self.rectangle.setPen(pen)
        self.rectangle.setTransformOriginPoint(self.rectangle.boundingRect().center())

        self.scene : QGraphicsScene = scene
        scene.addItem(self)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.rectangle.mouseMoveEvent = self.mouseMoveEvent
        self.rectangle.mousePressEvent = self.mousePressEvent
        self.rectangle.mouseReleaseEvent = self.mouseReleaseEvent
        self.rectangle.wheelEvent = self.wheelEvent
        self.rectangle.contextMenuEvent = self.contextMenuEvent

        #self.arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        #self.arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        
    def wheelEvent(self, QWheelEvent):
        if(not self.isSelected()): return
        #print(QWheelEvent.delta() * 1)
        self.rectangle.setRotation(self.rectangle.rotation() + ((1/8)*QWheelEvent.delta()))

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.scene.clearSelection()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        #self.scene.clearSelection()
    def contextMenuEvent(self, event):
        context_menu = QMenu()
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = context_menu.addAction("Delete")
        deleteButton.triggered.connect(self.delete)
        
        context_menu.exec(event.screenPos())
        #event.setAccepted(True)

        #return super().contextMenuEvent(event)
            
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if(not self.isSelected()): return
    def delete(self):
        self.scene.removeItem(self)
    def center(self):
        return self.pos()
    
    def update(self):
        self.scene.update()

