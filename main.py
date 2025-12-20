import sys

from PyQt6.QtCore import QSize, Qt, QEvent
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QToolButton, QStyle
from Editor import Editor
from Window.CustomWindow import MainWindow

app = QApplication(sys.argv)

# Optionally, setting the style to 'Fusion' can make the rest of the UI consistent
#app.setStyle('Fusion') 

from pyqt_custom_titlebar_window.customTitlebarWindow import CustomTitlebarWindow

window = MainWindow()

window.show()


app.exec()