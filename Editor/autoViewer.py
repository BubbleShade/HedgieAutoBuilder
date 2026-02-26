import sys

from PyQt6.QtCore import Qt, QPointF, QPoint, QRectF, QSize
from PyQt6.QtGui import QBrush, QPainter, QPen, QPixmap, QTransform, QShowEvent, QGuiApplication
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
    QFileDialog
)
import json, os, numpy, math
import Styles
from . import PointDisplay, SideBar, Action, Auto, Path, Waypoint, FieldMap, CommandGroup
from Tools import BezierCurve, clamp
import Tools
from Fields.Field2D_2026Rebuilt import RebuiltMap

class Camera(QGraphicsItem):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.zoomLevel = 1

    def setCenterPos(self, pos):
        #print(f"location: ${QPointF(self.scene().width(), self.scene().height())/2}")
        self.setPos(pos - QPointF(self.scene().width(), self.scene().height())/2)
    def paint(self, painter, option, widget = ...): pass
    def boundingRect(self):
        return QRectF(0,0,0,0)
    def reset(self, screen_rect):
        self.inflate = 0
        self.area = screen_rect.copy()
        return self.image.subsurface(self.area)

    def zoom(self, amount, eventPos : QPointF= None):
        #print(f"event: {eventPos}  + cam: {self.pos()}")
        startZoomLevel = self.zoomLevel
        mult = 1 + 0.02 * amount
        self.zoomLevel = clamp(self.zoomLevel * mult, 0.5, 2.0) 
        if(startZoomLevel == self.zoomLevel): return
        origin = eventPos  - self.pos()
        transform = QTransform()
        transform.translate(origin.x(), origin.y())
        transform.scale(self.zoomLevel, self.zoomLevel)
        transform.translate(-origin.x(), -origin.y())
        self.setTransform(transform)
    def setZoom(self, zoomLevel):
        #print(f"event: {eventPos}  + cam: {self.pos()}")
        startZoomLevel = self.zoomLevel
        self.zoomLevel = zoomLevel 
        transform = QTransform()
        transform.scale(self.zoomLevel, self.zoomLevel)
        self.setTransform(transform)
    def scenePosToCamera(self, pos):
        return (pos*self.scale()) - self.pos()
        
class AutoViewer(QGraphicsScene):
    def __init__(self, size : QRectF = QRectF(0,0,200,200), fieldMap : RebuiltMap = RebuiltMap()):
        super().__init__(size)
        self.camera = Camera()
        self.camera.setZoom(0.3)
        self.addItem(self.camera)
        self.addItem = self.addItemToCamera

        self.camera.setPos(-60,0)
        
        # Add the items to the scene. Items are stacked in the order they are added.
        self.auto : Auto = Auto(self)

        self.fieldMap = RebuiltMap()
        self.addItem(self.fieldMap)

        self.context_menu = QMenu()
    @staticmethod
    def fromJson(self, 
                 autoJson : dict,
                 size : QRectF = QRectF(0,0,200,200), 
                 fieldMap : RebuiltMap = RebuiltMap(),
                 ):
        viewer = AutoViewer(size, fieldMap)
        viewer.auto.delete()
        viewer.auto = Auto.fromJsonFile(viewer,autoJson, fieldMap)
        viewer.auto.addToStaticScene(viewer)
        return viewer


    def publish(self):
        Tools.networkTables.push_auto_to_network_tables(
            self.auto.getJsonFile(self.fieldMap)
            )

    def wheelEvent(self, event):
        super().wheelEvent(event)
        modifiers = QApplication.keyboardModifiers()
        if (modifiers & Qt.KeyboardModifier.ControlModifier):
            scrollAmount = math.sqrt(abs(event.delta())) * numpy.sign(event.delta())
            self.camera.zoom(scrollAmount, event.scenePos()) #+ QPointF(self.width(), self.height()))

    def addItemToCamera(self, item):
        item.setParentItem(self.camera)
        
    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        if(event.isAccepted()): return
        context_menu = QMenu()
        context_menu.setAutoFillBackground(True)
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        addWaypoint = context_menu.addAction("Add Waypoint")
        addPose = context_menu.addAction("Add Pose")
        addPath = context_menu.addAction("Add Path")

        addWaypoint.triggered.connect(lambda _:self.addPose(event.scenePos()))
        pos = AutoViewer.calculateContextPosition(event.scenePos(), event.screenPos(), context_menu.width(), self.sceneRect().width())
        context_menu.exec(pos)
        
    def calculateContextPosition(eventScenePos : QPointF, eventScreenPos : QPoint, menuWidth : float, contextWidth: float) -> QPoint:
        #print(f"scene pos: {eventScenePos}\n menu width: {menuWidth}\n context width: {contextWidth}")
        if(contextWidth + eventScenePos.x() > menuWidth):
            return (eventScreenPos- QPoint(menuWidth, 0))
        else: return eventScreenPos

    def addPose(self, position: QPointF):
        print(position, self.camera.scenePosToCamera(position))
        position = self.camera.scenePosToCamera(position)
        pose = Waypoint(self.auto.getClosestPath(position), position.x(),position.y())
        pose.addDisplay(self)
        self.auto.getClosestPath(position).addWaypoint(pose)
            
