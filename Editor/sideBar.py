import sys

from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QBrush, QPainter, QPen, QContextMenuEvent, QDrag, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsView,
    QHBoxLayout,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
    QLabel,
    QMenu,
    
)
#from . import PoseDisplay
from . import PoseDisplay
import Styles

class DragWidget(QWidget):
    """
    Generic list sorting handler.
    """

    orderChanged = pyqtSignal(list)

    def __init__(self, *args, orientation=Qt.Orientation.Vertical, **kwargs):
        super().__init__()
        self.setAcceptDrops(True)

        # Store the orientation for drag checks later.
        self.orientation = orientation

        if self.orientation == Qt.Orientation.Vertical:
            self.blayout = QVBoxLayout()
        else:
            self.blayout = QHBoxLayout()

        self.setLayout(self.blayout)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        pos = e.position()
        widget = e.source()
        self.blayout.removeWidget(widget)

        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            if self.orientation == Qt.Orientation.Vertical:
                # Drag drop vertically.
                drop_here = pos.y() < w.y() + w.size().height() // 2
            else:
                # Drag drop horizontally.
                drop_here = pos.x() < w.x() + w.size().width() // 2

            if drop_here:
                break

        else:
            # We aren't on the left hand/upper side of any widget,
            # so we're at the end. Increment 1 to insert after.
            n += 1

        self.blayout.insertWidget(n, widget)
        self.orderChanged.emit(self.get_item_data())

        e.accept()

    def add_item(self, item):
        self.blayout.addWidget(item)
        self.orderChanged.emit(self.get_item_data())
    def remove_item(self, item):
        self.blayout.removeWidget(item)
        self.orderChanged.emit(self.get_item_data())

    def get_item_data(self):
        data = []
        for n in range(self.blayout.count()):
            # Get the widget at each index in turn.
            w = self.blayout.itemAt(n).widget()
            data.append(w)
        return data

class PoseLabel(QLabel):
    def __init__(self, name : str, pose = None, parentLayout : QVBoxLayout = None):
        super().__init__(name)
        self.pose = pose
        self.parentLayout = parentLayout
    def contextMenuEvent(self, event : QContextMenuEvent):
        context_menu = QMenu()
        context_menu.setStyleSheet(Styles.contextMenuStyle)
        deleteButton = context_menu.addAction("Delete")
        deleteButton.triggered.connect(self.delete)
        context_menu.exec(event.globalPos()) 
    def delete(self):
        if(self.pose != None): self.pose.delete()
        print("hello")
        self.parentLayout.remove_item(self)
    def mouseMoveEvent(self, e):
        if e.buttons() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime = QMimeData()
            drag.setMimeData(mime)

            pixmap = QPixmap(self.size())
            self.render(pixmap)
            drag.setPixmap(pixmap)

            drag.exec(Qt.DropAction.MoveAction)


class PathLabel(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.poseLayout = DragWidget()
        self.poses = []
        self.addWidget(QLabel("Follow Path: "))
        self.addWidget(self.poseLayout)
    def addPoseLabel(self, poseLabel):
        self.poseLayout.add_item(poseLabel)
    def addPose(self, name : str, pose = None):
        poseLabel = PoseLabel(name, pose=pose, parentLayout=self.poseLayout)
        self.poses.append(poseLabel)
        self.poseLayout.add_item(poseLabel)


class SideBar(QVBoxLayout):
    def __init__(self, parent = None):
        super().__init__(parent)         

        up = QPushButton("Up")
        self.addWidget(up)

        down = QPushButton("Down")
        self.addWidget(down)

        rotate = QSlider()
        rotate.setRange(0, 360)
        self.addWidget(rotate)
        self.i = 0
    def addPathLabel(self, pathLabel):
        self.addLayout(pathLabel)
    def CreatePoseLabel(self, pose, name = None):
        if(name == None):
            self.i += 1
            return PoseLabel(f"Pose {self.i}", pose)
        return PoseLabel(name, pose)