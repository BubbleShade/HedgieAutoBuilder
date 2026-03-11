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
from . import PointDisplay, SideBar, Action, Auto, Path, Waypoint, InitialPose
from Tools import BezierCurve, clamp
import Tools
from Fields.Field2D_2026Rebuilt import RebuiltMap

class Camera(QGraphicsItem):
    def __init__(self, parent = None):
        super().__init__()
        self.zoomLevel = 1

    def setCenterPos(self, pos):
        self.setPos(pos - QPointF(self.scene().width(), self.scene().height())/2)
    def paint(self, painter, option, widget = ...): pass
    def boundingRect(self):
        return QRectF(0,0,0,0)
    def reset(self, screen_rect):
        self.inflate = 0
        self.area = screen_rect.copy()
        return self.image.subsurface(self.area)
    def setZoom(self, zoom):
        self.zoomLevel = zoom
        transform = QTransform()
        transform.scale(self.zoomLevel, self.zoomLevel)
        self.setTransform(transform)


    def zoom(self, amount, eventPos : QPointF= None):
        startZoomLevel = self.zoomLevel
        mult = 1 + 0.02 * amount
        self.zoomLevel = clamp(self.zoomLevel * mult, 0.5, 2.0) 
        if(startZoomLevel == self.zoomLevel): return
        if(eventPos == None):
            eventPos = QPointF(0,0)
        origin = eventPos  - self.pos()
        transform = QTransform()
        transform.translate(origin.x(), origin.y())
        transform.scale(self.zoomLevel, self.zoomLevel)
        transform.translate(-origin.x(), -origin.y())
        self.setTransform(transform)
    def scenePosToCamera(self, pos):
        return (pos*self.scale()) - self.pos()
        
class AutoBuilderScene(QGraphicsScene):
    def __init__(self, fieldMap = RebuiltMap(), sideBar : SideBar = None, size : QRectF = QRectF(0,0,200,200), isStatic = False):
        super().__init__(size)
        self.isStatic = isStatic

        self.sideBar = sideBar
        self.camera = Camera()
        self.addItem(self.camera)
        self.addItem = self.addItemToCamera

        self.isDragging = False
        self.dragStartPos = QPointF()
        self.dragScenePos = QPointF()
        #self.camera.setScale(1)
        
        # Add the items to the scene. Items are stacked in the order they are added.
        self.auto : Auto = None



        self.fieldMap = RebuiltMap()
        self.fieldMap.setParentItem(self.camera)

        self.context_menu = QMenu()
        self.current_file = ""
        self.defaultDirectory = ""
        
        if(self.isStatic):
            self.camera.setZoom(0.3)
            self.camera.setPos(-60,10)
        else:
            #self.auto.addToSideBar(self.sideBar)   
            self.camera.setZoom(1)
            self.camera.setPos(-240,-150)
  

    @staticmethod
    def fromJson(self, 
                    autoJson : dict,
                    size : QRectF = QRectF(0,0,200,200)
                    ):
        viewer = AutoBuilderScene(RebuiltMap(), None, size, True)
        viewer.auto = Auto.fromJsonFile(viewer,autoJson, viewer.fieldMap)
        viewer.auto.addToStaticScene(viewer)

        return viewer   

    def reset_camera(self):
        self.camera.setZoom(1)
        self.camera.setPos(-240,-150)
        

    def save_as(self):
        if(self.defaultDirectory != ""): folderDialog = QFileDialog(directory=self.defaultDirectory)
        else: folderDialog = QFileDialog()
        fileName = folderDialog.getSaveFileName(caption="Save As",filter="*.json")
        if(fileName[0] == ""): return
        with open(fileName[0], "w") as f:
            json.dump(self.auto.getJsonFile(self.fieldMap), f, indent=4)
        self.current_file = fileName[0]
    def save(self):
        if(self.current_file == ""): self.save_as(); return
        with open(self.current_file, "w") as f:
            json.dump(self.auto.getJsonFile(self.fieldMap), f, indent=4)
    def changeAutoTo(self, auto : Auto):
        if(self.auto != None): 
            self.auto.delete()
        self.auto = auto
        self.auto.addToScene(self)
        self.auto.addToSideBar(self.sideBar)
        self.update()

    def setDefaultDirectory(self,directory =""):
        self.defaultDirectory = directory
    def setCurrentFile(self, file = ""):
        self.current_file = file
    def changeAutoFromFile(self, fileName : str):
        with open(fileName, "r") as f:
            auto = Auto.fromJsonFile(self, json.load(f),self.fieldMap)
            self.changeAutoTo(auto)        
        self.current_file = fileName
    def open(self):
        if(self.defaultDirectory != ""): folderDialog = QFileDialog(directory=self.defaultDirectory)
        else: folderDialog = QFileDialog()
        fileName = folderDialog.getOpenFileName(caption="Open File",filter="*.json")
        if(fileName[0] == ""): return
        self.changeAutoFromFile(fileName[0])

    def publish(self):
        Tools.networkTables.push_auto_to_network_tables(
            self.parent(),
            self.auto.getJsonFile(self.fieldMap)
            )

    def keyPressEvent(self, event):
        if(self.isStatic): return
        modifiers = QApplication.queryKeyboardModifiers()
        if event.key() == Qt.Key.Key_Z and  modifiers & Qt.KeyboardModifier.ControlModifier:
            if(modifiers & Qt.KeyboardModifier.ShiftModifier):
                Action.redo()
            else:
                Action.undo()
        if event.key() == Qt.Key.Key_S and modifiers & Qt.KeyboardModifier.ControlModifier:
            if(modifiers & Qt.KeyboardModifier.ShiftModifier):
                self.save_as()
            else:
                self.save()
        if event.key() == Qt.Key.Key_P and modifiers & Qt.KeyboardModifier.ControlModifier:
            self.publish()
  
    def mousePressEvent(self, event):
        if(self.isStatic): return
        super().mousePressEvent(event)
        if(not event.isAccepted()):
            self.isDragging = True
            self.dragScenePos = event.scenePos()
            self.dragStartPos = self.camera.pos()

    def mouseReleaseEvent(self, event):
        if(self.isStatic): return
        super().mouseReleaseEvent(event)
        self.isDragging = False

    def mouseMoveEvent(self, event):
        if(self.isStatic): return
        super().mouseMoveEvent(event)
        if(self.isDragging):
            self.camera.setPos(self.dragStartPos + (event.scenePos() - self.dragScenePos))

    def wheelEvent(self, event):
        if(self.isStatic): return
        super().wheelEvent(event)
        modifiers = QApplication.keyboardModifiers()
        if (modifiers & Qt.KeyboardModifier.ControlModifier):
            scrollAmount = math.sqrt(abs(event.delta())) * numpy.sign(event.delta())
            self.camera.zoom(scrollAmount, event.scenePos()) #+ QPointF(self.width(), self.height()))

    def addItemToCamera(self, item):
        item.setParentItem(self.camera)
        
    def contextMenuEvent(self, event):
        if(self.isStatic): return
        super().contextMenuEvent(event)
        if(event.isAccepted()): return
        context_menu = QMenu()
        context_menu.setAutoFillBackground(True)
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        addWaypoint = context_menu.addAction("Add Waypoint")
        addPose = context_menu.addAction("Add Pose")
        addPath = context_menu.addAction("Add Path")

        addWaypoint.triggered.connect(lambda _:self.addPose(event.scenePos()))
        pos = AutoBuilderScene.calculateContextPosition(event.scenePos(), event.screenPos(), context_menu.width(), self.sceneRect().width())
        context_menu.exec(pos)
        
    def calculateContextPosition(eventScenePos : QPointF, eventScreenPos : QPoint, menuWidth : float, contextWidth: float) -> QPoint:
        if(contextWidth + eventScenePos.x() > menuWidth):
            return (eventScreenPos- QPoint(menuWidth, 0))
        else: return eventScreenPos

    def addPose(self, position: QPointF):
        position = self.camera.scenePosToCamera(position)
        pose = Waypoint(self.auto.getClosestPath(position), position.x(),position.y())
        pose.addDisplay(self)
        self.auto.getClosestPath(position).addWaypoint(pose)
            
