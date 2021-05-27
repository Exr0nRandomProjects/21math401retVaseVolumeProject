import openpyscad as ops

from util import frange

from math import sqrt, pi
from os import getenv

OUTPUT_PATH = f"{getenv('HOME')}/projects/Taproot/21math401/KBe21math401retCrossSections.scad"
SLICE_WIDTH = 4e-2
LEFT_BOUND = 0
RIGHT_BOUND = 4

base_functions = {
        'semicircle':   lambda x: sqrt(4-(x-2)**2),
        'cubic':        lambda x: 0.25 * (x-1)**3 - (x-1)**2 + 3,
        'xaxis':        lambda x: 0
        }
top_fn = 'cubic'
bot_fn = 'semicircle'

cross_section = {
        'slab':         lambda w: ops.Cube([SLICE_WIDTH, w, 1]),
        'square':       lambda w: ops.Cube([SLICE_WIDTH, w, w])
        }
cross_fn = 'square'

def scadsum(*args):
    if type(args[0]) == list:
        args = args[0]
    if args is None or len(args) == 0:
        return ops.Cube(0)
    if len(args) == 1:
        return args[0]
    ret = args[0]
    for obj in args[1:]:
        ret += obj
    return ret

if __name__ == '__main__':
    # out = scadsum(ops.Cube([10, 20, 30]), ops.Cube([1, 2, 3]))
    out = scadsum([
        cross_section[cross_fn](
                abs(base_functions[top_fn](x)-base_functions[bot_fn](x))
            ).translate([x, base_functions[bot_fn](x), 0])
        for x in frange(LEFT_BOUND, RIGHT_BOUND, SLICE_WIDTH)])
    print(out)
    out.write(OUTPUT_PATH)

