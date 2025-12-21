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
from Tools import Line
#from . import Arrow
class BezierHandle(QGraphicsEllipseItem):
    def __init__(self, parent : QGraphicsRectItem, pos : QPointF = QPointF(30,0)):
        super().__init__(0, 0, 10, 10, parent)

        # Draw a rectangle item, setting the dimensions.
        #self.arrow = Arrow(QPointF(15, 4), QPointF(15, 26), self)
        self.setPos(pos + parent.center())
        self.parent = parent

        #self.arrow.setPos(50, 20)
        #scene.addItem(self.arrow)
        self.line = Line(lambda _=None: - self.pos(), lambda _=None: self.rect().center(), self)
        self.line.setZValue(-100)

        # Define the pen (line)
        pen = QPen(Styles.toothPasteGray)
        pen.setWidth(2)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        #self.arrow.setPen(pen)

        self.setPen(pen)
        
        pen = QPen(Styles.darkerGray)
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)

        self.line.setPen(pen)
        self.line.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent)

        brush = QBrush(Styles.toothpasteWhite)
        self.setBrush(brush)



        self.setTransformOriginPoint(self.boundingRect().center())

        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        

        


        #self.arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        #self.arrow.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        
    def wheelEvent(self, QWheelEvent):
        if(not self.isSelected()): return
        #print(QWheelEvent.delta() * 1)
        #self.setRotation(self.rotation() + ((1/8)*QWheelEvent.delta()))
    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        #self.scene.clearSelection()
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
        self.parent.update()

    def delete(self): self.hide()
        #self.scene.removeItem(self)
    def center(self):
        return self.pos() + self.rect().center()
