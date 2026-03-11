from . import Waypoint
from ..import SideBar, PathSidebarItem, FieldMap
from ..SideBar import WaypointSidebarItem
import Tools

class InitialPose(Waypoint):
    def __init__(self, x=0, y=0, heading=0):
        super().__init__(None, x, y, heading)
        self.sideBarItem = PathSidebarItem(self)
        
        self.poseLabel = WaypointSidebarItem("Waypoint", self)
        self.sideBarItem.addPoseLabel(self.poseLabel)
        self.sideBarItem.pathLabel.setText("InitialPose")


    def delete(self, isRecursive=False):
        if(self.sideBarItem != None and self.sideBarItem.isVisible()):

            self.sideBarItem.hide()
            self.sideBarItem.deleteLater()
        super().delete(isRecursive)
        
    @staticmethod
    def fromJsonFile(json : dict, fieldMap : FieldMap):
        pos = fieldMap.field_pos_to_screen(Tools.pointFromJson(json["anchor"]))
        waypoint = InitialPose(x = pos.x(), y=  pos.y(), heading=json["anchor"]["heading"])

        if(json["prevControl"] != None):
            waypoint.ctrlPoint2 = fieldMap.field_pos_to_screen(Tools.pointFromJson(json["prevControl"]))
        if(json["nextControl"] != None):
            waypoint.ctrlPoint1 = fieldMap.field_pos_to_screen(Tools.pointFromJson(json["nextControl"]))
        return waypoint
