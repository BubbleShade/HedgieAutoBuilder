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
class PoseDisplay(QGraphicsRectItem):
    def __init__(self, scene : QGraphicsScene):
        super().__init__(0, 0, 30, 30)

        # Draw a rectangle item, setting the dimensions.
        self.arrow = Arrow(QPointF(15, 4), QPointF(15, 26), self)

        #self.arrow.setPos(50, 20)
        #scene.addItem(self.arrow)
        brush = QBrush(Qt.GlobalColor.transparent)
        self.setBrush(brush)

        # Define the pen (line)
        pen = QPen(Qt.GlobalColor.green)
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        self.arrow.setPen(pen)

        self.setPen(pen)
        self.setTransformOriginPoint(self.boundingRect().center())

        self.scene : QGraphicsScene = scene
        scene.addItem(self)

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        

        


        #self.arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        #self.arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        
    def wheelEvent(self, QWheelEvent):
        if(not self.isSelected()): return
        #print(QWheelEvent.delta() * 1)
        self.setRotation(self.rotation() + ((1/8)*QWheelEvent.delta()))
    def mousePressEvent(self, e):
        self.scene.clearSelection()
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.scene.clearSelection()
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
        return QPointF(self.x() + self.rect().width()/2, self.y() + self.rect().height()/2)

