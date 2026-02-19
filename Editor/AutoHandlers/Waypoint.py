from PyQt6.QtCore import QPointF
from .. import PointDisplay, Action, FieldMap
from Tools import magnitude
import Tools
class Waypoint():
    def __init__(self, parentPath = None, x = 0, y = 0, heading = None):
        self.startX = x
        self.startY = y

        self.ctrlPoint1 = None
        self.ctrlPoint2 = None

        self.startHeading = heading
        self.hasHeading = heading != None

        self.parentPath = parentPath
        self.poseDisplay = None

    def setHeading(self, rotation):
        self.startHeading = rotation
        if(self.poseDisplay):
            self.poseDisplay.setHasRotation(True)
            self.poseDisplay.setRotation(rotation)
    def setHasHeading(self, hasHeading):
        self.poseDisplay.setHasRotation(hasHeading)
        if(hasHeading):
            if(self.startHeading == None): self.startHeading = 0.0
        else:
            self.startHeading = None
    def x(self) -> float:
        if(self.poseDisplay != None): return self.poseDisplay.x()
        return self.startX
    def y(self) -> float:
        if(self.poseDisplay != None): return self.poseDisplay.y()
        return self.startY
    def pos(self) -> QPointF:
        if(self.poseDisplay != None): 
            return self.poseDisplay.pos()
        return QPointF(self.startX, self.startY)
    def heading(self):
        if(self.poseDisplay != None and self.poseDisplay.canRotate):
            return self.poseDisplay.rotation()
        else:
            return self.startHeading
    def dist(self, pos) -> float:
        return magnitude(pos - self.pos())

    def setParent(self, parentPath):
        self.parentPath = parentPath

    def addDisplay(self, scene, isStatic = False):
        self.poseDisplay = PointDisplay(scene, self, has_rotation=self.startHeading != None, isStatic=isStatic)
        self.poseDisplay.setPos(self.startX, self.startY)
        if(self.startHeading != None):
            self.poseDisplay.setRotation(self.startHeading)
        if(self.ctrlPoint1 != None):
            self.poseDisplay.handle.handle1.setPos(self.ctrlPoint1)
        if(self.ctrlPoint2 != None):
            self.poseDisplay.handle.handle2.setPos(self.ctrlPoint2)
            
    def undoDelete(self):
        if(self.parentPath != None): 
            self.parentPath.addWaypoint(self, self.index)
        if(self.poseDisplay != None): self.poseDisplay.undoDelete()
    
    def delete(self, isRecursive = False):
        Action.addAction(Action.Action(self.undoDelete, self.delete))
        if(self.parentPath != None): 
            self.index = self.parentPath.waypoints.index(self)
            self.parentPath.remove(self)
            self.parentPath.updateScene(self.parentPath.scene())
        if(self.poseDisplay != None): self.poseDisplay.delete()

    def getDict(self, fieldMap : FieldMap):
        data = {}
        if(self.poseDisplay.handle.handle1.isVisible()):
            data["nextControl"] = [self.poseDisplay.handle.handle1.pos().x(), 
                                   self.poseDisplay.handle.handle1.pos().y()]
        else:
            data["nextControl"] = None

        if(self.poseDisplay.handle.handle2.isVisible()):
            data["prevControl"] = [self.poseDisplay.handle.handle2.pos().x(),
                                   self.poseDisplay.handle.handle2.pos().y()]
        else:
            data["prevControl"] = None
        
        data["anchor"] = [self.x(), self.y]
        return data
    def addToJson(self, waypointList : list, fieldMap : FieldMap):
        json = {}
        if(self.poseDisplay == None):
            raise RuntimeError("Attempted to export json file before waypoints indexed")
        if(self.poseDisplay.handle.handle1.isVisible()):
            handle1Pos = fieldMap.screen_pos_to_field(self.poseDisplay.handle.handle1.pos())
            json["nextControl"] = {"x":handle1Pos.x(), "y":handle1Pos.y()}
        else: json["nextControl"] = None
        if(self.poseDisplay.handle.handle2.isVisible()):
            handle2Pos = fieldMap.screen_pos_to_field(self.poseDisplay.handle.handle2.pos())
            json["prevControl"] = {"x":handle2Pos.x(), "y":handle2Pos.y()}
        else: json["prevControl"] = None
        anchorPos = fieldMap.screen_pos_to_field(self.pos())
        json["anchor"] = {"x":anchorPos.x(), "y":anchorPos.y()}
        if(self.poseDisplay.canRotate):
            json["anchor"]["heading"] = self.poseDisplay.rotation()
        else:
            json["anchor"]["heading"] = None
        waypointList.append(json)
    @staticmethod
    def fromJsonFile(json : dict, fieldMap : FieldMap):
        pos = fieldMap.field_pos_to_screen(Tools.pointFromJson(json["anchor"]))
        waypoint = Waypoint(x = pos.x(), y=  pos.y(), heading=json["anchor"]["heading"])

        if(json["prevControl"] != None):
            waypoint.ctrlPoint2 = fieldMap.field_pos_to_screen(Tools.pointFromJson(json["prevControl"]))
        if(json["nextControl"] != None):
            waypoint.ctrlPoint1 = fieldMap.field_pos_to_screen(Tools.pointFromJson(json["nextControl"]))
        return waypoint

