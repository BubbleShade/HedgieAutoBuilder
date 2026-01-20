from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtCore import Qt

with open("Styles/contextMenu.qss","r") as file:
    contextMenuStyle = file.read()
with open("Styles/Window/windowStyle.qss","r") as file:
    windowStyle = file.read()
with open("Styles/editorStyle.qss","r") as file:
    editorStyle = file.read()

class Style():
    def __init__(self, pen : QPen, brush : QBrush = None):
        self.pen = pen
        self.brush = brush
    def set_painter(self, painter):
        painter.setPen(self.pen)
        if(self.brush != None): painter.setBrush(self.brush)



toothpasteWhite = QColor(221, 226, 235)
toothPasteGray = QColor(130, 132, 135)
darkishGray = QColor(73, 74, 74)
darkerGray = QColor(56, 56, 56)

darkGray = QColor(38, 38, 38)
veryDarkGray = QColor(28, 28, 28)
black = QColor(0,0,0)

poseStyle = Style(QPen(darkGray, 3, cap = Qt.PenCapStyle.SquareCap))
waypointStyle = Style(QPen(darkGray, 3, cap = Qt.PenCapStyle.SquareCap), QBrush(darkerGray))
curveStyle = Style(QPen(darkishGray, 2, cap = Qt.PenCapStyle.SquareCap), Qt.BrushStyle.NoBrush)
bezierHandleStyle = Style(QPen(darkerGray, 3), QBrush(darkishGray))


