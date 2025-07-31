import numpy as np
import matplotlib.pyplot as plt
from pylab import imshow, cla
from numpy import sin, pi
import pycxsimulator

# --- Parámetros iniciales ---
n = 100
c = 0.3
damping = 0.99
timestep = 0

# Parámetros dinámicos controlables por el usuario
f1 = 0.05
f2 = 0.05
phase1 = 0
phase2 = 0

# --- Setters de parámetros ---
def set_freq1(val=f1):
    global f1
    f1 = float(val)
    return val

def set_freq2(val=f2):
    global f2
    f2 = float(val)
    return val

def set_phase1(val=phase1):
    global phase1
    phase1 = float(val)
    return val

def set_phase2(val=phase2):
    global phase2
    phase2 = float(val)
    return val

# --- Simulación de onda ---
def initialize():
    global config, prev_config, next_config, timestep
    config = np.zeros((n, n), dtype=np.float32)
    prev_config = np.zeros((n, n), dtype=np.float32)
    next_config = np.zeros((n, n), dtype=np.float32)
    timestep = 0

def observe():
    cla()
    imshow(config, vmin=-1, vmax=1, cmap='seismic', interpolation='bilinear')

def laplacian_moore(grid, x, y):
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

    # Fuentes oscilantes con frecuencia y fase independientes
    A = 1.0
    wave1 = A * sin(2 * pi * f1 * timestep + phase1)
    wave2 = A * sin(2 * pi * f2 * timestep + phase2)

    r = 2  # radio fuente

    def apply_source(cx, cy, value):
        for dx in range(-r, r+1):
            for dy in range(-r, r+1):
                if dx**2 + dy**2 <= r**2:
                    x = (cx + dx) % n
                    y = (cy + dy) % n
                    next_config[x, y] = value

    apply_source(n//3, n//2, wave1)
    apply_source(2*n//3, n//2, wave2)

    prev_config, config, next_config = config, next_config, prev_config
    timestep += 1

# --- Ejecutar GUI ---
pycxsimulator.GUI(
    parameterSetters=[
        set_freq1,
        set_phase1,
        set_freq2,
        set_phase2
    ]
).start(func=[initialize, observe, update])
