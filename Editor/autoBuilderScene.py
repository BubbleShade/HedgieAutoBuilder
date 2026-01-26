import sys

from PyQt6.QtCore import Qt, QPointF, QPoint, QRectF
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
)
from . import PointDisplay, SideBar, Action
import Styles
import numpy, math
from Tools import BezierCurve, clamp
from . import Auto, Path, Waypoint
from . import FieldMap, FieldImage

class Camera(QGraphicsItem):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.zoomLevel = 1

    def setCenterPos(self, pos):
        print(self.scene().sceneRect().width())
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
    def scenePosToCamera(self, pos):
        return (pos*self.scale()) - self.pos()


        #self.setTransformOriginPoint(origin)

        #self.setScale(1/self.zoomLevel)

        
class AutoBuilderScene(QGraphicsScene):
    def __init__(self, sideBar : SideBar):
        super().__init__(0,0,200,200)
        self.sideBar = sideBar
        self.camera = Camera()
        self.addItem(self.camera)
        self.addItem = self.addItemToCamera

        self.isDragging = False
        self.dragStartPos = QPointF()
        self.dragScenePos = QPointF()
        #self.camera.setScale(1)
        self.camera.setPos(-240,-150)
        
        # Add the items to the scene. Items are stacked in the order they are added.
        self.auto = Auto(self,[Path([Waypoint(x=504,y=504), Waypoint(x=125,y=100),Waypoint(x=200,y=200)])])

        self.auto.addToScene(self)
        self.fieldMap = FieldMap("Fields/Field2d_2025Bunnybots/")
        self.fieldImage = FieldImage(self.fieldMap)
        self.addItem(self.fieldImage)

        self.auto.addToSideBar(self.sideBar)

        #pose1 = PoseDisplay(self)
        #pose1.setPos(50, 20)
        
        #pose2 = PoseDisplay(self)
        #pose2.setPos(125, 100)
        self.i = 3
        self.curves : list[BezierCurve] = []

        self.context_menu = QMenu()

    def keyPressEvent(self, event):
        modifiers = QApplication.queryKeyboardModifiers()
        if event.key() == Qt.Key.Key_Z and  modifiers & Qt.KeyboardModifier.ControlModifier:
            if(modifiers & Qt.KeyboardModifier.ShiftModifier):
                Action.redo()
            else:
                Action.undo()


        
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if(not event.isAccepted()):
            #self.camera.setPos(self.camera.pos() + QPointF(10,0))
            #self.camera.setScale(self.camera.scale())
            self.isDragging = True
            self.dragScenePos = event.scenePos()
            self.dragStartPos = self.camera.pos()

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        self.isDragging = False

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        if(self.isDragging):
            self.camera.setPos(self.dragStartPos + (event.scenePos() - self.dragScenePos))

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
        context_menu.addSection("test")
        addPath = context_menu.addAction("Add Path")
        addPath = context_menu.addAction("Add Path")


        addWaypoint.triggered.connect(lambda _:self.addPose(event.scenePos()))
        pos = AutoBuilderScene.calculateContextPosition(event.scenePos(), event.screenPos(), context_menu.width(), self.sceneRect().width())
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
            
