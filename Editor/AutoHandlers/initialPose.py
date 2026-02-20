from . import Waypoint
from ..import SideBar, PathSidebarItem, FieldMap
import Tools

class InitialPose(Waypoint):
    def __init__(self, x=0, y=0, heading=0):
        super().__init__(None, x, y, heading)
        self.sideBarItem = None
    def addToSideBar(self, sideBar : SideBar):
        self.sideBarItem = PathSidebarItem()
        sideBar.addSideBarLayout(self.sideBarItem)
        self.poseLabel = sideBar.create_waypoint_label(self)
        self.sideBarItem.addPoseLabel(self.poseLabel)
        self.sideBarItem.pathLabel.setText("InitialPose")
    def delete(self, isRecursive=False):
        super().delete(isRecursive)
        if(self.sideBarItem != None):
            self.sideBarItem.hide()
            self.sideBarItem.deleteLater()
    @staticmethod
    def fromJsonFile(json : dict, fieldMap : FieldMap):
        pos = fieldMap.field_pos_to_screen(Tools.pointFromJson(json["anchor"]))
        waypoint = InitialPose(x = pos.x(), y=  pos.y(), heading=json["anchor"]["heading"])

        if(json["prevControl"] != None):
            waypoint.ctrlPoint2 = fieldMap.field_pos_to_screen(Tools.pointFromJson(json["prevControl"]))
        if(json["nextControl"] != None):
            waypoint.ctrlPoint1 = fieldMap.field_pos_to_screen(Tools.pointFromJson(json["nextControl"]))
        return waypoint
