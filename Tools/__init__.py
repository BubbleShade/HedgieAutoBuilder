__all__ = ["Arrow", "Line", "BezierCurve","clamp","magnitude","vectorAngle","angleBetween","rotateVectorByAngle"]
__name__ = "Tools"

from PyQt6.QtCore import QPointF
import math
from Tools.arrow import Arrow, ArrowDrawer
from Tools.line import Line
from Tools.bezierCurve import BezierCurve

def clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)
def magnitude(pos : QPointF): return math.sqrt(pow(pos.x(),2) + pow(pos.y(),2))
def unit(pos : QPointF) -> QPointF: return pos / magnitude(pos)
"""Returns the Arctan2 of x and y"""
def vectorAngle(pos : QPointF): return math.atan2(pos.x(), pos.y())
def angleBetween(pos1 : QPointF, pos2 : QPointF): 
    return math.acos(
        QPointF.dotProduct(pos1, pos2) / (magnitude(pos1)*magnitude(pos2)))
def rotateVectorByAngle(pos : QPointF, theta):
    return QPointF(pos.x() * math.cos(theta) - pos.y() * math.sin(theta),
                   pos.x() * math.sin(theta) + pos.y() * math.cos(theta))


def getHandlePos(point : QPointF, pointA : QPointF, pointB : QPointF) -> tuple[QPointF,QPointF]:
    point1 = pointA - point
    point2 = pointB - point
    A = unit(point1- point2)
    return A, -A
def pointFromJson(json : dict) -> QPointF:
    return QPointF(json["x"], json["y"])

def clear_layout(layout):
    """
    Recursively removes all items (widgets, sub-layouts, and spacers) from a layout.
    """
    if layout is not None:
        # Loop in reverse order to safely remove items
        for i in reversed(range(layout.count())):
            item = layout.takeAt(i)
            widget = item.widget()
            if widget is not None:
                # Remove and delete the widget
                widget.setParent(None)
                widget.deleteLater()
            elif item.layout() is not None:
                # Recurse into sub-layouts
                clear_layout(item.layout())
            
            # It is the caller's responsibility to delete the item
            del item

    """handle1 = pointA - point
    handle2 = pointB - point
        
    angleBetweenHandles =  angleBetween(handle1, handle2)
    if(abs(vectorAngle(pointA) - vectorAngle(pointB)) <= math.pi/2):
        angleBetweenHandles *= -1


    handle1 = rotateVectorByAngle(handle1, -angleBetweenHandles/2)
    handle2 = rotateVectorByAngle(handle2, angleBetweenHandles/2)

    midpoint = (handle1+handle2)/2

    return unit(handle1 - midpoint), unit(handle2 - midpoint)"""

    """
    angleBetweenHandles =  angleBetween(handle1, handle2)
    if((handle1 + handle2).y() > 0):
        angleBetweenHandles = -angleBetweenHandles
    handle1 = rotateVectorByAngle(handle1, -angleBetweenHandles/2)
    handle2 = rotateVectorByAngle(handle2, angleBetweenHandles/2)

    return handle1, handle2"""