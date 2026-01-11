from . import PoseDisplay, SideBar, PathLabel, WaypointDisplay
import Styles
from Tools import BezierCurve
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QBrush, QPainter, QPen, QContextMenuEvent, QDrag, QPixmap
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
    QLabel,
    QMenu,
    
)
def handlePoseComposer(pose : PoseDisplay, handle):
    return lambda _ =  None: handle.centerPos() + pose.center()

class Pose():
    def __init__(self, parentPath = None, x = 0, y = 0):
        self.x = x
        self.y = y
        self.parentPath = parentPath
        self.poseDisplay = None
    def setParent(self, parentPath):
        self.parentPath = parentPath

    def addPoseDisplay(self, scene):
        self.poseDisplay = PoseDisplay(scene, self)
        self.poseDisplay.setPos(self.x, self.y)
    
    def delete(self, isRecursive = False):
        if(self.poseDisplay != None):
            self.poseDisplay.delete()

class Waypoint():
    def __init__(self, parentPath = None, x = 0, y = 0):
        self.x = x
        self.y = y
        self.parentPath = parentPath
        self.poseDisplay = None
    def setParent(self, parentPath):
        self.parentPath = parentPath

    def addDispalay(self, scene):
        self.poseDisplay = WaypointDisplay(scene, self)
        self.poseDisplay.setPos(self.x, self.y)
    
    def delete(self, isRecursive = False):
        if(self.poseDisplay != None):
            self.poseDisplay.delete()

class Path():
    def __init__(self, initialPose : Pose = None, endPose : Pose = None, waypoints : list[Waypoint] = []):
        if(initialPose != None): 
            initialPose.setParent(self)
            self.initialPose = initialPose
        else: self.initialPose = Pose(self)

        if(endPose != None): 
            self.endPose = endPose
            initialPose.setParent(self)

        else: self.endPose = Pose(self)

        self.waypoints = waypoints
        self.sideBarItem = None
        self.curves = []

    def updateScene(self,scene):
        self.reBezier(scene)
        pass
    def reBezier(self,scene):
        for i in self.curves:
            scene.removeItem(i)
        self.curves = []
        data = [self.initialPose, *self.waypoints, self.endPose]

        pen = QPen(Styles.toothPasteGray)
        pen.setWidth(2)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)

        for i in data:
            i.poseDisplay.handle.hideHandles()
        
        for i in range(len(data)-1):
            pose1 = data[i].poseDisplay
            pose2 = data[i+1].poseDisplay

            pose1.handle.handle1.show()
            pose2.handle.handle2.show()

            curve = BezierCurve(pose1.center, pose2.center, 
                                handlePoseComposer(pose1, pose1.handle.handle1),
                                handlePoseComposer(pose2, pose2.handle.handle2))
                                #lambda _ =  None: pose1.handle.handle1.centerPos() + pose1.center(), 
                                #lambda _ = None: pose2.handle.handle2.centerPos() + pose2.center())

            curve.setPen(pen)
            scene.addItem(curve)
            self.curves.append(curve)

    def addToScene(self, scene):
        self.initialPose.addPoseDisplay(scene)
        self.endPose.addPoseDisplay(scene)
        for i in self.waypoints:
            i.addDispalay(scene)
        self.reBezier(scene)

    def addToSideBar(self, sideBar : SideBar):
        self.sideBarItem = PathLabel()
        sideBar.addPathLabel(self.sideBarItem)
        self.sideBarItem.addPoseLabel(sideBar.CreatePoseLabel(self.initialPose))
        self.sideBarItem.addPoseLabel(sideBar.CreatePoseLabel(self.endPose))



class Auto():
    def __init__(self, execution = []):
        self.execution = execution
    def addToScene(self, scene):
        for i in self.execution:
            if(i.addToScene !=  None):
                i.addToScene(scene)
    def addToSideBar(self, sideBar):
        for i in self.execution:
            i.addToSideBar(sideBar)




