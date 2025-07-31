import matplotlib.pyplot as plt
import numpy as np
import random

# Parámetros
n = 100
p = 0.1
steps = 1000

# Inicialización
config = np.zeros((n, n))
for x in range(n):
    for y in range(n):
        config[x, y] = 1 if random.random() < p else 0
nextconfig = np.zeros((n, n))
density_list = []

# Función de actualización
def update(config):
    new_config = np.zeros_like(config)
    for x in range(n):
        for y in range(n):
            count = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    count += config[(x + dx) % n, (y + dy) % n]
            new_config[x, y] = 1 if count == 3 or (count == 2 and config[x, y] == 1) else 0
    return new_config

# Simulación
for t in range(steps):
    density = np.sum(config) / (n * n)
    density_list.append(density)
    config = update(config)

# Graficar densidad al final
plt.figure(figsize=(10, 4))
plt.plot(density_list, label='Density of 1\'s')
plt.xlabel('Time Step')
plt.ylabel('Density')
plt.title('Game of Life - Density Over Time')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
