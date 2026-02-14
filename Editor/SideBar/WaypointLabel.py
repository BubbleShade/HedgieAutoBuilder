import sys

from PyQt6.QtCore import Qt, QMimeData, pyqtSignal, QRegularExpression, QPointF
from PyQt6.QtGui import QBrush, QPainter, QPen, QContextMenuEvent, QDrag, QPixmap, QRegularExpressionValidator
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
    QLabel,
    QMenu,
    QLineEdit,
    QFrame
)
import Styles, Tools
from .. import FieldMap

class WaypointLabel(QFrame):
    def __init__(self, name : str, waypointHandler = None, parentLayout : QVBoxLayout = None):
        super().__init__()
        self.handler = waypointHandler

        self.label = QLabel(name)

        self.xInput = QLineEdit()
        self.yInput = QLineEdit()

        self.xInput.setValidator(QRegularExpressionValidator(QRegularExpression('/^[^.]*.[^.]*$|^[0-9.-]*$/')))
        self.yInput.setValidator(QRegularExpressionValidator(QRegularExpression('/^[^.]*.[^.]*$|^[0-9.-]*$/')))


        self.waypointHandler = waypointHandler
        self.parentLayout = parentLayout
        self.setMaximumHeight(45)
        self.setFixedHeight(45)
        self.setMaximumWidth(250)

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet(Styles.waypointLabelStyle)


        #self.xInput.setMaximumWidth(20)
        #self.yInput.setMaximumWidth(20)





        self.lay = QHBoxLayout(self)
        self.lay.addWidget(self.label)
        self.lay.addWidget(self.xInput)
        self.lay.addWidget(self.yInput)

        self.setLayout(self.lay)
        self.updatePosition()
        self.waypointHandler.poseDisplay.movedSignal.connect(self.updatePosition)

        self.xInput.textChanged.connect(self.updateX)

    def updateX(self, newText: str):
        if(self.handler.poseDisplay != None):
            fieldMap : FieldMap = self.handler.poseDisplay.scene.fieldMap
            x= Tools.parseFloatString(newText)
            
            self.handler.poseDisplay.setX(fieldMap.field_pos_to_screen(QPointF(x,0)).x())

    def updateY(self, newText: str):
        if(self.handler.poseDisplay != None):
            self.handler.poseDisplay.setX(Tools.parseFloatString(newText))
        




    def updatePosition(self):
        x, y = self.handler.x(), self.handler.y()

        if(self.handler.poseDisplay != None):
            fieldMap : FieldMap = self.handler.poseDisplay.scene.fieldMap
            pos = fieldMap.screen_pos_to_field(QPointF(x,y))
            x, y = pos.x(), pos.y()
        if(not self.xInput.hasFocus() and not self.yInput.hasFocus()):
            self.xInput.setText(str(round(x,3)))
            self.yInput.setText(str(round(y,3)))

        


    def swapEvent(self, oldIndex, newIndex):
        if(self.waypointHandler == None): return
        w = self.waypointHandler.parentPath.swapIndexes(oldIndex, newIndex)

    def contextMenuEvent(self, event : QContextMenuEvent):
        context_menu = QMenu()
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = context_menu.addAction("Delete")
        deleteButton.triggered.connect(self.waypointHandler.delete)
        context_menu.exec(event.globalPos()) 
    def delete(self):
        #if(self.pose != None): self.pose.delete()
        self.parentLayout.removeWidget(self)
        self.hide()
    def mouseMoveEvent(self, e):

        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)
