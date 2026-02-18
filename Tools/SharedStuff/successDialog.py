import ntcore
from PyQt6.QtCore import QRect
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QDialog, QLineEdit, QPushButton
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression, QTimer

from PyQt6.QtGui import QPainter
import time

class SuccessDialog(QDialog):
    def __init__(self, text, title, parent=None):
        super(SuccessDialog, self).__init__(parent)
        self.setWindowTitle(title)
        
        # Create widgets
        layout = QVBoxLayout(self)
        label = QLabel(text)

        # Add widgets to layout
        layout.addWidget(label)
        self.setLayout(layout)

    def get_value(self):
        return self.name_input.text()