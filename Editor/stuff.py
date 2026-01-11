from . import PoseDisplay, SideBar, PathLabel

class Pose():
    def __init__(self, parentPath = None, x = 0, y = 0):
        self.x = x
        self.y = y
        self.parentPath = parentPath
        self.poseDisplay = None
    def setParent(self, parentPath):
        self.parentPath = parentPath

    def addPoseDisplay(self, scene):
        self.poseDisplay = PoseDisplay(scene, self)
        self.poseDisplay.setPos(self.x, self.y)
    
    def delete(self, isRecursive = False):
        if(self.poseDisplay != None):
            self.poseDisplay.delete()

        





class Waypoint():
    def __init__():
        pass


class Path():
    def __init__(self, initialPose : Pose = None, endPose : Pose = None, waypoints : list[Waypoint] = []):
        if(initialPose != None): 
            initialPose.setParent(self)
            self.initialPose = initialPose
        else: self.initialPose = Pose(self)

        if(endPose != None): 
            self.endPose = endPose
            initialPose.setParent(self)

        else: self.endPose = Pose(self)

        self.waypoints = waypoints
        self.sideBarItem = None
    def addToScene(self, scene):
        self.initialPose.addPoseDisplay(scene)
        self.endPose.addPoseDisplay(scene)

    def addToSideBar(self, sideBar : SideBar):
        self.sideBarItem = PathLabel()
        sideBar.addPathLabel(self.sideBarItem)
        self.sideBarItem.addPoseLabel(sideBar.CreatePoseLabel(self.initialPose))
        self.sideBarItem.addPoseLabel(sideBar.CreatePoseLabel(self.endPose))



class Auto():
    def __init__(self, execution = []):
        self.execution = execution
    def addToScene(self, scene):
        for i in self.execution:
            if(i.addToScene !=  None):
                i.addToScene(scene)
    def addToSideBar(self, sideBar):
        for i in self.execution:
            i.addToSideBar(sideBar)




