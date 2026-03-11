import sys

from PyQt6.QtWidgets import QApplication
app = QApplication(sys.argv)

from Window import MainWindow
from Editor import Editor
from Home import Home


window = MainWindow()
#window.editor = Editor(window)
#window.editor.hide()
editor = Editor(window)
window.editor = Home(window, editor) 
window.editor.show()

window.show()

app.exec()
