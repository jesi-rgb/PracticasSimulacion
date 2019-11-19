import noise
import numpy as np
from PIL import Image
from Clases import CONEJO, LINCE, ZANAHORIA, ZANAHORIA_CONEJO


class Terrain:
    '''Terrain class with main methods such as a constructor and some helpers like display_world or add_color
    
    The class also has some parameters like colors or the seed to speed up the creating process. 

    DO NOT FORGET TO ADD SELF in front of any attribute we may want to refer to.
    '''
    white = np.array([255, 255, 255])
    orange = np.array([207, 147, 45])

    blue = np.array([65, 105, 225])
    green = np.array([34, 139, 34])
    beach = np.array([240, 233, 175])
    lightGreen = np.array([119, 204, 65])
    darkGreen = np.array([17, 74, 17])
    snow = np.array([250, 250, 250])
    mountain = np.array([139, 137, 137])

    seed = 234567546
    world = None
    manipulable_world = None
    original_world = None

    # functions
    def __init__(self, shape, scale, offX, offY, octaves, persistence,
                 lacunarity):
        self.world = self.normalize(
            self.generate_world(shape, scale, offX, offY, octaves, persistence,
                                lacunarity), 0, 255)
        self.manipulable_world = np.zeros(
            (self.world.shape[0], self.world.shape[1], 2), 'uint8')

    def normalize(self, oldWorld, newMin, newMax):
        '''Normalizes de input array between newMin and newMax.'''
        oldMax = oldWorld.max()
        oldMin = oldWorld.min()

        factor = (newMax - newMin) / (oldMax - oldMin)
        newWorld = (oldWorld - oldMin) * factor + newMin
        return newWorld

    def generate_world(self, shape, scale, offX, offY, octaves, persistence,
                       lacunarity):
        '''Generates a numpy array filled with noise values which are then normalized.'''
        world = np.zeros(shape)
        for i in range(shape[0]):
            for j in range(shape[1]):
                world[i][j] = noise.pnoise3(
                    i / scale + offX,  #22.65
                    j / scale + offY,  #89.55
                    self.seed,
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=1024,
                    repeaty=1024,
                    base=0)

        return world

    def display_world(self):
        '''Reproduce the resulting world as an image.'''
        Image.fromarray(self.world).show()

    def add_color(self):
        '''Adds color to the input array based on interval values.
        >< 60 = blue \n
        >\>= 60 & < 70 = beach \n
        >\>= 70 & < 100 = lightGreen \n
        >\>= 100 & < 150 = green \n
        >\>= 150 & < 190 = darkGreen \n
        >\>= 190 & < 240 = mountain \n
        >\> 240 = snow
        '''

        color_world = np.zeros((self.world.shape[0], self.world.shape[1], 3),
                               'uint8')

        blueCondition = self.world < 60
        beachCondition = (self.world >= 60) & (self.world < 70)
        lightGreenCondition = (self.world >= 70) & (self.world < 100)
        greenCondition = (self.world >= 100) & (self.world < 150)
        darkGreenCondition = (self.world >= 150) & (self.world < 190)
        mountainCondition = (self.world >= 190) & (self.world < 240)
        snowCondition = self.world > 240

        color_world[blueCondition] = self.blue
        color_world[beachCondition] = self.beach
        color_world[lightGreenCondition] = self.lightGreen
        color_world[greenCondition] = self.green
        color_world[darkGreenCondition] = self.darkGreen
        color_world[mountainCondition] = self.mountain
        color_world[snowCondition] = self.snow

        self.manipulable_world[blueCondition] = [0, 0]
        self.manipulable_world[beachCondition] = [1, 0]
        self.manipulable_world[lightGreenCondition] = [2, 0]
        self.manipulable_world[greenCondition] = [3, 0]
        self.manipulable_world[darkGreenCondition] = [4, 0]
        self.manipulable_world[mountainCondition] = [5, 0]
        self.manipulable_world[snowCondition] = [6, 0]

        self.world = color_world
        # np.save("world", self.world)
        # np.save("manipulable_world", self.manipulable_world)
        # self.original_world = np.copy(self.manipulable_world)

    def recalculate_world(self):
        '''Función para recalcular el mundo en base a la posición nueva que toman los animales'''
        bunnyCondition = self.manipulable_world[:, :, 1] == CONEJO
        carrotCondition = self.manipulable_world[:, :, 1] == ZANAHORIA
        eatingCondition = self.manipulable_world[:, :, 1] == ZANAHORIA_CONEJO
        lynxCondition = self.manipulable_world[:, :, 1] == LINCE

        self.world[bunnyCondition] = self.white
        self.world[carrotCondition] = self.orange
        self.world[eatingCondition] = [255, 80, 80]
        self.world[lynxCondition] = [0,0,0]

    def reset_worlds(self):
        '''Función para resetear ambos mundos y prepararlos para el siguiente tick'''
        # self.manipulable_world = np.copy(self.original_world)

        blueCondition = self.manipulable_world[:, :, 0] == 0
        beachCondition = self.manipulable_world[:, :, 0] == 1
        lightGreenCondition = self.manipulable_world[:, :, 0] == 2
        greenCondition = self.manipulable_world[:, :, 0] == 3
        darkGreenCondition = self.manipulable_world[:, :, 0] == 4
        mountainCondition = self.manipulable_world[:, :, 0] == 5
        snowCondition = self.manipulable_world[:, :, 0] == 6

        self.world[blueCondition] = self.blue
        self.world[beachCondition] = self.beach
        self.world[lightGreenCondition] = self.lightGreen
        self.world[greenCondition] = self.green
        self.world[darkGreenCondition] = self.darkGreen
        self.world[mountainCondition] = self.mountain
        self.world[snowCondition] = self.snow


if __name__ == "__main__":
    # shape = (1024, 1024)
    # scale = 500.0
    # octaves = 6
    # persistence = 0.45
    # lacunarity = 2
    terrain = Terrain((800, 800), 500.0, 6, 0.45, 2)
    terrain.add_color()
    np.save("Terrain", terrain.world)
    np.save("Manipulable_terrain", terrain.manipulable_world)
    print(terrain.manipulable_world.shape)
    terrain.display_world()
