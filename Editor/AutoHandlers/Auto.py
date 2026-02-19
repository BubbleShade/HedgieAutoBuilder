from .. import PointDisplay, SideBar, PathLabel, Action
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
class Auto():
    def __init__(self, scene, initialPose : InitialPose, execution : list = []):
        self.initialPose = initialPose
        self.execution = execution
        for i in execution:
            i.parentAuto = self
        self.scene = scene
        
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
        for i in self.execution:
            i.addToSideBar(sideBar)
    def paths(self) -> list[Path]:
        return list(filter(lambda a: type(a) == Path, self.execution))
    
    def delete(self):
        for i in self.execution:
            i.delete()
        
    def getClosestPath(self, position) -> Path:
        paths= self.paths()
        if(len(paths) == 0): return None
        return min(paths, key = lambda a: a.distFromPoint(position))
    
    def getJsonFile(self, fieldMap):
        data = {"execution":[]}

        for i in self.execution:
            i.addToJson(data, fieldMap)
        return data
    @staticmethod
    def fromJsonFile(scene, json : dict, fieldMap : FieldMap):
        execution = []
        for step in json["execution"]:
            if(step[0] == "Path"):
                path = Path.fromJsonFile(json[step[1]], fieldMap)

                execution.append(path)
                continue
                
        return Auto(scene, execution)