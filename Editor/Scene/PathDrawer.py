
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QBrush, QPainter, QPen, QPainterPath,QPolygonF
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
    QGraphicsPathItem,
    

    
)
import Styles
import math
from . import PointDisplay
def handlePoseComposer(pose : PointDisplay, handle):
    return lambda _ =  None: handle.centerPos() + pose.center()

class PathDrawer(QGraphicsPathItem):
    def __init__(self, path, *args, **kwargs):
        super(PathDrawer, self).__init__(*args, **kwargs)
        self.pathParent = path
        self.setPen(Styles.curveStyle.pen)
        self.curves = []
    def updatePath(self):
        self.curves = []
        data = self.pathParent.waypoints

        for i in data:
            i.poseDisplay.handle.hideHandles()
        
        for i in range(len(data)-1):
            pose1 = data[i].poseDisplay
            pose2 = data[i+1].poseDisplay

            pose1.handle.handle1.show()
            pose2.handle.handle2.show()

            self.curves.append((
                handlePoseComposer(pose1, pose1.handle.handle1),
                handlePoseComposer(pose2, pose2.handle.handle2), 
                pose2.center))
        #self.paint(QPainter(), 0)
        self.readyPaint()
        
        #if(self.parentItem() != None):
        #    print("helos")
        #    self
        #    self.scene().update()
        #    self.paint(QPainter(), 0)

    def _sourcePoint(self):
        return self.pathParent.waypoints[0].pos()

    def setDestination(self, point: QPointF):
        self._destinationPoint = point

    def bezierPath(self):
        path = QPainterPath()
        if(self._sourcePoint() == None): return path
        path.moveTo(self._sourcePoint())
        for curve in self.curves:
            path.cubicTo(curve[0](), curve[1](), curve[2]())
        return path
    
    @staticmethod
    def getLengthOfWaypoints(waypoints) -> QPainterPath:
        curves = []

        for i in waypoints:
            i.poseDisplay.handle.hideHandles()
        
        for i in range(len(waypoints)-1):
            pose1 = waypoints[i].poseDisplay
            pose2 = waypoints[i+1].poseDisplay

            pose1.handle.handle1.show()
            pose2.handle.handle2.show()

            curves.append((
                handlePoseComposer(pose1, pose1.handle.handle1),
                handlePoseComposer(pose2, pose2.handle.handle2), 
                pose2.center))
        path = QPainterPath()
        path.moveTo(waypoints[0].pos())
        for curve in curves:
            path.cubicTo(curve[0](), curve[1](), curve[2]())
        return path

    def readyPaint(self):
        path = self.bezierPath()
        self.setPath(path)

    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setPen(self.pen())
        painter.setBrush(Qt.BrushStyle.NoBrush)

        path = self.bezierPath()
        painter.drawPath(path)
        self.setPath(path)
    def delete(self):
        self.setParentItem(None)
        self.hide()

