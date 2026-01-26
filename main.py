import sys

from PyQt6.QtCore import QSize, Qt, QEvent, QPointF
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QToolButton, QStyle
from Editor import Editor
from Window.CustomWindow import MainWindow
from Tools import *
import math
app = QApplication(sys.argv)

# Optionally, setting the style to 'Fusion' can make the rest of the UI consistent
#app.setStyle('Fusion') 

#from pyqt_custom_titlebar_window.customTitlebarWindow import CustomTitlebarWindow

window = MainWindow()


    
#print(getHandlePos(QPointF(1,1),QPointF(0,0),QPointF(2,0)))
#print(rotateVectorByAngle(QPointF(1,1),math.pi))
window.show()


app.exec()
