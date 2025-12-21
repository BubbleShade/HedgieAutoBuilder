
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
class Line(QGraphicsPathItem):
    def __init__(self, source, destination, *args, **kwargs):
        super(Line, self).__init__(*args, **kwargs)

        self._sourcePoint = source
        self._destinationPoint = destination
        
        pen = QPen(Qt.GlobalColor.green)
        pen.setWidth(3)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        self.setPen(pen)


    def setSource(self, point: QPointF):
        self._sourcePoint = point

    def setDestination(self, point: QPointF):
        self._destinationPoint = point

    def directPath(self):
        path = QPainterPath(self._sourcePoint())
        path.lineTo(self._destinationPoint())
        return path
    
    """def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.drawBezierCurve(qp)
        qp.end()"""


    def paint(self, painter: QPainter, option, widget=None) -> None:
        painter.setPen(self.pen())
        painter.setBrush(Qt.BrushStyle.NoBrush)

        path = self.directPath()
        painter.drawPath(path)
        self.setPath(path)

