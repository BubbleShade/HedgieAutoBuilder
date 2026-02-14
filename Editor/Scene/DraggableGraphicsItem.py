import sys
from .. import Action
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

class DraggableGraphicsItem(QGraphicsItem):
    def __init__(self, scene : QGraphicsScene, canRotate = True, canMove = True):
        super(DraggableGraphicsItem, self).__init__()
        self.canRotate = canRotate

        if(canMove):
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        else:
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)

        self.scene : QGraphicsScene = scene
        self.startPosition = self.pos()
    
    def createUndoMoveAction(this, startPos, endPos):
        return Action.Action(lambda : this.setPos(startPos), lambda : this.setPos(endPos))    
    def wheelEvent(self, QWheelEvent):
        if(not self.isSelected()): return
        if(not self.canRotate): return
        newRotation = self.rotation() + ((1/8)*QWheelEvent.delta())
        if(Action.lastAction() != None and Action.lastAction().key[0] == "R"):
            print(newRotation)
            Action.undoList[-1].redo = lambda: self.setRotation(newRotation)
        else:
            currentRotation = self.rotation()
            Action.addAction(Action.Action(lambda:self.setRotation(currentRotation), lambda:self.setRotation(newRotation), ["R"]))
        self.setRotation(self.rotation() + ((1/8)*QWheelEvent.delta()))
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.startPosition = self.pos()
        self.scene.clearSelection()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        Action.addAction(self.createUndoMoveAction(self.startPosition, self.pos()))
            
    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if(not self.isSelected()): return

    def center(self):
        return self.pos() 
