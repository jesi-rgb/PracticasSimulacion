import noise
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import sklearn

shape = (1024, 1024)
scale = 100.0
octaves = 6
persistence = 0.5
lacunarity = 1.37

blue = [65, 105, 225]
green = [34, 139, 34]
beach = [238, 214, 175]

world = np.zeros(shape)


# functions
def display_world(world):
    '''Reproduce the resulting world as an image'''
    Image.fromarray(world).show()


def add_color(world):
    color_world = np.zeros((shape[0], shape[1], 3), 'uint8')
    for i in range(shape[0]):
        for j in range(shape[1]):
            if world[i][j] < 100:
                color_world[i][j] = blue
            elif world[i][j] < 120:
                color_world[i][j] = beach
            elif world[i][j] < 255:
                color_world[i][j] = green

    return color_world


def normalize(oldWorld, newMin, newMax):
    oldMax = oldWorld.max()
    oldMin = oldWorld.min()

    factor = (newMax - newMin) / (oldMax - oldMin)
    newWorld = (oldWorld - oldMin) * factor + newMin
    return newWorld


def generateWorld(shape, world, scale, octaves, persistence, lacunarity):
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

    return normalize(world, 0, 255)


if __name__ == "__main__":
    world = generateWorld(shape, world, scale, octaves, persistence,
                          lacunarity)
    display_world(world)
    colored_world = add_color(world)
    display_world(colored_world)
