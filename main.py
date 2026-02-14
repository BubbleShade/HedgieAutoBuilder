import sys

from PyQt6.QtWidgets import QApplication
from Window import MainWindow
from Editor import Editor
from Home import Home

app = QApplication(sys.argv)

window = MainWindow()
#window.editor = Editor(window)
#window.editor.hide()
editor = Editor(window)
window.editor = Home(window, editor) 
window.editor.show()

window.show()

app.exec()
