# coding:utf-8
import sys

from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import QColor, QPixmap, QIcon, QPalette
from PyQt6.QtWidgets import QApplication, QLabel

from qframelesswindow import FramelessWindow, TitleBar, StandardTitleBar
import Styles
from . import CustomTitleBar

class MainWindow(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setAcceptDrops(True)
        # change the default title bar if you like
        self.setTitleBar(CustomTitleBar(self))
        self.setAutoFillBackground(True)
        
        #self.label = QLabel(self)
        #self.label.setScaledContents(True)
        #self.label.setPixmap(QPixmap("Window/icons/LoneHeeg.png"))
        self.editor = None

        self.setWindowIcon(QIcon("Window/icons/CutHeeg.png"))
        self.setWindowTitle("HedgeAuto")
        self.setStyleSheet(Styles.windowStyle)
        self.setMinimumSize(1000,600)
        self.setMinimumSize(400,200)
        #self.setStyleSheet("background:rgb(25,25,25)")

        self.titleBar.raise_()

        

        

        # customize the area of system title bar button, only works for macOS
        if sys.platform == "darwin":
            self.setSystemTitleBarButtonVisible(True)
            self.titleBar.minBtn.hide()
            self.titleBar.maxBtn.hide()
            self.titleBar.closeBtn.hide()

    def resizeEvent(self, e):
        # don't forget to call the resizeEvent() of super class
        super().resizeEvent(e)
        length = min(self.width(), self.height())
        if(self.editor == None): return

        self.editor.resize(self.width(), self.height()-30)
        self.editor.move(
            0,
            30
        )

    def systemTitleBarRect(self, size: QSize) -> QRect:
        """ Returns the system title bar rect, only works for macOS

        Parameters
        ----------
        size: QSize
            original system title bar rect
        """
        return QRect(size.width() - 75, 0, 75, size.height())
    def dragEnterEvent(self, e):
        e.accept()