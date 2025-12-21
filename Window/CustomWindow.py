# coding:utf-8
import sys

from PyQt6.QtCore import QRect, QSize, Qt
from PyQt6.QtGui import QColor, QPixmap, QIcon, QPalette
from PyQt6.QtWidgets import QApplication, QLabel

from qframelesswindow import FramelessWindow, TitleBar, StandardTitleBar
from Editor.editor import Editor
import Styles
class CustomTitleBar(StandardTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)

        #self.setStyleSheet()
        buttons = [self.minBtn, self.maxBtn, self.closeBtn]
        for button in buttons:
            button.setNormalColor(QColor(242, 246, 250))
            button.setPressedColor(QColor(242, 246, 250))
            button.setHoverColor(QColor(242, 246, 250))

        for button in buttons[:-1]:
            button.setHoverBackgroundColor(QColor(62, 62, 66))
            button.setPressedBackgroundColor(QColor(54, 57, 65))
        
        # customize the style of title bar button
        

        # use qss to customize title bar button
        self.maxBtn.setStyleSheet("""
            TitleBarButton {
                qproperty-pressedColor: white;
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)
        #with open("./Window/windowStyle.qss","r") as file:
        #    self.setStyleSheet(file.read())
        #self.


class MainWindow(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # change the default title bar if you like
        self.setTitleBar(CustomTitleBar(self))
        self.setAutoFillBackground(True)
        
        #self.label = QLabel(self)
        #self.label.setScaledContents(True)
        #self.label.setPixmap(QPixmap("Window/icons/LoneHeeg.png"))
        self.editor = Editor(self)

        self.setWindowIcon(QIcon("Window/icons/LoneHeeg.png"))
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