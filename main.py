import sys

from PyQt6.QtWidgets import QApplication
from Window import MainWindow
from Editor.editor import Editor


app = QApplication(sys.argv)

window = MainWindow()
window.editor = Editor(window)



window.show()


app.exec()
