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
from . import Path, NamedCommand, CommandGroup, CommandGroupType
from . import InitialPose
from .. import FieldMap
from .. import PathDrawer
import Tools
class Auto():
    def __init__(self, scene, initialPose : InitialPose = InitialPose(0,0), commandGroup : CommandGroup = CommandGroup(CommandGroupType.Sequential, None)):
        self.initialPose = initialPose
        self.commandGroup = commandGroup
        self.scene = scene
        self.pathDrawer = PathDrawer(self)

    def updateScene(self,scene : QGraphicsScene = None):
        self.pathDrawer.updatePath(self.pathDrawerWaypoints())
        if(scene == None): return

    def pathDrawerWaypoints(self):
        waypoints = [self.initialPose]
        for i in self.commandGroup.execution:
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
        
        self.initialPose.addDisplay(scene)
        self.commandGroup.addToScene(scene)
        
        self.pathDrawer.setParentItem(scene.camera)
        self.updateScene(scene)

    def addToStaticScene(self, scene):
        self.initialPose.addDisplay(scene, True)
        self.commandGroup.addToStaticScene(scene)
        self.pathDrawer.setParentItem(scene.camera)
        self.updateScene(scene)

    def addToSideBar(self, sideBar):
        Tools.clear_layout(sideBar.lay)
        sideBar.addSideBarWidget(self.initialPose.sideBarItem)
        self.commandGroup.addToSideBar(sideBar)

    def paths(self) -> list[Path]:
        return list(filter(lambda a: type(a) == Path, self.commandGroup.execution))
    
    def delete(self):
        if(type(self.initialPose) == InitialPose): self.initialPose.delete()
        self.commandGroup.delete()
        self.pathDrawer.delete()

        
    def getClosestPath(self, position) -> Path:
        paths= self.paths()
        if(len(paths) == 0): return None
        return min(paths, key = lambda a: a.distFromPoint(position))
    @staticmethod
    def iterateThroughExecution(commandGroup : CommandGroup, json, pathCount, fieldMap):
        string = commandGroup.type.value[0] + "("
        for i in commandGroup.execution:
            if(string != ""): string += ","
            if(type(i) == Path):
                string += "p" + str(pathCount)
                json["p" + str(pathCount)] = i.getJson(fieldMap)
                pathCount += 1
            if(type(i) == NamedCommand):
                string += "n(" + i.name + ")"
            if(type(i) == CommandGroup):
                pathCount, guy = Auto.iterateThroughExecution(json, pathCount, fieldMap)
                string += guy
        return pathCount, string + ")"
    
    def getJsonFile(self, fieldMap):
        data = {"initialPose": self.initialPose.getJson(fieldMap)}
        pathCount, execution = Auto.iterateThroughExecution(self.commandGroup, data, 0, fieldMap)
        data["execution"] = execution
        print(data)
        return data
    @staticmethod
    def iterateThroughExecutionJson(i, executionString : str, json, fieldMap):
        execution = []
        stringLength = len(executionString)
        while(i < stringLength):
            if(executionString[i] == ","):
                i += 1
                continue
            if(executionString[i] == ")"):
                i += 1
                break
            if(json["execution"][i] == "p"):
                num = ""
                i += 1
                while(i < stringLength and executionString[i].isnumeric()):
                    num += executionString[i]
                    i += 1
                execution.append(Path.fromJsonFile(json["p" + num], fieldMap))
                print("exec", execution)
                continue
            if(json["execution"][i] == "n"):
                autoName = ""
                i += 2
                while(executionString[i] != "]" and i < stringLength):
                    autoName += executionString[i]
                    i += 1
                execution.append(NamedCommand(autoName))
                continue
            if(json["execution"][i] in ("S", "P", "R", "D")):
                commandType = CommandGroupType.getFromLetter(json["execution"][i])
                i, newCommandGroupExecution = Auto.iterateThroughExecutionJson(i+2, executionString, json, fieldMap)
                print(newCommandGroupExecution)

                execution.append(CommandGroup(commandType, None, *newCommandGroupExecution))
                continue
            i += 1
        return i, execution


    @staticmethod
    def fromJsonFile(scene, json : dict, fieldMap : FieldMap):
        i, execution = Auto.iterateThroughExecutionJson(0, json["execution"], json, fieldMap)
        initialPose = InitialPose.fromJsonFile(json["initialPose"], fieldMap)
        print("finalExec", execution[0].execution)
        print("FromJsonFile")
        return Auto(scene, initialPose, execution[0])
