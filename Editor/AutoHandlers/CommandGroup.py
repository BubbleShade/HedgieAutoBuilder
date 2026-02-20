from .. import PointDisplay, SideBar, PathSidebarItem, Action
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
from . import Path
from . import InitialPose
from .. import FieldMap
from .. import PathDrawer
from ..SideBar import CommandGroupSideBarItem
from enum import Enum
@enumerate
class CommandGroupType(Enum):
    Sequential = ("S","Sequential")
    Parallel = ("P","Parallel")
    ParallelRace = ("R","Parallel Race")
    ParallelDeadline = ("D","Parallel Deadline")
    @staticmethod
    def getFromLetter(letter):
        if(letter == "P"): return CommandGroupType.Parallel
        if(letter == "R"): return CommandGroupType.ParallelRace
        if(letter == "D"): return CommandGroupType.ParallelDeadline
        return CommandGroupType.Sequential

class CommandGroup():
    def __init__(self, type : CommandGroupType, *execution):
        self.execution = list(execution)
        self.type = type
        for i in execution:
            i.parentAuto = self
        self.pathDrawer = PathDrawer(self)

    def updateScene(self,scene : QGraphicsScene = None):
        self.pathDrawer.updatePath(self.pathDrawerWaypoints())
        if(scene == None): return

    def pathDrawerWaypoints(self):
        waypoints = [self.initialPose]
        for i in self.execution:
            if(type(i) == Path):
                for waypoint in i.waypoints:
                    waypoints.append(waypoint)
        return waypoints

        
    def getLastPose(self, path : Path):
        index = self.execution.index(path)
        for i in range(index + 1):
            if(index - i - 1 < 0):
                return self.initialPose
            if(type(self.execution[index - i - 1] == Path)):
                return self.execution[index - i - 1].waypoints[-1]

    def addToScene(self, scene):
        for i in self.execution:
            if(i.addToScene !=  None):
                i.addToScene(scene)
    def addToStaticScene(self, scene):
        for i in self.execution:
            if(i.addToStaticScene !=  None):
                i.addToStaticScene(scene)

    def addToSideBar(self, sideBar):
        self.sideBarItem = CommandGroupSideBarItem("WHAR", self)
        sideBar.addSideBarItem(self.sideBarItem)
        for i in self.execution:
            i.addToSideBar(self)
    def addSideBarItem(self, widget):
        self.sideBarItem.lay.addWidget(widget)
    
    def paths(self) -> list[Path]:
        return list(filter(lambda a: type(a) == Path, self.execution))
    
    def delete(self):
        self.initialPose.delete()
        for i in self.execution:
            i.delete()
        self.pathDrawer.delete()