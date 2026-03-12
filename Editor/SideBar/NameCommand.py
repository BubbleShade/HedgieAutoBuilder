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
    
)
import Styles, Tools
from .. import FieldMap

class NamedCommandSidebarItem(QFrame):
    def __init__(self, name : str, namedCommandHandler = None, parentLayout : QVBoxLayout = None):
        super().__init__()

        self.edit = QLineEdit(name)

        self.handler = namedCommandHandler
        self.parentLayout = parentLayout

        self.edit.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.edit.setFrame(False)
        self.setStyleSheet(Styles.namedCommandStyle)

        self.lay = QHBoxLayout(self)
        self.lay.addWidget(QLabel("Named Command: "))
        self.lay.addWidget(self.edit)
        self.setMaximumHeight(50)
        self.setLayout(self.lay)

        self.context = QMenu()
        
        self.addPathBelow = self.context.addAction("Add Path Below")
        self.addPathBelow.triggered.connect(self.handler.addPathBelow)
        
        self.addPathBelow = self.context.addAction("Add Named Command Below")
        self.addPathBelow.triggered.connect(self.handler.addNamedCommandBelow)
        
        self.context.addSection("Bannana")
        self.context.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = self.context.addAction("Delete")
        deleteButton.triggered.connect(self.handler.delete)


    def contextMenuEvent(self, event : QContextMenuEvent):
        self.context.exec(event.globalPos()) 

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
