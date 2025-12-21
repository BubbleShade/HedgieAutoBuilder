from PyQt6.QtGui import QColor

with open("Styles/contextMenu.qss","r") as file:
    contextMenuStyle = file.read()
with open("Styles/Window/windowStyle.qss","r") as file:
    windowStyle = file.read()
with open("Styles/editorStyle.qss","r") as file:
    editorStyle = file.read()
toothpasteWhite = QColor(221, 226, 235)
toothPasteGray = QColor(130, 132, 135)
darkerGray = QColor(73, 74, 74)