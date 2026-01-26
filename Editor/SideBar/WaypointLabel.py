import sys

from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QBrush, QPainter, QPen, QContextMenuEvent, QDrag, QPixmap
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
    QMenu
)
import Styles

class WaypointLabel(QLabel):
    def __init__(self, name : str, waypointHandler = None, parentLayout : QVBoxLayout = None):
        super().__init__()
        self.setText(name)
        self.waypointHandler = waypointHandler
        self.parentLayout = parentLayout
        self.setMaximumHeight(50)
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
