import matplotlib
matplotlib.use('TkAgg')  # Use a non-interactive backend for script execution
from pylab import *
import random

n = 100
p = 0.1
pe = 0.2 # probability of a cell getting excited
recovery_time = 4 # number of time steps a cell remains excited

def set_n(val=n):
    global n
    n = int(val)
    return val

def set_p(val=p):
    global p
    p = float(val)
    return val

def set_pe(val=pe):
    global pe
    pe = float(val)
    return val

def set_recovery_time(val=recovery_time):
    global recovery_time
    recovery_time = int(val)
    return val

def initialize():
    global config, nextconfig
    config = zeros([n, n])
    for x in range(n):
        for y in range(n):
            if n//3 < x < 2*n//3 and n//3 < y < 2*n//3:
                config[x, y] = 1 if random.random() < 0.3 else 0
            else:
                config[x, y] = -1  # zona muerta (no excitables, puedes representar con -1)
    nextconfig = zeros([n, n])


def observe():
    global config
    cla()
    imshow(config, vmin=0, vmax=recovery_time, cmap='inferno')

def update():
    global config, nextconfig
    for x in range(n):
        for y in range(n):
            count = 0
            if config[x, y] == recovery_time:
                nextconfig[x, y] = 0
            elif config[x, y] > 0:
                nextconfig[x, y] += 1
            else:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue  # Evita contar la celda actual
                        if config[(x + dx) % n, (y + dy) % n] > 0:
                            count += 1
                if count * pe > random.random():
                    nextconfig[x, y] = 1            
                else: 
                    nextconfig[x, y] = 0
    config, nextconfig = nextconfig, config

import pycxsimulator
pycxsimulator.GUI(
    parameterSetters=[
        set_n, set_p, set_pe, set_recovery_time
    ]
).start(func=[initialize, observe, update])