HUNGER_LOSS = 0.01
HUNGER_FEELING_LIMIT = 0.3
REPRODUCTIONH_FEELING_LIMIT = 0.5
ATTACK_LIMIT = 0.1
MIN_SPEED = 5
MAX_SPEED = 20
EAT_DELAY = 4  #ticks
HUNGER_QUENCH = 0.3
MOVES_PER_ACTION = 1
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
        self.vision_field = 5
        self.risk_aversion = 0
        self.racionality = 0

        #Life attributes
        self.max_time_alive = 100
        self.time_alive = 0

        #Map position
        self.x = int(50)
        self.y = int(50)

        self.lastX = self.x
        self.lastY = self.y

        self.wants_fight = False
        self.wants_reproduction = False

        self.eat_ticks = 0

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
        if terrain[self.x][self.y][1] == ZANAHORIA_CONEJO:
            pass  #ahora es pelea
        elif terrain[self.x][self.y][1] == ZANAHORIA:
            terrain[self.x][self.y][1] = ZANAHORIA_CONEJO
        elif terrain[self.x][self.y][1] == CONEJO:
            pass  #reproduccion
        else:
            terrain[self.x][self.y][1] = CONEJO

        if not (self.x == self.lastX and self.y == self.lastY):
            terrain[self.lastX][self.lastY][1] = 0
            self.lastX = self.x
            self.lastY = self.y

        # print('x', self.x, 'y', self.y)

    def action(self, terrain):
        '''Función para calcular nuestra siguiente acción.'''

        # Animal.action(self, terrain)

        if terrain[self.x][self.y][1] == ZANAHORIA_CONEJO:
            self.eat(terrain)
        elif terrain[self.x][self.y][1] == CONEJO_REPRODUCCION:
            pass
        elif terrain[self.x][self.y][1] == CONEJO_CONEJO:
            pass
        elif terrain[self.x][self.y][1] == PELEA_CONEJO:
            pass  #reiniciar eat_ticks
        elif terrain[self.x][self.y][1] == CONEJO_LINCE:
            pass  #reiniciar eat_ticks del conejo
        else:

            #Check map with vision_field
            has_hunger = self.hunger < HUNGER_FEELING_LIMIT
            want_reproduction = self.reproductive_need < REPRODUCTIONH_FEELING_LIMIT
            vision_scan, nearest_coord = NADA, (None, None)
            dist = None
            for i in range(self.x - self.vision_field,
                           self.x + self.vision_field):
                for j in range(self.y - self.vision_field,
                               self.y + self.vision_field):
                    if not (i == self.x and
                            j == self.y):  #no nos evaluamos a nosotros mismos
                        #si vemos una casilla con un lince
                        if terrain[i][j][1] >= LINCE:
                            if vision_scan >= LINCE:
                                auxDist = Funciones.dist((i, j),
                                                         (self.x, self.y))
                                if auxDist < dist:
                                    dist = auxDist
                                    nearest_coord = (i, j)
                            else:
                                vision_scan, nearest_coord = LINCE, (i, j)
                                dist = Funciones.dist((self.x, self.y), (i, j))

                        #si no hay linces
                        elif (vision_scan < LINCE) and (has_hunger) and (
                                terrain[i][j][1] == ZANAHORIA):
                            if vision_scan == ZANAHORIA:
                                auxDist = Funciones.dist((i, j),
                                                         (self.x, self.y))
                                if auxDist < dist:
                                    dist = auxDist
                                    nearest_coord = (i, j)
                            else:
                                vision_scan, nearest_coord = ZANAHORIA, (i, j)
                                dist = Funciones.dist((self.x, self.y), (i, j))

                        elif vision_scan < ZANAHORIA and terrain[i][j][
                                1] == ZANAHORIA_CONEJO and self.hunger * self.risk_aversion < ATTACK_LIMIT:
                            if vision_scan == ZANAHORIA_CONEJO:
                                auxDist = Funciones.dist((i, j),
                                                         (self.x, self.y))
                                if auxDist < dist:
                                    dist = auxDist
                                    nearest_coord = (i, j)
                            else:
                                vision_scan, nearest_coord = ZANAHORIA_CONEJO, (
                                    i, j)
                                dist = Funciones.dist((self.x, self.y), (i, j))

                        elif vision_scan < ZANAHORIA_CONEJO and want_reproduction and terrain[
                                i][j][1] == CONEJO:
                            print(nearest_coord)
                            if vision_scan == CONEJO:
                                auxDist = Funciones.dist((i, j),
                                                         (self.x, self.y))
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
                self.moveRandom(terrain)
                # print("NADA")
            else:
                if vision_scan == ZANAHORIA_CONEJO:
                    self.wants_fight = True
                elif vision_scan == CONEJO:
                    self.wants_reproduction = True
                self.goTo(nearest_coord[0], nearest_coord[1],
                          terrain)  #vamos a comer o reproducirnos

    def moveRandom(self, terrain):
        random_eje_x = random.randint(-1, 1)
        random_eje_y = random.randint(-1, 1)

        extra = EXTRA_STEP if self.strength_speed > numero_random_que_borraremos else 0

        for _ in range(MOVES_PER_ACTION + extra):
            diffX = random_eje_x
            diffY = random_eje_y

            self.move(diffX, diffY, terrain)

        self.display(terrain)

    def move(self, diffX, diffY, terrain):
        if diffX != 0 or diffY != 0:  #Checking if there is movement
            absDiffX = 0 if diffX == 0 else diffX // abs(diffX)
            absDiffY = 0 if diffY == 0 else diffY // abs(diffY)
            if self.wants_fight:
                if terrain[self.x + absDiffX][self.y +
                                              absDiffY][1] > ZANAHORIA:
                    diffSum = absDiffX + absDiffY
                    if diffSum == -1 or diffSum == 1:  #Moving in one axis
                        if absDiffX == 0:
                            if terrain[self.x + 1][self.y +
                                                   absDiffY][1] <= ZANAHORIA:
                                self.x += 1
                                self.y += absDiffY
                            elif terrain[self.x - 1][self.y +
                                                     absDiffY][1] <= ZANAHORIA:
                                self.x += -1
                                self.y += absDiffY
                        else:
                            if terrain[self.x][self.y + absDiffY +
                                               1][1] <= ZANAHORIA:
                                self.x += absDiffX
                                self.y += 1
                            elif terrain[self.x][self.y + absDiffY -
                                                 1][1] <= ZANAHORIA:
                                self.x += absDiffX
                                self.y += -1
                    else:  # Moving in two axis
                        if terrain[self.x][self.y + absDiffY][1] <= ZANAHORIA:
                            self.y += absDiffY
                        elif terrain[self.x +
                                     absDiffX][self.y][1] <= ZANAHORIA:
                            self.x += absDiffX

                else:
                    self.x += absDiffX
                    self.y += absDiffY
            else:
                if terrain[self.x + absDiffX][self.y + absDiffY][1] > ZANAHORIA and\
                        terrain[self.x + absDiffX][self.y + absDiffY][1] != ZANAHORIA_CONEJO:
                    diffSum = absDiffX + absDiffY
                    if diffSum == -1 or diffSum == 1:  #Moving in one axis
                        if absDiffX == 0:
                            if terrain[self.x + 1][self.y + absDiffY][1] <= ZANAHORIA and\
                                    terrain[self.x + 1][self.y + absDiffY][1] != ZANAHORIA_CONEJO:
                                self.x += 1
                                self.y += absDiffY
                            elif terrain[self.x - 1][self.y + absDiffY][1] <= ZANAHORIA and\
                                    terrain[self.x - 1][self.y + absDiffY][1] != ZANAHORIA_CONEJO:
                                self.x += -1
                                self.y += absDiffY
                        else:
                            if terrain[self.x][self.y + absDiffY + 1][1] <= ZANAHORIA and\
                                    terrain[self.x][self.y + absDiffY + 1][1] != ZANAHORIA_CONEJO:
                                self.x += absDiffX
                                self.y += 1
                            elif terrain[self.x][self.y + absDiffY - 1][1] <= ZANAHORIA and\
                                    terrain[self.x][self.y + absDiffY - 1][1] != ZANAHORIA_CONEJO:
                                self.x += absDiffX
                                self.y += -1
                    else:  # Moving in two axis
                        if terrain[self.x][self.y + absDiffY][1] <= ZANAHORIA and\
                                terrain[self.x][self.y + absDiffY][1] != ZANAHORIA_CONEJO :
                            self.y += absDiffY
                        elif terrain[self.x + absDiffX][self.y][1] <= ZANAHORIA and \
                                terrain[self.x + absDiffX][self.y][1] != ZANAHORIA_CONEJO:
                            self.x += absDiffX

                else:
                    self.x += absDiffX
                    self.y += absDiffY

    def goTo(self, i, j, terrain):
        '''Función para ir a las coordenadas indicadas'''
        print("going to:", i, " ", j)
        print("we are in:", self.x, self.y)
        extra = EXTRA_STEP if self.strength_speed > numero_random_que_borraremos else 0

        for _ in range(MOVES_PER_ACTION + extra):
            diffX = i - self.x
            diffY = j - self.y

            self.move(diffX, diffY, terrain)

        # print(diffX, diffX, self.x, self.y)
        self.display(terrain)

    def flee(self, i, j):
        '''Función para huir de las coordenadas indicadas'''

        diffX = (self.x - i) * (MOVES_PER_ACTION + EXTRA_STEP)
        diffY = (self.y - j) * (MOVES_PER_ACTION + EXTRA_STEP)

        self.goTo(i + diffX, j + diffY)

    def eat(self, terrain):
        print("Eating")
        self.eat_ticks += 1
        if self.eat_ticks == EAT_DELAY:
            self.eat_ticks = 0
            self.hunger -= HUNGER_QUENCH
            terrain[self.x][self.y][1] = CONEJO  #solo estoy yo

    def attack(self):
        pass

    def reproduce(self):
        pass


class Lynx(Animal):
    def __init__(self):
        Animal.__init__(self)
        self.suffocation = 0

    def display(self, terrain, x, y):
        terrain[self.x][self.y][1] = LINCE


class Zanahoria():
    def __init__(self, terrain):
        '''
            Carrot class and generator. Carrots are only generated where the grass is lightGreen or green.
        '''

        carrotCondition = (terrain[:, :, 1] == 0) & (terrain[:, :, 0] >= 2) & (
            terrain[:, :, 0] <= 3)

        x, y = np.where(carrotCondition)

        i = np.random.randint(len(x))
        random_pos = [x[i], y[i]]

        self.x = random_pos[0]
        self.y = random_pos[1]

        terrain[self.x][self.y][1] = ZANAHORIA
