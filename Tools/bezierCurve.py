
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
    QGraphicsPathItem
    
)
import Styles
import math
class BezierCurve(QGraphicsPathItem):
    def __init__(self, source, destination, ctrlPoint1, ctrlPoint2, *args, **kwargs):
        super(BezierCurve, self).__init__(*args, **kwargs)

        self._sourcePoint = source
        self._destinationPoint = destination
        self.ctrlPoint1 = ctrlPoint1
        self.ctrlPoint2 = ctrlPoint2


    def setSource(self, point: QPointF):
        self._sourcePoint = point

    def setDestination(self, point: QPointF):
        self._destinationPoint = point

    def bezierPath(self):
    
        path = QPainterPath()
        path.moveTo(self._sourcePoint())
        #print(f"CtrlPoint1: {self.ctrlPoint1()}, CtrlPoint2: {self.ctrlPoint2()}")
        path.cubicTo(self.ctrlPoint1(), self.ctrlPoint2(), self._destinationPoint())
        return path


    def paint(self, painter: QPainter, option, widget=None) -> None:

        painter.setPen(self.pen())
        painter.setBrush(Qt.BrushStyle.NoBrush)

        path = self.bezierPath()
        painter.drawPath(path)
        self.setPath(path)

