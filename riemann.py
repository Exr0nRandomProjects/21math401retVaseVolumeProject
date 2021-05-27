from tqdm import tqdm

from math import cos, pi, sqrt
from matplotlib import pyplot

end = 4.21
step = 1e-6
config = [
        [ 0.24,   lambda x: 2    *(x-0.6697)**2 + 0.23 ],
        [ 0.8287, lambda x: 0.997*(x-1.513 )**3 + 0.6  ],
        [ 2.116 , lambda x: -2.42*cos(x+0.67)   - 1.45 ],
        [ 3.065 , lambda x: sqrt((x-4.21)/(-3.7)) ],
        [ end , None ]
    ]
calculation = {
        'volume':       lambda f, x: pi * f(x)**2,
        'surfacearea':  lambda f, x: 2 * pi * f(x) * sqrt(1+((f(x+step) - f(x))/step)**2)
        }

def frange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step

def calc(calc_type):
    tot = 0

    plotx = []
    ploty = []

    # step = (end - config[0][0]) / num
    with tqdm(total=int((end-config[0][0])/step)) as pbar:
        for i, (start, func) in enumerate(config):
            if i + 1 == len(config): break
            for x in frange(start, config[i+1][0]-step, step):
                # print(x, func(x))
                # plotx.append(x)
                # ploty.append(func(x))

                try:
                    tot += calculation[calc_type](func, x) * step
                except ValueError:
                    print("domain error! skipping slice...", x)
                finally:
                    pbar.update(1)

    # pyplot.scatter(plotx, ploty)
    # pyplot.show()

    # print(tot)
    return tot

if __name__ == '__main__':
    print('surface area', calc('surfacearea'))
    print('volume', calc('volume'))

