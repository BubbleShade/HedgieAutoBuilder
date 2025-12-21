
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
class Arrow(QGraphicsPathItem):
    def __init__(self, source: QPointF = None, destination: QPointF = None,  *args, **kwargs):
        super(Arrow, self).__init__(*args, **kwargs)

        self._sourcePoint = source
        self._destinationPoint = destination

        self._arrow_height = 5
        self._arrow_width = 4

    def setSource(self, point: QPointF):
        self._sourcePoint = point

    def setDestination(self, point: QPointF):
        self._destinationPoint = point

    def directPath(self):
        path = QPainterPath(self._sourcePoint)
        path.lineTo(self._destinationPoint)
        return path

    def arrowCalc(self, start_point=None, end_point=None):  # calculates the point where the arrow should be drawn

        try:
            startPoint, endPoint = start_point, end_point

            if start_point is None:
                startPoint = self._sourcePoint

            if endPoint is None:
                endPoint = self._destinationPoint

            dx, dy = startPoint.x() - endPoint.x(), startPoint.y() - endPoint.y()

            leng = math.sqrt(dx ** 2 + dy ** 2)
            normX, normY = dx / leng, dy / leng  # normalize

            # perpendicular vector
            perpX = -normY
            perpY = normX

            leftX = endPoint.x() + self._arrow_height * normX + self._arrow_width * perpX
            leftY = endPoint.y() + self._arrow_height * normY + self._arrow_width * perpY

            rightX = endPoint.x() + self._arrow_height * normX - self._arrow_width * perpX
            rightY = endPoint.y() + self._arrow_height * normY - self._arrow_width * perpY

            point2 = QPointF(leftX, leftY)
            point3 = QPointF(rightX, rightY)

            return QPolygonF([point2, endPoint, point3])

        except (ZeroDivisionError, Exception):
            return None

    def paint(self, painter: QPainter, option, widget=None) -> None:

        #painter.setRenderHint(Qt.)

        #painter.pen().setWidth(2)
        #painter.pen().setColor(Qt.GlobalColor.green)
        painter.setPen(self.pen())
        painter.setBrush(Qt.BrushStyle.NoBrush)

        path = self.directPath()
        painter.drawPath(path)
        self.setPath(path)

        triangle_source = self.arrowCalc(path.pointAtPercent(0.1), self._sourcePoint)  # change path.PointAtPercent() value to move arrow on the line

        if triangle_source is not None:
            painter.drawPolyline(triangle_source)