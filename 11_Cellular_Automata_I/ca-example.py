import matplotlib
matplotlib.use('TkAgg')  # Use a non-interactive backend for script execution
from pylab import *
import random

n = 100
p = 0.1

def initialize():
    global config, nextconfig
    config = zeros([n, n])
    for x in range(n):
        for y in range(n):
            config[x, y] = 1 if random.random() < p else 0
    nextconfig = zeros([n, n])

def observe():
    global config
    cla()
    imshow(config, vmin=0, vmax=1, cmap='binary')

def update():
    global config, nextconfig
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue  # Evita contar la celda actual
                    count += config[(x + dx) % n, (y + dy) % n]
            nextconfig[x, y] = 1 if count == 3 or (count == 2 and config[x, y] == 1) else 0
    config, nextconfig = nextconfig, config

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])