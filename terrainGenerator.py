import noise
import numpy as np
from PIL import Image

shape = (1024, 1024)
scale = 500.0
octaves = 6
persistence = 0.45
lacunarity = 2

blue = [65, 105, 225]
green = [34, 139, 34]
beach = [240, 233, 175]
lightGreen = [119, 204, 65]
darkGreen = [17, 74, 17]
snow = [255, 250, 250]
mountain = [139, 137, 137]

world = np.zeros(shape)

seed = 234567546


# functions
def display_world(world):
    '''Reproduce the resulting world as an image'''
    Image.fromarray(world).show()


def add_color(world):
    color_world = np.zeros((shape[0], shape[1], 3), 'uint8')

    color_world[world < 60] = blue
    color_world[(world >= 60) & (world < 70)] = beach
    color_world[(world >= 70) & (world < 100)] = lightGreen
    color_world[(world >= 100) & (world < 150)] = green
    color_world[(world >= 150) & (world < 190)] = darkGreen
    color_world[(world >= 190) & (world < 240)] = mountain
    color_world[world > 240] = snow

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
            world[i][j] = noise.pnoise2(i / scale + 50,
                                        j / scale + 50,
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
    # display_world(world)
    colored_world = add_color(world)
    display_world(colored_world)
