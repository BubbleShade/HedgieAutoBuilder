__all__ = ["Arrow", "Line", "BezierCurve"]
__name__ = "Tools"

from Tools.arrow import Arrow, ArrowDrawer
from Tools.line import Line
from Tools.bezierCurve import BezierCurve

def clamp(value, min_value, max_value):
    return min(max(value, min_value), max_value)