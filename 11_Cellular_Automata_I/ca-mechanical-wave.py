import numpy as np
import matplotlib.pyplot as plt
from pylab import imshow, cla
from numpy import sin, pi

n = 100
c = 0.3
damping = 0.99  # amortiguación ligera
timestep = 0

def initialize():
    global config, prev_config, next_config, timestep
    config = np.zeros((n, n), dtype=np.float32)
    prev_config = np.zeros((n, n), dtype=np.float32)
    next_config = np.zeros((n, n), dtype=np.float32)
    timestep = 0

def observe():
    cla()
    # Visualizamos con una paleta continua entre -1 y 1
    imshow(config, vmin=-1, vmax=1, cmap='seismic', interpolation='bilinear')

def laplacian_moore(grid, x, y):
    # Vecindario de Moore (8 vecinos)
    total = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            total += grid[(x + dx) % n, (y + dy) % n]
    return total - 8 * grid[x, y]

def update():
    global config, prev_config, next_config, timestep

    for x in range(n):
        for y in range(n):
            lap = laplacian_moore(config, x, y)
            wave = (2 * config[x, y] - prev_config[x, y] + c**2 * lap) * damping
            next_config[x, y] = wave

    # Dos fuentes circulares que oscilan con el tiempo
    f = 0.05  # frecuencia
    A = 1.0   # amplitud
    wave_value = A * sin(2 * pi * f * timestep)

    r = 2  # radio de la fuente

    def apply_source(cx, cy):
        for dx in range(-r, r+1):
            for dy in range(-r, r+1):
                if dx**2 + dy**2 <= r**2:
                    x = (cx + dx) % n
                    y = (cy + dy) % n
                    next_config[x, y] = wave_value

    apply_source(n//3, n//2)
    apply_source(2*n//3, n//2)

    # Swap buffers
    prev_config, config, next_config = config, next_config, prev_config
    timestep += 1

import pycxsimulator
pycxsimulator.GUI().start(func=[initialize, observe, update])