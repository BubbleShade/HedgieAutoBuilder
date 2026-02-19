from . import Waypoint
from ..import SideBar, PathLabel

class InitialPose(Waypoint):
    def __init__(self, x=0, y=0, heading=0):
        super().__init__(None, x, y, heading)
        self.sideBarItem = None
    def addToSideBar(self, sideBar : SideBar):
        self.sideBarItem = PathLabel()
        sideBar.addPathLabel(self.sideBarItem)
        self.poseLabel = sideBar.create_waypoint_label(self)
        self.sideBarItem.addPoseLabel(self.poseLabel)
        self.sideBarItem.pathLabel.setText("InitialPose")
    def delete(self, isRecursive=False):
        super().delete(isRecursive)
        if(self.sideBarItem != None):
            self.sideBarItem.hide()
            self.sideBarItem.deleteLater()