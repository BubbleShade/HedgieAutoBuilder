import sys

from PyQt6.QtCore import Qt, QPoint, QRectF, QSize
from PyQt6.QtGui import QBrush, QPainter, QPen, QMouseEvent, QCursor
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
    QMenu,
    QGridLayout,
    QLabel,
    QBoxLayout,
    QFrame,
    QLineEdit
)
import json, os
from Editor import AutoViewer
#from . import PoseDisplay
import Styles
from Window import CustomTitleBar, CustomWindow

from Editor import Editor, Auto
import Tools
class AutoBox(QFrame):
    def __init__(self, parent : QWidget, AutoJsonPath = "D:\\Programming\\HedgieAutoBuilder\\New folder\\banana.json"):
        super().__init__(parent)
        self.setStyleSheet(Styles.autoBoxStyle)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.lay = QVBoxLayout(self)
        self.topPart = QHBoxLayout(self)
        self.name = QLineEdit(AutoJsonPath.split("\\")[-1].split(".")[0])
        self.name.setFrame(False)
        self.name.returnPressed.connect(self.rename)
        self.path = AutoJsonPath
        self.topPart.addWidget(self.name)
        self.contextButton = QPushButton("\u22EE")
        self.contextButton.setFixedSize(30,30)
        

        self.fileMenu = QMenu()
        self.fileMenu.setStyleSheet(Styles.contextMenuStyle)
    
        delete = self.fileMenu.addAction("Delete")
        duplicate = self.fileMenu.addAction("Duplicate")

        delete.triggered.connect(self.delete)

        duplicate.triggered.connect(self.duplicate)

        self.fileFun = lambda : self.fileMenu.exec(self.contextButton.mapToGlobal(QPoint(0,32)))
        self.contextButton.pressed.connect(self.fileFun)


        self.topPart.addWidget(self.contextButton)
        self.lay.addLayout(self.topPart)


        with open(AutoJsonPath, "r") as f:
            self.autoViewer = AutoViewer.fromJson(self, json.load(f), QRectF(0,0,190,170))
        self.view = QGraphicsView(self.autoViewer)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setMaximumSize(QSize(200,180))
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.guyFellow = parent

        self.lay.addWidget(self.view)
        self.view.mouseReleaseEvent = self.mouseReleaseEvent
    def delete(self):
        os.remove(self.path)
        self.guyFellow.updateLayouts()

    def rename(self):

        self.name.clearFocus()
        fileName = self.path.split("\\")[-1]
        directory = self.path.removesuffix(fileName)

        newFile = directory + self.name.text() + ".json"

        os.rename(self.path, newFile)
        self.path = newFile

    def duplicate(self):
        fileName = self.path.split("\\")[-1]
        directory = self.path.removesuffix(fileName)
        newPath = Tools.Files.newFileOfName(directory, fileName)
        with open(self.path, "r") as f:
            with open(directory + newPath, "w") as newF:
                json.dump(json.load(f), newF)
        self.guyFellow.updateLayouts()
        print(newPath)

    def mouseReleaseEvent(self, event : QMouseEvent):
        if(event.button() == Qt.MouseButton.LeftButton):
            ed : Editor =self.guyFellow.editor
            ed.scene.changeAutoFromFile(self.path)
            ed.back = self.guyFellow
            self.guyFellow.parent().setFocus(self.guyFellow.editor)
        
    