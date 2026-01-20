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

            
    def getFieldImagePath(self) -> str:
        return self.path + "image.png"
    def getCenter(self) -> QPointF:
        return (self.bottomRight - self.topLeft)/2 + self.topLeft
    def getRedCenter(self) -> QPointF:
        print(self.getCenter())
        return self.getCenter() - QPointF(self.getCenter().x()/2, 0)

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