import sys
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal, QRegularExpression, QPointF
from PyQt6.QtGui import QBrush, QPainter, QPen, QContextMenuEvent, QDrag, QPixmap, QRegularExpressionValidator, QCursor
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
    QFrame,
    QComboBox,
    QToolButton
    
)
import Styles, Tools
from .. import FieldMap

class CommandGroupSideBarItem(QFrame):
    def __init__(self, name : str, commandGroupHandler = None):
        super().__init__()
        self.lay = QVBoxLayout()
        self.topPart = QFrame()
        self.topPartLay = QHBoxLayout()


        self.label = QComboBox()
        self.label.addItems(["Sequential Command Group", "Parrellel Command Group"])
        self.toolButton = QToolButton()
        self.toolButton.setArrowType(Qt.ArrowType.DownArrow)
        self.topPartLay.addWidget(self.label)
        self.topPartLay.addWidget(self.toolButton)
        self.topPart.setLayout(self.topPartLay)
        self.lay.addWidget(self.topPart)
        self.lay.setAlignment(self.topPart, Qt.AlignmentFlag.AlignTop)


        #self.label.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.commandGroupHandler = commandGroupHandler

        self.setStyleSheet(Styles.commandGroupStyle)
        self.setLayout(self.lay)

    def swapEvent(self, oldIndex, newIndex):
        if(self.waypointHandler == None): return
        w = self.waypointHandler.parentPath.swapIndexes(oldIndex, newIndex)

    def contextMenuEvent(self, event : QContextMenuEvent):
        context_menu = QMenu()
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = context_menu.addAction("Delete")
        context_menu.exec(event.globalPos()) 
    def delete(self):
        #if(self.pose != None): self.pose.delete()
        self.parentLayout.removeWidget(self)
        self.hide()
