import matplotlib
matplotlib.use('TkAgg')
from pylab import *
import numpy as np
import random
import pycxsimulator

n = 100
p = 0.2      # more sparse initial condition
Ra = 2
Ri = 5
wa = 1.2
wi = 1.0

def set_n(val=n):
    global n
    n = int(val)
    return val

def set_p(val=p):
    global p
    p = float(val)
    return val

def set_Ra(val=Ra):
    global Ra
    Ra = int(val)
    return val

def set_Ri(val=Ri):
    global Ri
    Ri = int(val)
    return val

def set_wa(val=wa):
    global wa
    wa = float(val)
    return val

def set_wi(val=wi):
    global wi
    wi = float(val)
    return val

def get_neighborhood(radius):
    neighborhood = []
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            if dx**2 + dy**2 <= radius**2 and not (dx == 0 and dy == 0):
                neighborhood.append((dx, dy))
    return neighborhood

def initialize():
    global config, nextconfig
    config = np.random.rand(n, n) < p
    config = config.astype(int)
    nextconfig = np.zeros((n, n))

def observe():
    global config
    cla()
    imshow(config, vmin=0, vmax=1, cmap='Greys')
    
def update():
    global config, nextconfig
    Na = get_neighborhood(Ra)
    Ni = get_neighborhood(Ri)
    for x in range(n):
        for y in range(n):
            sum_a = 0
            sum_i = 0
            for dx, dy in Na:
                sum_a += config[(x + dx) % n, (y + dy) % n]
            for dx, dy in Ni:
                sum_i += config[(x + dx) % n, (y + dy) % n]
            a = wa * sum_a - wi * sum_i
            nextconfig[x, y] = 1 if a > 0 else 0
    config[:, :] = nextconfig

pycxsimulator.GUI(
    parameterSetters=[
        set_n, set_p, set_Ra, set_Ri, set_wa, set_wi
    ]
).start(func=[initialize, observe, update])
