from math import cos, pi, sqrt
from matplotlib import pyplot

# end = 4.21
end = 4
step = 1e-3
config = [
        # [ 0.24,   lambda x: 2    *(x-0.6697)**2 + 0.23 ],
        # [ 0.8287, lambda x: 0.997*(x-1.513 )**3 + 0.6  ],
        # [ 2.116 , lambda x: -2.42*cos(x+0.67)   - 1.45 ],
        # [ 3.065 , lambda x: sqrt((x-4.21)/(-3.7)) ],
        [ 0, lambda x: sqrt(4 - (x-2)**2)],
        [ end , None ]
    ]
calculation = {
        'volume':       lambda f, x: pi * f(x)**2,
        'surfacearea':  lambda f, x: 2 * pi * f(x) * sqrt(1+(f(x+step) - f(x))**2)
        }

def frange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step

if __name__ == '__main__':
    tot = 0

    plotx = []
    ploty = []

    # step = (end - config[0][0]) / num
    for i, (start, func) in enumerate(config):
        if i + 1 == len(config): break
        for x in frange(start, config[i+1][0]-step, step):
            # print(x, func(x))
            plotx.append(x)
            ploty.append(func(x))

            tot += calculation['surfacearea'](func, x)

    pyplot.scatter(plotx, ploty)
    pyplot.show()

    print(tot)

