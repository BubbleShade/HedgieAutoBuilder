from PyQt6.QtCore import QSize, Qt, QEvent
from PyQt6.QtGui import QPalette, QColor, QFont
from PyQt6.QtWidgets import QPushButton, QToolButton
from qframelesswindow import StandardTitleBar
import Styles

class CustomTitleBar(StandardTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        
        self.hBoxLayout.removeWidget(self.titleLabel)
        self.titleLabel.hide()

        self.backButton = QToolButton()
        self.backButton.setArrowType(Qt.ArrowType.LeftArrow)

        self.hBoxLayout.insertWidget(2,self.backButton)
        self.backButton.setStyleSheet(Styles.toolbarStyle)
        self.backButton.setMinimumSize(QSize(20,32))
        self.backButton.setFont(QFont("'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", 10))
        #self.backButton.hide()
        
        self.fileButton = QPushButton("File")
        
        self.hBoxLayout.insertWidget(3,self.fileButton)
        self.fileButton.setStyleSheet(Styles.toolbarStyle)
        self.fileButton.setMinimumSize(QSize(46,32))
        self.fileButton.setFont(QFont("'Segoe UI', Tahoma, Geneva, Verdana, sans-serif", 10))

        

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