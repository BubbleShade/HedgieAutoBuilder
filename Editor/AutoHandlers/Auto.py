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

class Auto():
    def __init__(self, scene, execution = []):
        self.execution = execution
        for i in execution:
            i.parentAuto = self
        self.scene = scene
    def addToScene(self, scene):
        for i in self.execution:
            if(i.addToScene !=  None):
                i.addToScene(scene)
    def addToSideBar(self, sideBar):
        for i in self.execution:
            i.addToSideBar(sideBar)
    def paths(self) -> list[Path]:
        return list(filter(lambda a: type(a) == Path, self.execution))
        
    def getClosestPath(self, position) -> Path:
        paths= self.paths()
        if(len(paths) == 0): return None
        return min(paths, key = lambda a: a.distFromPoint(position))
        






