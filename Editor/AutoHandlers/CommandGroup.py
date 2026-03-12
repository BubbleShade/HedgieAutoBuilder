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
from . import Path, Waypoint, NamedCommand
from .. import FieldMap, PathDrawer
from ..SideBar import CommandGroupSideBarItem
from enum import Enum

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
    def __init__(self, type : CommandGroupType, parentAuto, *execution):
        self.execution = list(execution)
        self.type = type
        self.scene = None
        self.parentAuto = None
        for i in execution:
             i.parentAuto = self

    def addPathBelow(self, item):
        print("ADD PATH BELWOS")
        index = self.execution.index(item) + 1
        paths = self.paths()
        if(len(self.paths()) > 0):
            lastWaypoint = paths[-1].waypoints[-1]
            newPath = Path(Waypoint(x=lastWaypoint.x() + 100, y=lastWaypoint.y(), heading=0))
        else:
            newPath = Path(Waypoint(x=100, y=250, heading=0))
        self.execution.insert(index, newPath)
        print(self.execution)
        newPath.parentAuto = self
        if(self.scene != None):
            newPath.addToScene(self.scene)
            self.addSideBarWidget(newPath.sideBarItem, index)
            self.updateScene()
    def addNamedCommandBelow(self, item):
        index = self.execution.index(item) + 1
        newNamedCommand = NamedCommand("Do Nothing")
        self.execution.insert(index, newNamedCommand)
        print(self.execution)
        newNamedCommand.parentAuto = self
        if(self.scene != None):
            newNamedCommand.addToScene(self.scene)
            self.addSideBarWidget(newNamedCommand.sideBarItem, index)
            self.updateScene()
    def updateScene(self,scene : QGraphicsScene = None):
        if(self.parentAuto != None):
            self.parentAuto.updateScene(scene)
        if(scene == None): return
        
    def addToScene(self, scene):
        self.scene = scene
        for i in self.execution:
            if(i.addToScene !=  None):
                i.addToScene(scene)
    def addToStaticScene(self, scene):
        self.scene = scene
        for i in self.execution:
            if(i.addToStaticScene !=  None):
                i.addToStaticScene(scene)

    def addToSideBar(self, sideBar):
        self.sideBarItem = CommandGroupSideBarItem("WHAR", self)
        sideBar.addSideBarWidget(self.sideBarItem)
        for i in self.execution:
            self.addSideBarWidget(i.sideBarItem)

    def addSideBarWidget(self, widget, index = -1):
        if(index >= 0):
            index += 1
        self.sideBarItem.lay.insertWidget(index, widget)
    def addSideBarLayout(self, layout):
        self.sideBarItem.lay.addLayout(layout)
    
    
    def paths(self) -> list[Path]:
        return list(filter(lambda a: type(a) == Path, self.execution))
    
    def delete(self):

        for i in range(len(self.execution)):
            self.execution[0].delete()