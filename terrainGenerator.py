import noise
import numpy as np
import matplotlib.pyplot as plt

shape = (1024, 1024)
scale = 50.0
octaves = 6
persistence = 0.5
lacunarity = 2.0

blue = [65, 105, 225]
green = [34, 139, 34]
beach = [238, 214, 175]

world = np.zeros(shape)


def display_world(world):
    plt.figure(figsize=(10, 10))
    plt.imshow(world)


def add_color(world):
    color_world = np.array(world, np.int32)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < -0.05:
                color_world[i][j] = blue
            elif world[i][j] < 0:
                color_world[i][j] = beach
            elif world[i][j] < 1.0:
                color_world[i][j] = green

    return color_world


for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i / scale,
                                    j / scale,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=1024,
                                    repeaty=1024,
                                    base=0)

display_world(world)

colored_world = add_color(world)

display_world(colored_world)
