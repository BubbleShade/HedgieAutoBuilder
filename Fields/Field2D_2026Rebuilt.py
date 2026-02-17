import sys
from PyQt6.QtCore import Qt, QPointF, QEvent, QRectF
from PyQt6.QtCore import pyqtSignal as Signal
from PyQt6.QtGui import QBrush, QPainter, QPen
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
    QGraphicsScene,
    QMenu,
    QGraphicsObject
)
import Styles
from Tools import Arrow, ArrowDrawer
import json

def inchesAsMeters(inches):
    return inches * 0.0254

class FieldObject():
    def drawRed(self, painter, option):
        for i in self.rects:
            painter.drawRect(i)
    def drawBlue(self, painter, option):
        for i in self.rects:
            painter.drawRect(self.rotateRect(self.map, i))
    @staticmethod
    def rotate(map, point: QPointF):
        print(map.boundingRect().width())

        return map.box - point
    @staticmethod
    def rotateRect(map, rect: QRectF):
        return QRectF(FieldObject.rotate(map,rect.topLeft()), FieldObject.rotate(map,rect.bottomRight()))

redHubPos = QPointF(182.11, 158.845)
redHubWidth = 47
class Hub(FieldObject):
    def __init__(self,map):
        self.map = map

        self.topLeft = map.inch_pos_to_screen(redHubPos + QPointF(-redHubWidth/2, redHubWidth/2))
        self.bottomRight = map.inch_pos_to_screen(redHubPos + QPointF(redHubWidth/2, -redHubWidth/2))

        self.rects = [QRectF(self.topLeft, self.bottomRight)]
bumpWidth = 44.5
bumpLength = 73
class Bumps(FieldObject):
    def __init__(self,map):
        self.map = map

        self.topLeft = map.inch_pos_to_screen(redHubPos + QPointF(-bumpWidth/2, bumpWidth/2 + bumpLength))
        self.topRight = map.inch_pos_to_screen(redHubPos + QPointF(bumpWidth/2, bumpWidth/2))

        self.bottomLeft = map.inch_pos_to_screen(redHubPos + QPointF(-bumpWidth/2, -bumpWidth/2 - bumpLength))
        self.bottomRight = map.inch_pos_to_screen(redHubPos + QPointF(bumpWidth/2, -bumpWidth/2))

        self.rects = [QRectF(self.topLeft, self.topRight), 
                      QRectF(self.bottomLeft, self.bottomRight)]

class Bumperson(FieldObject):
    def __init__(self,map):
        self.map = map
        width = 0.75

        self.topLeft = map.inch_pos_to_screen(redHubPos + QPointF(-width, bumpWidth/2 + bumpLength))
        self.topRight = map.inch_pos_to_screen(redHubPos + QPointF(width, bumpWidth/2))

        self.bottomLeft = map.inch_pos_to_screen(redHubPos + QPointF(-width, -bumpWidth/2 - bumpLength))
        self.bottomRight = map.inch_pos_to_screen(redHubPos + QPointF(width, -bumpWidth/2))

        self.rects = [QRectF(self.topLeft, self.topRight), 
                      QRectF(self.bottomLeft, self.bottomRight)]

trenchBlockLength = 12
class TrencherSon(FieldObject):
    def __init__(self,map):
        self.map = map

        self.rects = []
        topLeft = map.inch_pos_to_screen(redHubPos + QPointF(-redHubWidth/2, redHubWidth/2 + bumpLength + trenchBlockLength))
        bottomRight = map.inch_pos_to_screen(redHubPos + QPointF(redHubWidth/2, redHubWidth/2 + bumpLength-1))

        self.rects.append(QRectF(topLeft, bottomRight))

        topLeft = map.inch_pos_to_screen(redHubPos + QPointF(-redHubWidth/2, -redHubWidth/2 - bumpLength - trenchBlockLength))
        bottomRight = map.inch_pos_to_screen(redHubPos + QPointF(redHubWidth/2, -redHubWidth/2 - bumpLength+1))

        self.rects.append(QRectF(topLeft, bottomRight))        
trenchLength = 53
trenchWidth = 4
class Trench(FieldObject):
    def __init__(self,map):
        self.map = map

        self.rects = []
        topLeft = map.inch_pos_to_screen(redHubPos + QPointF(-trenchWidth/2, redHubWidth/2 + bumpLength + trenchBlockLength + trenchLength))
        bottomRight = map.inch_pos_to_screen(redHubPos + QPointF(trenchWidth/2, redHubWidth/2 + bumpLength + trenchBlockLength))

        self.rects.append(QRectF(topLeft, bottomRight))

        topLeft = map.inch_pos_to_screen(redHubPos + QPointF(-trenchWidth/2, -redHubWidth/2 - bumpLength - trenchBlockLength - trenchLength))
        bottomRight = map.inch_pos_to_screen(redHubPos + QPointF(trenchWidth/2, -redHubWidth/2 - bumpLength + trenchBlockLength))

        self.rects.append(QRectF(topLeft, bottomRight))        

class RebuiltMap(QGraphicsObject):
    def __init__(self):
        super().__init__()
        # Opening JSON file
        self.widthInches = 656.75
        self.pxWidth = 1024
        self.heightInches = 317.69

        self.factor = inchesAsMeters(self.widthInches) / self.pxWidth
        self.box = self.inch_pos_to_screen(QPointF(self.widthInches, self.heightInches))

        self.hub = Hub(self)
        self.bump = Bumps(self)
        self.trencherson = TrencherSon(self)
        self.trench = Trench(self)
        self.bumperson = Bumperson(self)

            
    def getFieldImagePath(self) -> str:
        return self.path + "image.png"
    def getCenter(self) -> QPointF:
        return self.widthInches / 2
    def getRedCenter(self) -> QPointF:
        return self.getCenter() - QPointF(self.getCenter().x()/2, 0)
    def screen_pos_to_field(self, screenPos : QPointF) -> QPointF:
        return QPointF(screenPos.x() * self.factor, screenPos.y() * self.factor)
    def field_pos_to_screen(self, screenPos : QPointF) -> QPointF:
        return QPointF(screenPos.x() / self.factor, screenPos.y() / self.factor)
    def inch_pos_to_screen(self, screenPos : QPointF) -> QPointF:
        return QPointF(inchesAsMeters(screenPos.x()) / self.factor, inchesAsMeters(screenPos.y()) / self.factor)
    
    
    def paint(self, painter, option, widget = ...):
        botRight = self.inch_pos_to_screen(QPointF(self.widthInches, self.heightInches))
        painter.setPen(QPen(Styles.toothpasteWhite, 5))
        painter.setBrush(QBrush(Styles.veryDarkGray))
        painter.drawRect(QRectF(QPointF(0,0), botRight))

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(Styles.toothpasteWhite))
        painter.drawRect(QRectF(QPointF(botRight.x()/2 - 3,0), QPointF(botRight.x()/2 + 3, botRight.y())))
        painter.setBrush(QBrush(Styles.black))
        painter.drawRect(QRectF(QPointF(0,botRight.y()/2 - 3), QPointF(botRight.x(), botRight.y()/2 + 3)))


        Styles.redStyle.set_painter(painter)
        self.bump.drawRed(painter, option)
        self.trench.drawRed(painter, option)
        Styles.darkRedStyle.set_painter(painter)
        self.hub.drawRed(painter, option)
        self.trencherson.drawRed(painter, option)
        Styles.darkRedOutline.set_painter(painter)
        self.bumperson.drawRed(painter,option)


        
        

        Styles.blueStyle.set_painter(painter)
        self.bump.drawBlue(painter, option)
        self.trench.drawBlue(painter, option)
        Styles.darkBlueStyle.set_painter(painter)
        self.hub.drawBlue(painter, option)
        self.trencherson.drawBlue(painter, option)
        Styles.darkBlueOutlineStyle.set_painter(painter)
        self.bumperson.drawBlue(painter,option)

        

    def boundingRect(self):
        return QRectF(QPointF(-5,-5), self.inch_pos_to_screen(QPointF(self.widthInches, self.heightInches) + QPointF(5,5)))
    