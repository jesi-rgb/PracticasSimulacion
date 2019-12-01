import noise
import numpy as np
from PIL import Image
from Clases import CONEJO, LINCE, ZANAHORIA, ZANAHORIA_CONEJO
from Funciones import HEIGTH, W_FACTOR, WIDTH, H_FACTOR


class Terrain:
    '''Terrain class with main methods such as a constructor and some helpers like display_world or add_color
    
    The class also has some parameters like colors or the seed to speed up the creating process. 

    DO NOT FORGET TO ADD SELF in front of any attribute we may want to refer to.
    '''
    white = np.array([255, 255, 255, 255])
    black = np.array([0, 0, 0, 255])
    fruitColor = np.array([255, 66, 80, 255])

    darkSand = np.array([214, 170, 75, 255])
    green = np.array([34, 139, 34, 255])
    sand = np.array([240, 233, 175, 255])
    lightGreen = np.array([119, 204, 65, 255])
    darkGreen = np.array([17, 74, 17, 255])
    snow = np.array([220, 220, 220, 255])
    mountain = np.array([139, 137, 137, 255])

    seed = 234567546
    world = None
    manipulable_world = None

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

        color_world = np.zeros((self.world.shape[0], self.world.shape[1], 4),
                               'uint8')

        darkSandCondition = self.world < 40
        sandCondition = (self.world >= 40) & (self.world < 70)
        lightGreenCondition = (self.world >= 70) & (self.world < 100)
        greenCondition = (self.world >= 100) & (self.world < 150)
        darkGreenCondition = (self.world >= 150) & (self.world < 190)
        mountainCondition = (self.world >= 190) & (self.world < 240)
        snowCondition = self.world > 240

        color_world[darkSandCondition] = self.darkSand
        color_world[sandCondition] = self.sand
        color_world[lightGreenCondition] = self.lightGreen
        color_world[greenCondition] = self.green
        color_world[darkGreenCondition] = self.darkGreen
        color_world[mountainCondition] = self.mountain
        color_world[snowCondition] = self.snow

        self.manipulable_world[darkSandCondition] = [0, 0]
        self.manipulable_world[sandCondition] = [1, 0]
        self.manipulable_world[lightGreenCondition] = [2, 0]
        self.manipulable_world[greenCondition] = [3, 0]
        self.manipulable_world[darkGreenCondition] = [4, 0]
        self.manipulable_world[mountainCondition] = [5, 0]
        self.manipulable_world[snowCondition] = [6, 0]

        self.world = color_world

    def recalculate_world(self):
        '''Función para recalcular el mundo en base a la posición nueva que toman los animales'''
        bunnyCondition = self.manipulable_world[:, :, 1] == CONEJO
        carrotCondition = self.manipulable_world[:, :, 1] == ZANAHORIA
        eatingCondition = self.manipulable_world[:, :, 1] == ZANAHORIA_CONEJO
        lynxCondition = self.manipulable_world[:, :, 1] == LINCE

        self.world[bunnyCondition] = self.white
        self.world[carrotCondition] = self.fruitColor
        self.world[eatingCondition] = [255, 80, 80, 255]
        self.world[lynxCondition] = self.black

    def reset_worlds(self):
        '''Función para resetear ambos mundos y prepararlos para el siguiente tick'''

        blueCondition = self.manipulable_world[:, :, 0] == 0
        beachCondition = self.manipulable_world[:, :, 0] == 1
        lightGreenCondition = self.manipulable_world[:, :, 0] == 2
        greenCondition = self.manipulable_world[:, :, 0] == 3
        darkGreenCondition = self.manipulable_world[:, :, 0] == 4
        mountainCondition = self.manipulable_world[:, :, 0] == 5
        snowCondition = self.manipulable_world[:, :, 0] == 6

        self.world[blueCondition] = self.darkSand
        self.world[beachCondition] = self.sand
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
    terrain = Terrain((WIDTH // W_FACTOR, HEIGTH // H_FACTOR), 100.0, 22.55,
                      89.55, 6, 0.45, 2)
    terrain.add_color()

    img = Image.fromarray(terrain.world)
    img = img.resize((800, 800))
    img.save('mapa definitivo.png')
    terrain.display_world()
