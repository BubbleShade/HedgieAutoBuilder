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
from . import DraggableGraphicsItem, BezierHandle
class PointDisplay(DraggableGraphicsItem):
    def poseRect(self): return QRectF(-15,-15,30,30)
    def waypointRect(self): return QRectF(-10,-10,20,20)
    def __init__(self, scene : QGraphicsScene, waypointHandler, has_rotation :bool = False):
        super(PointDisplay, self).__init__(scene)
        self.handle = BezierHandle(self)
        self.setHasRotation(has_rotation)
        self.arrow = ArrowDrawer(QPointF(0, -11), QPointF(0, 11))
        self.waypointHandler = waypointHandler
        
        self.setParentItem(scene.camera)
        self.pen = QPen(Styles.toothPasteGray)
        self.pen.setWidth(3)

        self.canRotate = has_rotation

        self.handle.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True)
        
    def drawPose(self, painter : QPainter, option, widget = ...):
        if(not self.isVisible()): return
        Styles.poseStyle.set_painter(painter)
        painter.drawRect(self.boundingRect())
        self.arrow.paint(painter ,option)
        
    def drawWapoint(self, painter : QPainter, option, widget = ...):
        if(not self.isVisible()): return
        Styles.waypointStyle.set_painter(painter)
        painter.drawEllipse(self.boundingRect())

    def paint(self, painter, option, widget = ...): pass
    def boundingRect(self): return QRectF(0,0,0,0)

    def delete(self):
        self.scene.removeItem(self)

    def undoDelete(self):
        self.scene.addItem(self)

    def setHasRotation(self, has_rotation):
        self.canRotate = has_rotation
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
        deleteButton.triggered.connect(self.waypointHandler.delete)
        
        context_menu.exec(event.screenPos())

    
