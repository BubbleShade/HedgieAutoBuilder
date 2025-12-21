import sys

from PyQt6.QtCore import QSize, Qt, QEvent, QPointF,QRectF
from PyQt6.QtGui import QPalette
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QWidget, QToolButton, QStyle

def get_center(rect : QRectF):
    return QPointF(rect.width()/2, rect.height()/2)