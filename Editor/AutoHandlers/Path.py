from .. import PointDisplay, PathLabel, SideBar
from . import Waypoint
import Styles
from Tools import BezierCurve

def handlePoseComposer(pose : PointDisplay, handle):
    return lambda _ =  None: handle.centerPos() + pose.center()


class Path():
    def __init__(self, waypoints : list[Waypoint] = []):
        for i in range(2-len(waypoints)):
            waypoints.append(Waypoint(self, rotation=0))
        for waypoint in [waypoints[0], waypoints[-1]]:
            if(waypoint.rotation == None): waypoint.rotation = 0
 
        self.waypoints = waypoints
        for i in waypoints:
            i.setParent(self)
        self.sideBarItem = None
        self.curves = []
        self.poseLabels = {}
        self.parentAuto = None

    def scene(self):
        if(self.parentAuto != None): return self.parentAuto.scene
        else: return None

    def updateScene(self,scene):
        if(scene == None): return
        self.reBezier(scene)

    def remove(self, waypoint : Waypoint):
        self.waypoints.remove(waypoint)
        if(self.poseLabels[waypoint] != None):
            self.poseLabels[waypoint].delete()

    def reBezier(self,scene):
        for i in self.curves:
            scene.removeItem(i)
        self.curves = []
        data = self.waypoints

        pen = Styles.curveStyle.pen

        for i in data:
            i.poseDisplay.handle.hideHandles()
        
        for i in range(len(data)-1):
            pose1 = data[i].poseDisplay
            pose2 = data[i+1].poseDisplay

            pose1.handle.handle1.show()
            pose2.handle.handle2.show()

            curve = BezierCurve(pose1.center, pose2.center, 
                                handlePoseComposer(pose1, pose1.handle.handle1),
                                handlePoseComposer(pose2, pose2.handle.handle2))
                                #lambda _ =  None: pose1.handle.handle1.centerPos() + pose1.center(), 
                                #lambda _ = None: pose2.handle.handle2.centerPos() + pose2.center())

            curve.setPen(pen)
            scene.addItem(curve)
            self.curves.append(curve)
    def addWaypoint(self,waypoint : Waypoint,index = -1):
        self.waypoints.insert(index, waypoint)
        poseLabel = self.sideBarItem.create_waypoint_label(waypoint)
        self.poseLabels[waypoint] = poseLabel
        self.sideBarItem.addPoseLabel(poseLabel)
        self.updateScene(self.scene())

    def addToScene(self, scene):
        for i in self.waypoints:
            i.addDispalay(scene)
        self.reBezier(scene)

    def addToSideBar(self, sideBar : SideBar):
        self.sideBarItem = PathLabel()
        sideBar.addPathLabel(self.sideBarItem)
        for waypoint in self.waypoints:
            poseLabel = sideBar.create_waypoint_label(waypoint)
            self.poseLabels[waypoint] = poseLabel
            self.sideBarItem.addPoseLabel(poseLabel)