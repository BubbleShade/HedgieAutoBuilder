from .. import PointDisplay, PathSidebarItem, SideBar, PathDrawer
from . import Waypoint
import Styles
import Tools
from PyQt6.QtWidgets import QGraphicsScene

from .. import FieldMap
from ..SideBar import NamedCommandSidebarItem

class NamedCommand():
    def __init__(self, name : str):
 
        self.name = name
        self.sideBarItem = None
        self.parentAuto = None
    
    def getDrawerWaypoints(self):
        return self.parentAuto

    def scene(self):
        if(self.parentAuto != None): return self.parentAuto.scene
        else: return None
            
    def addToScene(self, scene : QGraphicsScene): pass

    def addToStaticScene(self, scene : QGraphicsScene): pass

    def addToSideBar(self, sideBar : SideBar):
        self.sideBarItem = NamedCommandSidebarItem(self.name, self)
        sideBar.addSideBarWidget(self.sideBarItem)
    
    def delete(self):
        if(self.sideBarItem != None):
            self.sideBarItem.hide()
            self.sideBarItem.deleteLater()

    def getJson(self, fieldMap : FieldMap):
        waypointJsonList = []
        for waypoint in self.waypoints:
            waypoint.addToJson(waypointJsonList, fieldMap)
        return waypointJsonList
    
    @staticmethod
    def fromJsonFile(pathList, fieldMap : FieldMap):
        waypoints = []
        for i in pathList:
            waypoints.append(Waypoint.fromJsonFile(i, fieldMap))
        return Path(waypoints)
    



