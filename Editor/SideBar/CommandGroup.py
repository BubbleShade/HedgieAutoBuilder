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
        self.collapsed = False


        self.label = QComboBox()
        self.label.addItems(["Sequential Command Group", "Parrellel Command Group"])
        self.toolButton = QToolButton()
        self.toolButton.pressed.connect(self.collapse)
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
    @staticmethod
    def setVisibilityForLayout(layout : QHBoxLayout, visible : bool):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if(item.widget() != None):
                item.widget().setVisible(visible)
            if(item.layout() != None): 
                CommandGroupSideBarItem.setVisibilityForLayout(item.layout(), visible)
    def collapse(self):
        if(self.collapsed):
            self.collapsed = False
            CommandGroupSideBarItem.setVisibilityForLayout(self.lay, True)

            self.toolButton.setArrowType(Qt.ArrowType.DownArrow)
            # for i in range(self.lay.count()):
            #     self.lay.itemAt(i).show()
            return
        self.collapsed = True
        CommandGroupSideBarItem.setVisibilityForLayout(self.lay, False)
        self.topPart.show()
        #self.setVisibilityForLayout(self.topPart, True)
        # for i in range(self.lay.count()):
        #         self.lay.itemAt(i).hide()
        self.toolButton.setArrowType(Qt.ArrowType.RightArrow)
        
    def swapEvent(self, oldIndex, newIndex):
        if(self.waypointHandler == None): return
        w = self.waypointHandler.parentPath.swapIndexes(oldIndex, newIndex)

    def contextMenuEvent(self, event : QContextMenuEvent):
        context_menu = QMenu()
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = context_menu.addAction("Delete Command Group")
        context_menu.exec(event.globalPos()) 
    def delete(self):
        #if(self.pose != None): self.pose.delete()
        self.parentLayout.removeWidget(self)
        self.hide()
