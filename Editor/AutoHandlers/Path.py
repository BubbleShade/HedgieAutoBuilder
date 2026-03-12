from .. import PointDisplay, PathSidebarItem, SideBar, PathDrawer
from . import Waypoint
import Styles
import Tools
from PyQt6.QtWidgets import QGraphicsScene

from .. import FieldMap
def handlePoseComposer(pose : PointDisplay, handle):
    return lambda _ =  None: handle.centerPos() + pose.center()


class Path():
    def __init__(self, *waypoints : Waypoint):
 
        self.waypoints : list[Waypoint] = list(waypoints)

        if(self.waypoints == []):
            self.waypoints.append(Waypoint(self, rotation=0))
        self.waypoints[-1].setHeading(0)

        for i in waypoints:
            i.setParent(self)
        self.sideBarItem = None
        self.curves = []
        self.poseLabels = {}
        self.parentAuto = None
        self.name = "Path1"

        self.sideBarItem = PathSidebarItem(self)
        for i in self.waypoints:
            #self.poseLabels[i] = i.sideBarItem
            self.sideBarItem.addPoseLabel(i.sideBarItem)

    
    def getDrawerWaypoints(self):
        return self.parentAuto
    
    def addPathBelow(self):
        if(self.parentAuto != None):
            self.parentAuto.addPathBelow(self)
    def addNamedCommandBelow(self):
        if(self.parentAuto != None):
            self.parentAuto.addNamedCommandBelow(self)
        

    def scene(self):
        if(self.parentAuto != None): return self.parentAuto.scene
        else: return None

    def updateScene(self,scene : QGraphicsScene = None):
        self.parentAuto.updateScene(scene)
        if(scene == None): return

    def remove(self, waypoint : Waypoint):
        self.sideBarItem.poseLayout.remove_item(waypoint.sideBarItem)
        self.waypoints.remove(waypoint)

        # if(self.poseLabels[waypoint] != None):
        #     self.poseLabels[waypoint].delete()
    def addWaypointAtLocation(self, waypoint : Waypoint, addToIndex = 0):
        index= self.waypoints.index(waypoint) + addToIndex
        newWaypoint = Waypoint(self, waypoint.x() + 100, waypoint.y())
        self.waypoints.insert(index, newWaypoint)
        newWaypoint.addDisplay(self.scene())
        self.sideBarItem.addPoseLabel(newWaypoint.sideBarItem, index)
        self.updateScene()
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
        self.parentAuto.updateScene()



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

    def addToStaticScene(self, scene : QGraphicsScene):
        for i in self.waypoints:
            i.addDisplay(scene, True)

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
        if(self.sideBarItem != None):
            self.sideBarItem.hide()
            self.sideBarItem.deleteLater()
        if(self.parentAuto != None):
            self.parentAuto.execution.remove(self)
            self.parentAuto.updateScene()

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
        return Path(*waypoints)
    



