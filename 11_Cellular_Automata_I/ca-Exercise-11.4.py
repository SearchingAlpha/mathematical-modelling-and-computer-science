"""
Exercise 11.3 
Modify Code 11.5 to implement a simulator of the Game of Life
CA. Simulate the dynamics from a random initial configuration. Measure the density
of state 1’s in the configuration at each time step, and plot how the density
changes over time. This can be done by creating an empty list in the initialize
function, and then making the measurement and appending the result to the list in
the observe function. The results stored in the list can be plotted manually after the
simulation, or they could be plotted next to the visualization using pylab’s subplot
function during the simulation.
"""

import matplotlib
matplotlib.use('TkAgg')  # Use a non-interactive backend for script execution
from pylab import *
import random

n = 100
p = 0.4
r = 3
avg = 0.5

def set_n(val=n):
    global n
    n = int(val)
    return val

def set_p(val=p):
    global p
    p = float(val)
    return val

def set_r(val=r):
    global r
    r = int(val)
    return val

def set_avg(val=avg):
    global avg
    avg = float(val)
    return val

def initialize():
    global config, nextconfig, density_list
    config = zeros([n, n])
    for x in range(n):
        for y in range(n):
            config[x, y] = 1 if random.random() < p else 0
    nextconfig = zeros([n, n])
    density_list = []  # List to store density of state 1's

def observe():
    global config, density_list
    cla()
    # Autómata celular
    subplot(1, 2, 1)
    imshow(config, vmin=0, vmax=1, cmap='binary')
    title("Game of Life")

    # Densidad
    subplot(1, 2, 2)
    density = np.sum(config) / (n * n)
    density_list.append(density)
    plot(density_list, label="Density")
    title("Density of State 1's")
    xlabel("Time Step")
    ylim(0, 1)
    grid(True)

def update():
    global config, nextconfig
    neighbor_count = (2 * r + 1) ** 2 - 1
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in range(-r, r+1):
                for dy in range(-r, r+1):
                    if dx == 0 and dy == 0:
                        continue  # Evita contar la celda actual
                    count += config[(x + dx) % n, (y + dy) % n]
        
            average = count / neighbor_count
            nextconfig[x, y] = 1 if average >= avg else 0
    config, nextconfig = nextconfig, config

import pycxsimulator
pycxsimulator.GUI(parameterSetters=[
        set_n,
        set_p,
        set_r,
        set_avg 
    ]
).start(func=[initialize, observe, update])

