from PyQt6.QtCore import QPointF
from .. import PointDisplay, Action
from Tools import magnitude

class Waypoint():
    def __init__(self, parentPath = None, x = 0, y = 0, heading = None):
        self.startX = x
        self.startY = y

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
        if(self.poseDisplay != None): return self.poseDisplay.x()
        return self.startX
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

    def addDisplay(self, scene):
        self.poseDisplay = PointDisplay(scene, self, has_rotation=self.startHeading != None)
        self.poseDisplay.setPos(self.startX, self.startY)
        if(self.startHeading != None):
            self.poseDisplay.setRotation(self.startHeading)
            
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