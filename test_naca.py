import cadquery as cq
import math

def get_pts(chord, offset=0):
    m = 0.02; p = 0.4; t = 0.12
    n_pts = 40
    pts = []
    upper = []
    lower = []
    for i in range(n_pts + 1):
        b = math.pi * i / n_pts
        xn = 0.5 * (1 - math.cos(b))
        yt = 5 * t * (0.2969 * math.sqrt(xn) - 0.1260 * xn - 0.3516 * xn**2 + 0.2843 * xn**3 - 0.1036 * xn**4)
        # Offset thickness
        yt_eff = max(0, yt - offset/chord) # Very simple vertical offset
        
        # yc logic... (simplified for test)
        yc = 0
        xu, yu = (xn * chord), (yc + yt_eff) * chord
        xl, yl = (xn * chord), (yc - yt_eff) * chord
        if i == 0: upper.append((0.0, 0.0))
        else:
            upper.append((xu, yu))
            lower.insert(0, (xl, yl))
    return lower + upper[:-1]

pts_outer = get_pts(200, 0)
pts_inner = get_pts(200, 1.5)
w_outer = cq.Workplane("XY").spline(pts_outer).close().objects[0]
w_inner = cq.Workplane("XY").spline(pts_inner).close().objects[0]
solid = cq.Solid.makeLoft([w_outer, w_inner], ruled=False)
print("Loft Success")
