
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
import math
class BezierCurve(QGraphicsPathItem):
    def __init__(self, source: QPointF = None, destination: QPointF = None, *args, **kwargs):
        super(BezierCurve, self).__init__(*args, **kwargs)

        self._sourcePoint = source
        self._destinationPoint = destination


    def setSource(self, point: QPointF):
        self._sourcePoint = point

    def setDestination(self, point: QPointF):
        self._destinationPoint = point

    def directPath(self):
        path = QPainterPath(self._sourcePoint)
        path.lineTo(self._destinationPoint)
        return path


    def paint(self, painter: QPainter, option, widget=None) -> None:

        #painter.setRenderHint(Qt.)

        #painter.pen().setWidth(2)
        #painter.pen().setColor(Qt.GlobalColor.green)
        painter.setPen(self.pen())
        painter.setBrush(Qt.BrushStyle.NoBrush)

        path = self.directPath()
        painter.drawPath(path)
        self.setPath(path)