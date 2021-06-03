import openpyscad as ops
from tqdm import tqdm

from util import frange

from math import sqrt, pi, exp, sin, cos, log as ln
from inspect import getsource
from os import getenv

FN_TOP = 'sqrt'
FN_BOT = 'xaxis'
FN_CROSS = 'rect'

OUTPUT_PATH = f"{getenv('HOME')}/Desktop/output.scad"
SLICE_WIDTH = 1e-1
LEFT_BOUND = 0
RIGHT_BOUND = 9

base_functions = {
        'semicircle':   lambda x: sqrt(4-(x-2)**2),
        'horizontal':   lambda x: 9,
        'parabola':     lambda x: x**2,
        'cubic':        lambda x: 0.25 * (x-1)**3 - (x-1)**2 + 3,
        'xaxis':        lambda x: 0,
        'sqrt':         lambda x: sqrt(x),
        'nsin':         lambda x: -sin(x+1)+1,
        'sin':          lambda x: sin(x+1)+1,
        'cos':          lambda x: cos(x+1)+1,
        'exp':          lambda x: exp(x-2),
        'custom':       []
        }

cross_section = {
        'slab':         lambda w: ops.Cube([SLICE_WIDTH, w, 1]),
        'rect':         lambda w: ops.Cube([SLICE_WIDTH, w, w/2]),
        'square':       lambda w: ops.Cube([SLICE_WIDTH, w, w]),
        'isoceles':     lambda w: isoceles_prism(SLICE_WIDTH, w, w**2/4),
        'semicircle':   lambda w: (ops.Cylinder(SLICE_WIDTH, w/2, _fn=30).rotate([0, 90, 0]).translate([0, w/2, 0])) & ops.Cube([SLICE_WIDTH, w, w]),
        'equalateral':  lambda w: isoceles_prism(SLICE_WIDTH, w, w),
        }

vol_fns = {
        'slab':         lambda w: w,
        'rect':         lambda w: w**2/2,
        'square':       lambda w: w**2,
        'isoceles':     lambda w: w**3/8,
        'semicircle':   lambda w: pi*w**2/8,
        'equalateral':  lambda w: sqrt(3)/4 * w**2,
        }

def isoceles_prism(w, l, h):
    return ops.Polyhedron(
        points = [[0, 0, 0], [0, l, 0], [w, 0, 0], [w, l, 0], [0, l/2, h], [w, l/2, h]],
        faces  = [[0, 1, 3, 2], [0, 1, 4], [2, 3, 5], [1, 3, 5, 4], [0, 2, 5, 4]]
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
    vol = 0
    for x in tqdm(frange(LEFT_BOUND, RIGHT_BOUND, SLICE_WIDTH), total=(RIGHT_BOUND-LEFT_BOUND)/SLICE_WIDTH):
        try:
            width = base_functions[top_fn](x)-base_functions[bot_fn](x)
            obj = cross_section[cross_fn](abs(width))
            if width < 0: obj = obj.rotate([180, 0, 0])
            ret += obj.translate([x, base_functions[bot_fn](x)])
            vol += vol_fns[cross_fn](abs(width))*SLICE_WIDTH
        except ValueError:
            pass

    print(f'total volume: {vol}')

    return ret

def get_opt_stdin(name, opts):
    while True:
        print(f'What should the {name} be?')
        for v in opts.values():
            if type(v) == list: break
            print(getsource(v), end='')
        if 'custom' in opts:
            print("or type 'custom' to imput your own function")
        g = input()
        if len(g) == 0: return None
        if g == 'custom':
            opts['custom'].append(eval('lambda x: ' + input("Enter function here: ").replace('^', '**')))
            return 'custom'
        if g in opts.keys():
            return g
        else: print(f'invalid {name}!')

if __name__ == '__main__':
    while True:
        FN_TOP   = get_opt_stdin('top function', base_functions) or FN_TOP
        FN_BOT   = get_opt_stdin('bottom function', base_functions) or FN_BOT
        FN_CROSS = get_opt_stdin('cross section function', cross_section) or FN_CROSS

        # spaghetti ahead, please avert your eyes
        if FN_TOP == 'custom':
            FN_TOP = 'custom1'
            base_functions['custom1'] = base_functions['custom'].pop(0)
        if FN_BOT == 'custom':
            FN_BOT = 'custom2'
            base_functions['custom2'] = base_functions['custom'].pop(0)

        gen_crosssectional_solid(FN_TOP, FN_BOT, FN_CROSS).write(OUTPUT_PATH)

        print(f'finished! Open {OUTPUT_PATH} in OpenSCAD to see the result')

        input('press enter to begin a new solid')
    # (gen_crosssectional_solid('sqrt', 'semicircle', 'semicircle')-gen_crosssectional_solid('sqrt', 'semicircle', 'equalateral')).write(OUTPUT_PATH) # broken

