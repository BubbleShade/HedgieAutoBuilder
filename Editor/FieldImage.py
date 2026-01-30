from PyQt6.QtCore import QRectF, QPointF
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsItem
# importing the module
import json


class FieldMap():
    def __init__(self, path : str):
        
        if(path.endswith("/")):
            self.path = path
        else:
            self.path = path + "/"
        # Opening JSON file
        with open(self.path + "config.json") as json_file:
            self.config = json.load(json_file)
        self.topLeft = QPointF(*self.config["topLeft"])
        self.bottomRight = QPointF(*self.config["bottomRight"])
        self.widthInches = self.config["widthInches"]
        self.heightInches = self.config["heightInches"]

        self.xFactor = (self.widthInches * 0.0254) / (self.bottomRight.x() - self.topLeft.x())
        self.yFactor = (self.heightInches * 0.0254) / (self.bottomRight.y() - self.topLeft.y())

        print(self.xFactor, self.yFactor)

            
    def getFieldImagePath(self) -> str:
        return self.path + "image.png"
    def getCenter(self) -> QPointF:
        return (self.bottomRight - self.topLeft)/2 + self.topLeft
    def getRedCenter(self) -> QPointF:
        print(self.getCenter())
        return self.getCenter() - QPointF(self.getCenter().x()/2, 0)
    def screen_pos_to_field(self, screenPos : QPointF) -> QPointF:
        return QPointF(screenPos.x() * self.xFactor, screenPos.y() * self.yFactor)
    def field_pos_to_screen(self, screenPos : QPointF) -> QPointF:
        return QPointF(screenPos.x() / self.xFactor, screenPos.y() / self.yFactor)

class FieldImage(QGraphicsItem):
    def __init__(self, fieldMap : FieldMap, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap(fieldMap.getFieldImagePath())
        self.setZValue(-1000)
        self.fieldMap = fieldMap
        x, y = self.fieldMap.config["topLeft"]
        self.setPos(-x,-y)
        #self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable) # Make it movable

    def boundingRect(self):
        # Return the area the item occupies
        return QRectF(0, 0, self.pixmap.width(), self.pixmap.height())

    def paint(self, painter, option, widget=None):
        # Draw the pixmap at the item's position
        painter.drawPixmap(0, 0, self.pixmap)