import cadquery as cq
from cadquery import exporters
import math


resc_parameters = [
    # size x, size y, pad x, pad y, pad center-center, grid x, grid y, terminal x, heights
    (10,  5, 0.90, 0.70, 1.30,  6, 2, (0.10, 0.30), [15, 35, 37, 40]),
    (16,  8, 1.10, 1.00, 1.70,  6, 4, (0.15, 0.40), [40]),
    (20, 12, 1.30, 1.50, 1.90,  8, 4, (0.15, 0.65), [40]),
    (32, 16, 1.60, 1.80, 2.80, 10, 4, (0.25, 0.75), [40]),
    (32, 25, 1.60, 2.70, 2.80, 10, 6, (0.25, 0.75), [40]),
    (50, 25, 1.80, 2.70, 4.40, 14, 6, (0.35, 0.85), [40]),
    (63, 32, 1.80, 3.20, 5.60, 16, 8, (0.35, 0.85), [40]),
]

(sx, sy, px, py, pcc, gx, gy, tx, heights) = resc_parameters[0]

sx = float(sx)/10
sy = float(sy)/10

tx = (tx[0] + tx[1]) / 2

h = heights[1]
h = float(h) / 100

th = h * 0.05

body = cq.Workplane("XZ").\
    moveTo(-sx/2 + th, th).\
    lineTo(-sx/2 + th, h - th).\
    lineTo(sx/2 - th, h - th).\
    lineTo(sx/2 - th, th).\
    close().\
    extrude(sy).\
    translate((0, sy/2, 0))

show_object(body)

top = cq.Workplane("XZ").\
    moveTo(-sx/2 + tx, h - th).\
    lineTo(-sx/2 + tx, h).\
    lineTo(sx/2 - tx, h).\
    lineTo(sx/2 - tx, h - th).\
    close().\
    extrude(sy).\
    translate((0, sy/2, 0))

show_object(top)

f = math.sqrt(2)/2 * th

def terminal():
    return cq.Workplane("XZ").\
        moveTo(-sx/2 + tx, 0).\
        lineTo(-sx/2 + th, 0).\
        threePointArc((-sx/2 + th - f, th - f), (-sx/2, th)).\
        lineTo(-sx/2, h - th).\
        threePointArc((-sx/2 + th - f, h - th + f), (-sx/2 + th, h)).\
        lineTo(-sx/2 + tx, h).\
        lineTo(-sx/2 + tx, h - th).\
        lineTo(-sx/2 + th, h - th).\
        lineTo(-sx/2 + th, th).\
        lineTo(-sx/2 + tx, th).\
        close().\
        extrude(sy).\
        translate((0, sy/2, 0))

end = terminal()
show_object(end)

start = terminal().\
    rotate((0, 0, -1), (0, 0, 1), 180)

show_object(start)

if False:
    with open("/tmp/wat.step", "w") as f:
        objects = [body, top, end, start]
    #    objects = cq.Workplane("XY").union([body, top, end, start])
        o = body.union(top)
        cq.exporters.exportShape(o, "STEP", f)
