from . import Waypoint

class InitialPose(Waypoint):
    def __init__(self, x=0, y=0, heading=0):
        super().__init__(None, x, y, heading)