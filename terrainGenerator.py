import noise
import numpy as np
from PIL import Image


class Terrain:
    blue = [65, 105, 225]
    green = [34, 139, 34]
    beach = [240, 233, 175]
    lightGreen = [119, 204, 65]
    darkGreen = [17, 74, 17]
    snow = [255, 250, 250]
    mountain = [139, 137, 137]
    seed = 234567546
    world = None

    # functions
    def __init__(self, shape, scale, octaves, persistence, lacunarity):
        world = self.generateWorld(shape, scale, octaves, persistence,
                                   lacunarity)

    def normalize(self, oldWorld, newMin, newMax):
        '''Normalizes de input array between newMin and newMax.'''
        oldMax = oldWorld.max()
        oldMin = oldWorld.min()

        factor = (newMax - newMin) / (oldMax - oldMin)
        newWorld = (oldWorld - oldMin) * factor + newMin
        return newWorld

    def generateWorld(self, shape, scale, octaves, persistence, lacunarity):
        '''Generates a numpy array filled with noise values which are then normalized.'''
        world = np.zeros(shape)
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

        return self.normalize(world, 0, 255)

    def display_world(world):
        '''Reproduce the resulting world as an image.'''
        Image.fromarray(world).show()

    def add_color(world):
        '''Adds color to the input array based on interval values.
        >< 60 = blue \n
        >\>= 60 & < 70 = beach \n
        >\>= 70 & < 100 = lightGreen \n
        >\>= 100 & < 150 = green \n
        >\>= 150 & < 190 = darkGreen \n
        >\>= 190 & < 240 = mountain \n
        >\> 240 = snow
        '''
        color_world = np.zeros((shape[0], shape[1], 3), 'uint8')

        color_world[world < 60] = blue
        color_world[(world >= 60) & (world < 70)] = beach
        color_world[(world >= 70) & (world < 100)] = lightGreen
        color_world[(world >= 100) & (world < 150)] = green
        color_world[(world >= 150) & (world < 190)] = darkGreen
        color_world[(world >= 190) & (world < 240)] = mountain
        color_world[world > 240] = snow

        return color_world


if __name__ == "__main__":
    # shape = (1024, 1024)
    # scale = 500.0
    # octaves = 6
    # persistence = 0.45
    # lacunarity = 2
    terrain = Terrain(shape=(800, 800),
                      scale=500.0,
                      octaves=6,
                      persistence=0.45,
                      lacunarity=2)
    Terrain.display_world(terrain.world)
