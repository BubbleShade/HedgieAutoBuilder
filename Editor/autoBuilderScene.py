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
from . import PointDisplay, SideBar, PoseLabel
import Styles
from Tools import BezierCurve, clamp
from .stuff import Auto, Path, Waypoint
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
    def drift(self, screen_rect, mpos, inward):
        if inward:
            d = (pygame.Vector2(mpos) - screen_rect.center).normalize()
        else:
            d = (pygame.Vector2(screen_rect.center) - mpos).normalize()
 
        d *= self.speed
        self.area.move_ip(int(d.x), int(d.y))
 
    def reset(self, screen_rect):
        self.inflate = 0
        self.area = screen_rect.copy()
        return self.image.subsurface(self.area)
 
    def zoom_in(self, screen_rect, event):
        self.drift(screen_rect, event.pos, True)
        self.inflate -= self.speed
        rect = self.area.inflate(self.inflate, self.inflate)
        rect.clamp_ip(self.image.get_rect())
 
        return pygame.transform.scale(self.image.subsurface(rect), screen_rect.size)

    def zoom(self, amount, eventPos : QPointF= None):
        startZoomLevel = self.zoomLevel
        self.zoomLevel = clamp(self.zoomLevel + amount * 0.01, 0.5, 2.0) 
        if(startZoomLevel == self.zoomLevel): return

        self.setScale(1/self.zoomLevel)
        if(eventPos == None): return
        print(eventPos + self.scene().sceneRect().bottomRight()/2)
        eventPos *= startZoomLevel

        moveby = (eventPos + self.scene().sceneRect().center()/2) * amount * 0.01

        moveby *= self.zoomLevel
        #print(moveby)

        self.moveBy(moveby.x(), moveby.y())
        

        
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
        self.auto = Auto([Path([Waypoint(x=504,y=504), Waypoint(x=125,y=100),Waypoint(x=200,y=200)])])

        self.auto.addToScene(self)
        self.fieldMap = FieldMap("Fields/Field2d_2025Bunnybots/")
        self.fieldImage = FieldImage(self.fieldMap)
        self.addItem(self.fieldImage)

        self.auto.addToSideBar(self.sideBar)
        self.i = 3
        self.curves : list[BezierCurve] = []

        self.context_menu = QMenu()
        
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
            self.camera.zoom(event.delta(), event.scenePos()) #+ QPointF(self.width(), self.height()))

    def addItemToCamera(self, item):
        item.setParentItem(self.camera)
        
    def contextMenuEvent(self, event):
        super().contextMenuEvent(event)
        if(event.isAccepted()): return
        context_menu = QMenu()
        context_menu.setAutoFillBackground(True)
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        addButton = context_menu.addAction("Add Pose")
        addWaypoint = context_menu.addAction("Add Waypoint")

        addButton.triggered.connect(lambda _:self.addPose(event.scenePos()))
        pos = AutoBuilderScene.calculateContextPosition(event.scenePos(), event.screenPos(), context_menu.width(), self.sceneRect().width())
        context_menu.exec(pos)
        
    def calculateContextPosition(eventScenePos : QPointF, eventScreenPos : QPoint, menuWidth : float, contextWidth: float) -> QPoint:
        #print(f"scene pos: {eventScenePos}\n menu width: {menuWidth}\n context width: {contextWidth}")
        if(contextWidth + eventScenePos.x() > menuWidth):
            return (eventScreenPos- QPoint(menuWidth, 0))
        else: return eventScreenPos

    def addPose(self, position: QPointF):
        pose = PointDisplay(self)
        pose.setPos(position)
        self.sideBar.PathLabel1.addPose(f"Pose {self.i}", pose=pose)
        self.i += 1
        
    
        # Set all items as moveable and selectable.
        #for item in self.items():
            
