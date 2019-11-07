HUNGER_LOSS = 0.01
HUNGER_FEELING_LIMIT = 0.5
REPRODUCTIONH_FEELING_LIMIT = 0.5
ATTACK_LIMIT = 0.1
MIN_SPEED = 5
MAX_SPEED = 20
EAT_DELAY = 3  #ticks
HUNGER_QUENCH = 0.3
MOVES_PER_ACTION = 2
EXTRA_STEP = 1
numero_random_que_borraremos = 2

#CASILLAS
NADA = 0
CONEJO = 1
ZANAHORIA_CONEJO = 2
ZANAHORIA = 3
CONEJO_REPRODUCCION = 4
CONEJO_CONEJO = 5
PELEA_CONEJO = 6
LINCE = 7
PELEA_LINCE = 8
ZANAHORIA_LINCE = 9
CONEJO_LINCE = 10
LINCE_LINCE = 11

import Funciones
from PIL import Image
import numpy as np
import random


class Animal:
    def __init__(self):

        #Survival attributes
        self.hunger = 0
        self.strength_speed = 0
        self.reproductive_need = 0
        self.vision_field = 0
        self.risk_aversion = 0
        self.racionality = 0

        #Life attributes
        self.max_time_alive = 100
        self.time_alive = 0

        #Map position
        self.x = int(10)
        self.y = int(10)

        self.lastX = self.x
        self.lastY = self.y

        self.wants_fight = False
        self.wants_reproduction = False

    def action(self, terrain):
        self.hunger += HUNGER_LOSS
        if self.hunger == 1:
            pass  #Die

    def move(self, diffX, diffY):
        if not (diffX == 0 or diffY == 0):
            self.x += int(diffX / abs(diffX))
            self.y += int(diffY / abs(diffY))
        else:
            self.x += 0
            self.y += 0


class Rabbit(Animal):
    def __init__(self):
        Animal.__init__(self)

    def display(self, terrain):
        '''Función para editar el valor x, y del mundo donde nos situamos ahora mismo'''
        # oldValue = terrain[self.x][self.y]
        # terrain[self.x][self.y] = [oldValue[0], CONEJO]
        if terrain.manipulable_world[self.x][self.y][1] == ZANAHORIA_CONEJO:
            pass  #ahora es pelea

        if terrain.manipulable_world[self.x][self.y][1] == ZANAHORIA:
            terrain.manipulable_world[self.x][self.y][1] = ZANAHORIA_CONEJO
        else:
            terrain.manipulable_world[self.x][self.y][1] == CONEJO

    def action(self, terrain):
        '''Función para calcular nuestra siguiente acción.'''

        Animal.action(terrain)

        #Check map with vision_field
        has_hunger = self.hunger < HUNGER_FEELING_LIMIT
        want_reproduction = self.reproductive_need < REPRODUCTIONH_FEELING_LIMIT
        vision_scan, nearest_coord = NADA, (None, None)
        dist = None
        for i in range(self.x - self.vision_field, self.x + self.vision_field):
            for j in range(self.x - self.vision_field,
                           self.x + self.vision_field):

                #si vemos una casilla con un lince
                if terrain[i][j][0] >= LINCE:
                    if vision_scan >= LINCE:
                        auxDist = Funciones.dist((i, j), (self.x, self.y))
                        if auxDist < dist:
                            dist = auxDist
                            nearest_coord = (i, j)
                    else:
                        vision_scan, nearest_coord = LINCE, (i, j)
                        dist = Funciones.dist((self.x, self.y), (i, j))

                #si no hay linces
                elif vision_scan < LINCE and has_hunger and terrain[i][j][
                        0] == ZANAHORIA:
                    if vision_scan == ZANAHORIA:
                        auxDist = Funciones.dist((i, j), (self.x, self.y))
                        if auxDist < dist:
                            dist = auxDist
                            nearest_coord = (i, j)
                    else:
                        vision_scan, nearest_coord = ZANAHORIA, (i, j)
                        dist = Funciones.dist((self.x, self.y), (i, j))

                elif vision_scan < ZANAHORIA and terrain[i][j][
                        0] == ZANAHORIA_CONEJO and self.hunger * self.risk_aversion < ATTACK_LIMIT:
                    if vision_scan == ZANAHORIA_CONEJO:
                        auxDist = Funciones.dist((i, j), (self.x, self.y))
                        if auxDist < dist:
                            dist = auxDist
                            nearest_coord = (i, j)
                    else:
                        vision_scan, nearest_coord = ZANAHORIA_CONEJO, (i, j)
                        dist = Funciones.dist((self.x, self.y), (i, j))

                elif vision_scan < ZANAHORIA_CONEJO and want_reproduction and terrain[
                        i][j][0] == CONEJO:
                    if vision_scan == CONEJO:
                        auxDist = Funciones.dist((i, j), (self.x, self.y))
                        if auxDist < dist:
                            dist = auxDist
                            nearest_coord = (i, j)
                    else:
                        vision_scan, nearest_coord = CONEJO, (i, j)
                        dist = Funciones.dist((self.x, self.y), (i, j))

            #veredicto final vision_scan
            if vision_scan >= LINCE:
                self.flee(nearest_coord[0], nearest_coord[1])
            elif vision_scan == NADA:
                pass  #nos movemos random e inteligentemente
            else:
                if vision_scan == ZANAHORIA_CONEJO:
                    self.wants_fight = True
                elif vision_scan == CONEJO:
                    self.wants_reproduction = True
                self.goTo(nearest_coord[0],
                          nearest_coord[1])  #vamos a comer o reproducirnos

    def move(self, diffX, diffY, terrain):
        if diffX != 0 or diffY != 0:  #Cheking if there is movement
            absDiffX = 0 if diffX == 0 else diffX / abs(diffX)
            absDiffY = 0 if diffY == 0 else diffY / abs(diffY)
            if terrain[self.x + absDiffX][self.y + absDiffY][0] > ZANAHORIA:
                diffSum = absDiffX + absDiffY
                if diffSum == -1 or diffSum == 1:  #Moving in one axis
                    if absDiffX == 0:
                        if terrain[self.x + 1][self.y + absDiffY][0] <= ZANAHORIA:
                            self.x += 1
                            self.y += absDiffY
                        elif terrain[self.x - 1][self.y +
                                                 absDiffY][0] <= ZANAHORIA:
                            self.x += -1
                            self.y += absDiffY
                    else:
                        if terrain[self.x][self.y + absDiffY + 1][0] <= ZANAHORIA:
                            self.x += absDiffX
                            self.y += 1
                        elif terrain[self.x][self.y + absDiffY -
                                             1][0] <= ZANAHORIA:
                            self.x += absDiffX
                            self.y += -1
                else:  # Moving in two axis
                    if terrain[self.x][self.y + absDiffY][0] <= ZANAHORIA:
                        self.y += absDiffY
                    elif terrain[self.x + absDiffX][self.y][0] <= ZANAHORIA:
                        self.x += absDiffX

            else:
                self.x += absDiffX
                self.y += absDiffY

    def goTo(self, i, j):
        '''Función para ir a las coordenadas indicadas'''

        extra = EXTRA_STEP if self.strength_speed > numero_random_que_borraremos else 0

        for _ in range(MOVES_PER_ACTION + extra):
            diffX = i - self.x
            diffY = j - self.y

            self.move(diffX, diffY)

        self.display()

    def flee(self, i, j):
        '''Función para huir de las coordenadas indicadas'''

        diffX = (self.x - i) * (MOVES_PER_ACTION + EXTRA_STEP)
        diffY = (self.y - j) * (MOVES_PER_ACTION + EXTRA_STEP)

        self.goTo(i + diffX, j + diffY)

    def eat(self, terrain):
        #pasan los ticks de comer
        self.hunger -= HUNGER_QUENCH
        terrain[self.x][self.y] = CONEJO  #solo estoy yo

    def attack(self):
        pass

    def reproduce(self):
        pass


class Lynx(Animal):
    def __init__(self):
        Animal.__init__(self)
        self.suffocation = 0

    def display(terrain, x, y):
        terrain[x][y] = [207, 147, 45]


class Zanahoria():
    def __init__(self):
        self.x = random.randint(
            10, 20)  #habrá que generarlas solo en zonas de hierba
        self.y = random.randint(10, 20)

    def display(self, terrain):
        oldValue = terrain[self.x][self.y]
        terrain[self.x][self.y] = [oldValue[0], ZANAHORIA]
