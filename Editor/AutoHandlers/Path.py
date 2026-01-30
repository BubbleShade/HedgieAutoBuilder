from .. import PointDisplay, PathLabel, SideBar, PathDrawer
from . import Waypoint
import Styles
import Tools
from PyQt6.QtWidgets import QGraphicsScene

from .. import FieldMap
def handlePoseComposer(pose : PointDisplay, handle):
    return lambda _ =  None: handle.centerPos() + pose.center()


class Path():
    def __init__(self, waypoints : list[Waypoint] = []):
        for i in range(2-len(waypoints)):
            waypoints.append(Waypoint(self, rotation=0))
        for waypoint in [waypoints[0], waypoints[-1]]:
            if(waypoint.startHeading == None): waypoint.setHeading(0)
 
        self.waypoints : list[Waypoint] = waypoints
        for i in waypoints:
            i.setParent(self)
        self.sideBarItem = None
        self.curves = []
        self.poseLabels = {}
        self.parentAuto = None
        self.pathDrawer = PathDrawer(self)
        self.name = "Path1"

    def scene(self):
        if(self.parentAuto != None): return self.parentAuto.scene
        else: return None

    def updateScene(self,scene : QGraphicsScene):
        if(scene == None): return
        self.pathDrawer.update()

    def remove(self, waypoint : Waypoint):
        self.waypoints.remove(waypoint)
        if(self.poseLabels[waypoint] != None):
            self.poseLabels[waypoint].delete()
    def swapIndexes(self, i1, i2):
        waypoint1 : Waypoint = self.waypoints[i1]
        waypoint2 : Waypoint = self.waypoints[i2]
        
        if(i1 in [0, len(self.waypoints) - 1] and not i2 in [0, len(self.waypoints) - 1]):
            if(not waypoint2.hasHeading):
                waypoint2.setHeading(waypoint1.heading())
            if(not waypoint1.hasHeading):
                waypoint1.setHasHeading(False)
        if(i2 in [0, len(self.waypoints) - 1] and not i1 in [0, len(self.waypoints) - 1]):
            if(not waypoint1.hasHeading):
                waypoint1.setHeading(waypoint2.heading())
            if(not waypoint2.hasHeading):
                waypoint2.setHasHeading(False)
        
            
        self.waypoints[i1], self.waypoints[i2] = self.waypoints[i2], self.waypoints[i1]
        self.pathDrawer.update()



    def addWaypointAtIndex(self,waypoint : Waypoint,index = -1):
        self.waypoints.insert(index, waypoint)
        poseLabel = self.sideBarItem.create_waypoint_label(waypoint)
        self.poseLabels[waypoint] = poseLabel
        self.sideBarItem.addPoseLabel(poseLabel)
        self.updateScene(self.scene())
        
    def addWaypoint(self,waypoint : Waypoint, isPose = False):
        newWaypointPos = waypoint.pos()
        if(waypoint.poseDisplay == None): waypoint.addDisplay(self.scene())
        if(isPose):
            if(self.waypoints[0].dist(newWaypointPos) > self.waypoints[-1].dist(newWaypointPos)):
                return self.addWaypointAtIndex(waypoint, 0)
            return self.addWaypointAtIndex(waypoint, -1)
        
        if(len(self.waypoints) <= 2): return self.addWaypointAtIndex(waypoint, 1)
        
        bestIndex = None
        bestDist = None

        for i in range(len(self.waypoints) - 1):
            index = i + 1
            testWaypoints = self.waypoints.copy()
            testWaypoints.insert(index, waypoint)
            bestHandle1Pos, bestHandle2Pos =  Tools.getHandlePos(
                waypoint.pos(),
                testWaypoints[index-1].pos(),
                testWaypoints[index+1].pos())
            waypoint.poseDisplay.handle.handle1.setCenterPos(bestHandle1Pos * 20)
            waypoint.poseDisplay.handle.handle2.setCenterPos(bestHandle2Pos *20)

            dist = PathDrawer.getLengthOfWaypoints(testWaypoints).length()
            print(dist)
            if(bestIndex == None):
                bestIndex = index
                bestDist = dist
                continue
            if(dist < bestDist):
                bestIndex = index
                bestDist = dist
        bestHandle1Pos, bestHandle2Pos =  Tools.getHandlePos(
            waypoint.pos(),
            testWaypoints[index-1].pos() + waypoint.pos(),
            testWaypoints[index+1].pos() + waypoint.pos())
        waypoint.poseDisplay.handle.handle1.setCenterPos( bestHandle1Pos * 20 )
        waypoint.poseDisplay.handle.handle2.setCenterPos( bestHandle2Pos * 20 )
        self.addWaypointAtIndex(waypoint, bestIndex)        


        
        
    def addToScene(self, scene : QGraphicsScene):
        for i in self.waypoints:
            i.addDisplay(scene)
        self.pathDrawer.setParentItem(scene.camera)
        self.pathDrawer.update()

    def addToSideBar(self, sideBar : SideBar):
        self.sideBarItem = PathLabel()
        sideBar.addPathLabel(self.sideBarItem)
        for waypoint in self.waypoints:
            poseLabel = sideBar.create_waypoint_label(waypoint)
            self.poseLabels[waypoint] = poseLabel
            self.sideBarItem.addPoseLabel(poseLabel)
    def distFromPoint(self, pos):
        dist = self.waypoints[0].dist(pos)
        for i in self.waypoints[0:]:
            if(i.dist(pos) > dist):
                dist = i.dist(pos)
        return dist
    def delete(self):
        for i in range(len(self.waypoints)):
            self.waypoints[i].parentPath = None
            self.waypoints[i].delete()
        self.sideBarItem.hide()
        self.pathDrawer.delete()

    def addToJson(self, json : dict, fieldMap : FieldMap):
        json["execution"].append(("Path", self.name))
        waypointJsonList = []
        for waypoint in self.waypoints:
            waypoint.addToJson(waypointJsonList, fieldMap)
        json[self.name] = waypointJsonList
    @staticmethod
    def fromJsonFile(pathList, fieldMap : FieldMap):
        waypoints = []
        for i in pathList:
            waypoints.append(Waypoint.fromJsonFile(i, fieldMap))
        return Path(waypoints)
    



