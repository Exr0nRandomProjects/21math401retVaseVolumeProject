import openpyscad as ops
from tqdm import tqdm

from util import frange

from math import sqrt, pi, exp, sin, cos
from os import getenv

FN_TOP = 'sin'
FN_BOT = 'nsin'
FN_CROSS = 'semicircle'

OUTPUT_PATH = f"{getenv('HOME')}/projects/Taproot/21math401/KBe21math401retCrossSections.scad"
SLICE_WIDTH = 2e-2
LEFT_BOUND = 0
RIGHT_BOUND = 10

base_functions = {
        'semicircle':   lambda x: sqrt(4-(x-2)**2),
        'parabola':     lambda w: (x-2)**2,
        'cubic':        lambda x: 0.25 * (x-1)**3 - (x-1)**2 + 3,
        'xaxis':        lambda x: 0,
        'sqrt':         lambda x: sqrt(x),
        'nsin':         lambda x: -sin(x+1)+1,
        'sin':          lambda x: sin(x+1)+1,
        'cos':          lambda x: cos(x+1)+1,
        'exp':          lambda x: exp(x-2),
        }

cross_section = {
        'slab':         lambda w: ops.Cube([SLICE_WIDTH, w, 1]),
        'rect':         lambda w: ops.Cube([SLICE_WIDTH, w, w/2]),
        'square':       lambda w: ops.Cube([SLICE_WIDTH, w, w]),
        'isoceles':     lambda w: isoceles_prism(SLICE_WIDTH, w, w**2/4),
        'semicircle':   lambda w: (ops.Cylinder(SLICE_WIDTH, w/2, _fn=30).rotate([0, 90, 0]).translate([0, w/2, 0])) & ops.Cube([SLICE_WIDTH, w, w]),
        'equalateral':  lambda w: isoceles_prism(SLICE_WIDTH, w, w),
        }

def isoceles_prism(w, l, h):
    return ops.Polyhedron(
        points = [[0, 0, 0], [0, l, 0], [w, 0, 0], [w, l, 0], [0, l/2, h], [w, l/2, h]],
        faces  = [[0, 1, 2, 3], [0, 1, 4], [2, 3, 5], [1, 2, 5, 4], [0, 3, 5, 4]]
    )

def scadsum(*args):
    if args is None or len(args) == 0:
        return ops.Cube(0)
    if type(args[0]) == list:
        args = args[0]
    if len(args) == 1:
        return args[0]
    ret = args[0]
    for obj in args[1:]:
        ret += obj
    return ret

def gen_crosssectional_solid(top_fn, bot_fn, cross_fn):
    ret = scadsum()
    for x in tqdm(frange(LEFT_BOUND, RIGHT_BOUND, SLICE_WIDTH), total=(RIGHT_BOUND-LEFT_BOUND)/SLICE_WIDTH):
        try:
            width = base_functions[top_fn](x)-base_functions[bot_fn](x)
            temp = cross_section[cross_fn](abs(width))
            if width < 0: temp = temp.rotate([180, 0, 0])
            ret += temp.translate([x, base_functions[bot_fn](x)])
        except ValueError:
            pass
    return ret

if __name__ == '__main__':
    gen_crosssectional_solid(FN_TOP, FN_BOT, FN_CROSS).write(OUTPUT_PATH)
    # (gen_crosssectional_solid('sqrt', 'semicircle', 'semicircle')-gen_crosssectional_solid('sqrt', 'semicircle', 'equalateral')).write(OUTPUT_PATH) # broken

