from .. import PointDisplay, Action

class Waypoint():
    def __init__(self, parentPath = None, x = 0, y = 0, rotation = None):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.parentPath = parentPath
        self.poseDisplay = None
    def setParent(self, parentPath):
        self.parentPath = parentPath

    def addDispalay(self, scene):
        self.poseDisplay = PointDisplay(scene, self, has_rotation=self.rotation != None)
        self.poseDisplay.setPos(self.x, self.y)
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