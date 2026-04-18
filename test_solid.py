import cadquery as cq
import math
def get_pts(c):
    return [(c,0), (0,c*0.1), (0,-c*0.1)] # Simplified triangle
root = cq.Workplane("XY").polyline(get_pts(200)).close().toPending().objects[0]
tip = cq.Workplane("XY").workplane(offset=100).polyline(get_pts(140)).close().toPending().objects[0]
solid = cq.Solid.makeLoft([root, tip], ruled=False)
print(f"Shape type: {type(solid)}")
try:
    print(f"Is solid: {solid.isValid()}")
except:
    print("isValid not available")
