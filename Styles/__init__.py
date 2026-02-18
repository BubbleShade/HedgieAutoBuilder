from PyQt6.QtGui import QColor, QPen, QBrush
from PyQt6.QtCore import Qt

with open("Styles/contextMenu.qss","r") as file:
    contextMenuStyle = file.read()
with open("Styles/Window/windowStyle.qss","r") as file:
    windowStyle = file.read()
with open("Styles/editorStyle.qss","r") as file:
    editorStyle = file.read()
with open("Styles/ToolbarButtons.qss","r") as file:
    toolbarStyle = file.read()
    
with open("Styles/Editor/waypointLabel.qss","r") as file:
    waypointLabelStyle = file.read()
with open("Styles/Home/autoBox.qss","r") as file:
    autoBoxStyle = file.read()
with open("Styles/Home/home.qss","r") as file:
    homeStyle = file.read()

class Style():
    def __init__(self, pen : QPen, brush : QBrush = None):
        self.pen = pen
        self.brush = brush
    def set_painter(self, painter):
        painter.setPen(self.pen)
        if(self.brush != None): painter.setBrush(self.brush)



toothpasteWhite = QColor(221, 226, 235)
toothPasteGray = QColor(130, 132, 135)
gray = QColor(107, 107, 107)
darkishGray = QColor(73, 74, 74)
darkerGray = QColor(56, 56, 56)

darkGray = QColor(38, 38, 38)
veryDarkGray = QColor(28, 28, 28)
black = QColor(0,0,0)

poseStyle = Style(QPen(darkishGray, 3, cap = Qt.PenCapStyle.SquareCap))

darkRedOutline = Style(Qt.PenStyle.NoPen, QBrush(QColor(50,0,25)))
darkRedStyle = Style(Qt.PenStyle.NoPen, QBrush(QColor(200,0,0)))
redStyle = Style(Qt.PenStyle.NoPen, QBrush(QColor(255,0,0)))

darkBlueOutlineStyle = Style(Qt.PenStyle.NoPen, QBrush(QColor(25,0,50)))
darkBlueStyle = Style(Qt.PenStyle.NoPen, QBrush(QColor(0,0,200)))
blueStyle = Style(Qt.PenStyle.NoPen, QBrush(QColor(0,0,255)))

waypointStyle = Style(QPen(darkishGray, 3, cap = Qt.PenCapStyle.SquareCap), QBrush(gray))
curveStyle = Style(QPen(toothPasteGray, 3, cap = Qt.PenCapStyle.SquareCap), Qt.BrushStyle.NoBrush)
bezierHandleStyle = Style(QPen(gray, 3), QBrush(toothpasteWhite))



