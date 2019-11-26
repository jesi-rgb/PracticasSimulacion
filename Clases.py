LYNX_HUNGER_LOSS = 0.003
LYNX_REPRODUCTIVE_FEELING_GAIN = 0.0025
LYNX_HUNGER_FEELING_LIMIT = 0.5

LYNX_MAX_INITIAL_HUNGER = 0.5
LYNX_MAX_INITIAL_REPR = 0.2

RABBIT_HUNGER_LOSS = 0.01
RABBIT_REPRODUCTIVE_FEELING_GAIN = 0.015
RABBIT_HUNGER_FEELING_LIMIT = 0.3

RABBIT_MAX_INITIAL_HUNGER = 0.5
RABBIT_MAX_INITIAL_REPR = 0.4

REPRODUCTIONH_FEELING_LIMIT = 1

SUFFOCATION_GAIN = 0.03
SUFFOCATION_LOSS = 0.028

ATTACK_LIMIT = 0.1
MIN_SPEED = 5
MAX_SPEED = 20
EAT_DELAY = 2  #ticks
HUNGER_QUENCH = 0.3
MOVES_PER_ACTION = 2
EXTRA_STEP = 1
MAX_TIME_ALIVE = 1000
SEMILLA = 918273645
VISION_LENGTH = 5


# Death mode
OLD_AGE = 'Old Age'
HUNGER = 'Hunger'
FIGHT = 'Fighting'
EATEN = 'Eaten'
SUFFOCATION = 'Suffocation'

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
LINCE_REPRODUCCION = 12

#Estructuras de datos
rabbit_fight_dict = dict()
rabbit_reproduction_dict = dict()

lynx_fight_dict = dict()
lynx_reproduction_dict = dict()

import Funciones
from PIL import Image
import numpy as np
import random
from Funciones import HEIGTH, W_FACTOR, WIDTH, H_FACTOR
import global_variables as gv
from pygame.time import get_ticks
import pandas as pd



random.seed(SEMILLA)


class Rabbit:
    def __init__(self, terrain, x = None, y = None, risk_av = None, strength_spe = None):


        #Survival attributes
        self.id = gv.rabbit_id
        gv.rabbit_id += 1
        self.hunger = random.uniform(0, RABBIT_MAX_INITIAL_HUNGER)
        self.reproductive_need = random.uniform(0, RABBIT_MAX_INITIAL_REPR)
        self.vision_field = VISION_LENGTH

        #Life attributes
        self.max_time_alive = MAX_TIME_ALIVE * random.uniform(0.6, 1)
        self.time_alive = 0

        #Map position
        if x is not None:
            self.x = x
            self.y = y
            self.risk_aversion = risk_av
            self.strength_speed = strength_spe


        else:
            rabbitCondition = (terrain[:, :, 1] == 0) & (terrain[:, :, 0] >= 2) & (
                    terrain[:, :, 0] <= 3)

            x, y = np.where(rabbitCondition)

            i = random.randint(0, len(x)-1)

            random_pos = [x[i], y[i]]

            self.x = random_pos[0]
            self.y = random_pos[1]

            self.risk_aversion = random.random()
            self.strength_speed = random.random()


        self.lastX = self.x
        self.lastY = self.y

        #Desires
        self.wants_fight = False
        self.wants_reproduction = False

        self.eat_ticks = 0

        gv.rabbit_cont += 1
        terrain[self.x][self.y][1] = CONEJO


    def display(self, terrain):
        '''Función para editar el valor x, y del mundo donde nos situamos ahora mismo'''

        if not (self.x == self.lastX and self.y == self.lastY):
            if terrain[self.x][self.y][1] == ZANAHORIA_CONEJO:
                terrain[self.x][self.y][1] = PELEA_CONEJO
                rabbit_fight_dict[str(self.x)+"-"+str(self.y)] = self.strength_speed * random.random()

            elif terrain[self.x][self.y][1] == ZANAHORIA:
                terrain[self.x][self.y][1] = ZANAHORIA_CONEJO

            elif terrain[self.x][self.y][1] == CONEJO and self.wants_reproduction:
                rabbit_reproduction_dict[str(self.x)+"-"+str(self.y)] = (self.risk_aversion, self.strength_speed)
                terrain[self.x][self.y][1] = CONEJO_REPRODUCCION

            elif terrain[self.x][self.y][1] == CONEJO and not self.wants_reproduction:
                terrain[self.x][self.y][1] = CONEJO_CONEJO

            else:
                terrain[self.x][self.y][1] = CONEJO

        #Actualizamos la casilla de donde procedemos

            if terrain[self.lastX][self.lastY][1] == CONEJO:
                terrain[self.lastX][self.lastY][1] = NADA

            elif terrain[self.lastX][self.lastY][1] == NADA:
                terrain[self.lastX][self.lastY][1] = NADA

            else:
                terrain[self.lastX][self.lastY][1] = CONEJO

            self.lastX = self.x
            self.lastY = self.y

    def action(self, terrain, rabbit_dict):
        '''Función para calcular nuestra siguiente acción.'''

        self.time_alive += 1
        if self.time_alive >= self.max_time_alive:
            self.die(terrain, gv.rabbit_dict, OLD_AGE)

        if terrain[self.x][self.y][1] == ZANAHORIA_CONEJO:
            self.eat(terrain)

        elif terrain[self.x][self.y][1] == CONEJO_REPRODUCCION and self.reproductive_need > REPRODUCTIONH_FEELING_LIMIT:
            if rabbit_reproduction_dict[str(self.x)+"-"+str(self.y)] == None:
                terrain[self.x][self.y][1] = CONEJO_CONEJO
                self.reproductive_need = 0
                del rabbit_reproduction_dict[str(self.x)+"-"+str(self.y)]

            else:
                self.reproductive_need = 0
                self.reproduce(terrain, gv.rabbit_dict)
                rabbit_reproduction_dict[str(self.x)+"-"+str(self.y)] = None

        elif terrain[self.x][self.y][1] == PELEA_CONEJO:
            if rabbit_fight_dict[str(self.x) + "-" + str(self.y)] == None:  #Ganaste tu
                terrain[self.x][self.y][1] = ZANAHORIA_CONEJO
                self.eat(terrain)
                del rabbit_fight_dict[str(self.x)+"-"+str(self.y)]

            elif rabbit_fight_dict[str(self.x)+"-"+str(self.y)] == False: #Gana el
                self.die(terrain, gv.rabbit_dict, FIGHT)
                del rabbit_fight_dict[str(self.x)+"-"+str(self.y)]

            elif rabbit_fight_dict[str(self.x)+"-"+str(self.y)] > self.strength_speed * random.random(): #El menor gana - Ganamos nosotros
                rabbit_fight_dict[str(self.x)+"-"+str(self.y)] = False
                self.eat(terrain)

            else:
                rabbit_fight_dict[str(self.x)+"-"+str(self.y)] = None #Gana el
                self.die(terrain, gv.rabbit_dict, FIGHT)

        elif terrain[self.x][self.y][1] == CONEJO_LINCE or terrain[self.x][self.y][1] == PELEA_LINCE:
            self.die(terrain, gv.rabbit_dict, EATEN)

        elif self.hunger >= 1:
            self.die(terrain, gv.rabbit_dict, HUNGER)

        else:
            #Check map with vision_field
            has_hunger = self.hunger > RABBIT_HUNGER_FEELING_LIMIT
            want_reproduction = self.reproductive_need > REPRODUCTIONH_FEELING_LIMIT
            vision_scan, nearest_coord = NADA, (None, None)
            dist = None
            for i in range(self.x - self.vision_field,
                           self.x + self.vision_field):
                if i >= 0 and i<(HEIGTH/H_FACTOR):
                    for j in range(self.y - self.vision_field,
                                   self.y + self.vision_field):
                        if j >= 0 and j<(HEIGTH/H_FACTOR):
                            if not (i == self.x and
                                    j == self.y):  #no nos evaluamos a nosotros mismos
                                #si vemos una casilla con un lince
                                try:
                                    terrain_obj = terrain[i][j][1]
                                    if terrain_obj >= LINCE:
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
                                            terrain_obj == ZANAHORIA):
                                        if vision_scan == ZANAHORIA:
                                            auxDist = Funciones.dist((i, j),
                                                                     (self.x, self.y))
                                            if auxDist < dist:
                                                dist = auxDist
                                                nearest_coord = (i, j)
                                        else:
                                            vision_scan, nearest_coord = ZANAHORIA, (i, j)
                                            dist = Funciones.dist((self.x, self.y), (i, j))

                                    elif vision_scan < ZANAHORIA and terrain_obj == ZANAHORIA_CONEJO and\
                                            self.hunger * self.risk_aversion < ATTACK_LIMIT:
                                        if vision_scan == ZANAHORIA_CONEJO:
                                            auxDist = Funciones.dist((i, j), (self.x, self.y))
                                            if auxDist < dist:
                                                dist = auxDist
                                                nearest_coord = (i, j)
                                        else:
                                            vision_scan, nearest_coord = ZANAHORIA_CONEJO, (
                                                i, j)
                                            dist = Funciones.dist((self.x, self.y), (i, j))

                                    elif vision_scan < ZANAHORIA_CONEJO and want_reproduction and\
                                            terrain_obj == CONEJO:
                                        if vision_scan == CONEJO:
                                            auxDist = Funciones.dist((i, j),
                                                                     (self.x, self.y))
                                            if auxDist < dist:
                                                dist = auxDist
                                                nearest_coord = (i, j)
                                        else:
                                            vision_scan, nearest_coord = CONEJO, (i, j)
                                            dist = Funciones.dist((self.x, self.y), (i, j))
                                except IndexError:
                                    pass

            #veredicto final vision_scan
            if vision_scan >= LINCE:
                self.flee(nearest_coord[0], nearest_coord[1], terrain)
            elif vision_scan == NADA:
                self.moveRandom(terrain)
            else:
                if vision_scan == ZANAHORIA_CONEJO:
                    self.wants_fight = True
                elif vision_scan == CONEJO:
                    self.wants_reproduction = True
                self.goTo(nearest_coord[0], nearest_coord[1],
                          terrain)  #vamos a comer o reproducirnos

            #Sumamos el hambre
            self.hunger += RABBIT_HUNGER_LOSS
            self.reproductive_need += RABBIT_REPRODUCTIVE_FEELING_GAIN

    def moveRandom(self, terrain):
        if self.x <= 0:
            random_eje_x = random.randint(0, 1)
        elif self.x >= (HEIGTH/H_FACTOR)-1:
            random_eje_x = random.randint(-1, 0)
        else:
            random_eje_x = random.randint(-1, 1)
        if self.y <= 0:
            random_eje_y = random.randint(0, 1)
        elif self.y >= (HEIGTH/H_FACTOR)-1:
            random_eje_y = random.randint(-1, 0)
        else:
            random_eje_y = random.randint(-1, 1)

        extra = EXTRA_STEP if self.strength_speed > random.random() else 0

        for _ in range(MOVES_PER_ACTION + extra):
            diffX = random_eje_x
            diffY = random_eje_y

            self.move(diffX, diffY, terrain)

        self.display(terrain)

    def move(self, diffX, diffY, terrain):
        absDiffX = 0 if diffX == 0 else diffX // abs(diffX)
        absDiffY = 0 if diffY == 0 else diffY // abs(diffY)
        if (self.x + absDiffX) < 0 or (self.x + absDiffX) >= (WIDTH/W_FACTOR):
            absDiffX = 0
        if (self.y + absDiffY) < 0 or (self.y + absDiffY) >= (HEIGTH/H_FACTOR):
            absDiffY = 0
        if absDiffX != 0 or absDiffY != 0:  #Checking if there is movement
            if self.wants_fight:
                if terrain[self.x + absDiffX][self.y +
                                              absDiffY][1] > ZANAHORIA:
                    diffSum = absDiffX + absDiffY
                    if diffSum == -1 or diffSum == 1:  #Moving in one axis
                        if absDiffX == 0:
                            if self.x < (HEIGTH/H_FACTOR)-1 and terrain[self.x + 1][self.y +
                                                   absDiffY][1] <= ZANAHORIA:
                                self.x += 1
                                self.y += absDiffY
                            elif self.x != 0 and terrain[self.x - 1][self.y +
                                                     absDiffY][1] <= ZANAHORIA:
                                self.x += -1
                                self.y += absDiffY
                        else:
                            if self.y < (HEIGTH/H_FACTOR)-1 and terrain[self.x + absDiffX][self.y + 1][1] <= ZANAHORIA:
                                self.x += absDiffX
                                self.y += 1
                            elif self.y != 0 and terrain[self.x + absDiffX][self.y - 1][1] <= ZANAHORIA:
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
                            if self.x < (HEIGTH/H_FACTOR)-1 and terrain[self.x + 1][self.y + absDiffY][1] <= ZANAHORIA and\
                                    terrain[self.x + 1][self.y + absDiffY][1] != ZANAHORIA_CONEJO:
                                self.x += 1
                                self.y += absDiffY
                            elif self.x != 0 and terrain[self.x - 1][self.y + absDiffY][1] <= ZANAHORIA and\
                                    terrain[self.x - 1][self.y + absDiffY][1] != ZANAHORIA_CONEJO:
                                self.x += -1
                                self.y += absDiffY
                        else:
                            if self.y < (HEIGTH/H_FACTOR)-1 and terrain[self.x + absDiffX][self.y + 1][1] <= ZANAHORIA and\
                                    terrain[self.x + absDiffX][self.y + 1][1] != ZANAHORIA_CONEJO:
                                self.x += absDiffX
                                self.y += 1
                            elif self.y != 0 and terrain[self.x + absDiffX][self.y - 1][1] <= ZANAHORIA and\
                                    terrain[self.x + absDiffX][self.y - 1][1] != ZANAHORIA_CONEJO:
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

            self.x = int(self.x%int(WIDTH/W_FACTOR))
            self.y = int(self.y%int(HEIGTH/H_FACTOR))

    def goTo(self, i, j, terrain):
        '''Función para ir a las coordenadas indicadas'''
        extra = EXTRA_STEP if self.strength_speed > random.random() else 0

        for _ in range(MOVES_PER_ACTION + extra):
            diffX = i - self.x
            diffY = j - self.y

            self.move(diffX, diffY, terrain)

        self.display(terrain)

    def flee(self, i, j, terrain):
        '''Función para huir de las coordenadas indicadas'''

        extra = EXTRA_STEP if self.strength_speed > random.random() else 0

        for _ in range(MOVES_PER_ACTION + extra):
            diffX = self.x - i
            diffY = self.y - j

            self.move(diffX, diffY, terrain)

        # print(diffX, diffX, self.x, self.y)
        self.display(terrain)

    def eat(self, terrain):
        self.eat_ticks += 1
        if self.eat_ticks == EAT_DELAY:
            self.eat_ticks = 0
            self.hunger -= HUNGER_QUENCH
            terrain[self.x][self.y][1] = CONEJO  #solo estoy yo

    def reproduce(self, terrain, rabbit_dict):
        #mutar y juntar con rabbit_reproduction_dict
        aux_i = 0
        aux_j = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if terrain[(self.x+i)%int(WIDTH/W_FACTOR)][(self.y+j)%int(HEIGTH/H_FACTOR)][1] == NADA:
                    aux_i = i
                    aux_j = j
                    exit

        if aux_i != 0 or aux_j != 0:
            risk2, strength2 = rabbit_reproduction_dict[str(self.x)+"-"+str(self.y)]
            risk_av_child, strength_speed_child = Funciones.cruce_and_mutate(self.risk_aversion, risk2, self.strength_speed, strength2)

            x_child = int((self.x+aux_i)%(WIDTH/W_FACTOR))
            y_child = int((self.y+aux_j)%(HEIGTH/H_FACTOR))
            aux_rabbit = Rabbit(terrain, x_child , y_child, risk_av_child, strength_speed_child)
            rabbit_dict[gv.rabbit_id-1] = aux_rabbit
            terrain[x_child][y_child][1] = CONEJO

    def die(self, terrain, rabbit_dict, mode):
        aux = terrain[self.x][self.y][1]

        if aux == CONEJO:
            terrain[self.x][self.y][1] = NADA
        elif aux == ZANAHORIA_CONEJO:
            terrain[self.x][self.y][1] = ZANAHORIA
        elif aux == CONEJO_CONEJO or aux == CONEJO_REPRODUCCION:
            terrain[self.x][self.y][1] = NADA
        elif aux == PELEA_CONEJO:
            terrain[self.x][self.y][1] = ZANAHORIA_CONEJO

        gv.rabbit_cont -= 1
        gv.rabbit_df.loc[self.id-1] = [mode, self.strength_speed, self.risk_aversion, float(get_ticks() // 1000)]
        del gv.rabbit_dict[self.id]





class Lynx:
    def __init__(self, terrain, x = None, y = None, risk_av = None, strength_spe = None):

        #Survival attributes
        self.id = gv.lynx_id
        gv.lynx_id += 1
        self.suffocation = 0
        self.hunger = random.uniform(0, LYNX_MAX_INITIAL_HUNGER)
        self.reproductive_need = random.uniform(0, LYNX_MAX_INITIAL_REPR)
        self.vision_field = VISION_LENGTH

        #Life attributes
        self.max_time_alive = MAX_TIME_ALIVE * random.uniform(0.6, 1)
        self.time_alive = 0

        #Map position
        if x is not None:
            self.x = x
            self.y = y
            self.risk_aversion = risk_av
            self.strength_speed = strength_spe


        else:
            linxCondition = (terrain[:, :, 1] == 0) & (terrain[:, :, 0] >= 5)

            x, y = np.where(linxCondition)

            i = random.randint(0, len(x)-1)

            random_pos = [x[i], y[i]]

            self.x = random_pos[0]
            self.y = random_pos[1]

            self.risk_aversion = random.random()
            self.strength_speed = random.random()


        self.lastX = self.x
        self.lastY = self.y

        self.lastMountainX = self.x
        self.lastMountainY = self.y

        self.lastGreenX = None
        self.lastGreenY = None

        #Desires
        self.wants_fight = False
        self.wants_reproduction = False

        self.eat_ticks = 0

        gv.lynx_cont += 1
        terrain[self.x][self.y][1] = LINCE

    def display(self, terrain):

        if not (self.x == self.lastX and self.y == self.lastY):

            current_terrain_cell = terrain[self.x][self.y][1]

            if current_terrain_cell == CONEJO or current_terrain_cell == ZANAHORIA_CONEJO \
                    or current_terrain_cell == CONEJO_CONEJO \
                    or current_terrain_cell == CONEJO_REPRODUCCION \
                    or current_terrain_cell == PELEA_CONEJO:
                terrain[self.x][self.y][1] = CONEJO_LINCE
            elif current_terrain_cell == CONEJO_LINCE:
                terrain[self.x][self.y][1] = PELEA_LINCE
                lynx_fight_dict[str(self.x)+"-"+str(self.y)] = self.strength_speed * random.random()
            elif current_terrain_cell == ZANAHORIA:
                terrain[self.x][self.y][1] = ZANAHORIA_LINCE
            elif current_terrain_cell == LINCE and self.wants_reproduction:
                lynx_reproduction_dict[str(self.x)+"-"+str(self.y)] = (self.risk_aversion, self.strength_speed)
                terrain[self.x][self.y][1] = LINCE_REPRODUCCION
            elif current_terrain_cell == LINCE and not self.wants_reproduction:
                terrain[self.x][self.y][1] = LINCE_LINCE
            else:
                terrain[self.x][self.y][1] = LINCE

            #Actualizamos la casilla de donde procedemos

            if terrain[self.lastX][self.lastY][1] == LINCE:
                terrain[self.lastX][self.lastY][1] = NADA
            elif terrain[self.lastX][self.lastY][1] == NADA:
                terrain[self.lastX][self.lastY][1] = NADA
            elif terrain[self.lastX][self.lastY][1] == ZANAHORIA_LINCE:
                terrain[self.lastX][self.lastY][1] = ZANAHORIA
            elif terrain[self.lastX][self.lastY][1] == LINCE_LINCE \
                    or terrain[self.lastX][self.lastY][1] == LINCE_REPRODUCCION:
                terrain[self.lastX][self.lastY][1] = LINCE
            self.lastX = self.x
            self.lastY = self.y

    def action(self, terrain, lynx_dict):
        '''Función para calcular nuestra siguiente acción.'''

        self.time_alive += 1
        if self.time_alive >= self.max_time_alive:
            self.die(terrain, gv.lynx_dict, OLD_AGE)

        if terrain[self.x][self.y][1] == CONEJO_LINCE:
            self.eat(terrain)
        elif terrain[self.x][self.y][1] == LINCE_REPRODUCCION and self.reproductive_need > REPRODUCTIONH_FEELING_LIMIT:
            if lynx_reproduction_dict[str(self.x)+"-"+str(self.y)] == None:
                terrain[self.x][self.y][1] = LINCE_LINCE
                self.reproductive_need = 0
                del lynx_reproduction_dict[str(self.x)+"-"+str(self.y)]
            else:
                self.reproductive_need = 0
                self.reproduce(terrain, gv.lynx_dict)
                lynx_reproduction_dict[str(self.x)+"-"+str(self.y)] = None
        elif terrain[self.x][self.y][1] == PELEA_LINCE:
            if lynx_fight_dict[str(self.x)+"-"+str(self.y)] == None: #Ganaste tu
                terrain[self.x][self.y][1] = CONEJO_LINCE
                self.eat(terrain)
                del lynx_fight_dict[str(self.x)+"-"+str(self.y)]
            elif lynx_fight_dict[str(self.x)+"-"+str(self.y)] == False: #Gana el
                self.die(terrain, gv.lynx_dict, FIGHT)
                del lynx_fight_dict[str(self.x)+"-"+str(self.y)]
            elif lynx_fight_dict[str(self.x)+"-"+str(self.y)] \
                    > self.strength_speed * random.random(): #El menor gana - Ganamos nosotros
                lynx_fight_dict[str(self.x)+"-"+str(self.y)] = False
                self.eat(terrain)
            else:
                lynx_fight_dict[str(self.x)+"-"+str(self.y)] = None #Gana el
                self.die(terrain, gv.lynx_dict, FIGHT)

        elif self.hunger >= 1:
            self.die(terrain, gv.lynx_dict, HUNGER)

        elif self.suffocation > 1:
            self.die(terrain, gv.lynx_dict, SUFFOCATION)
        elif (0.9 - self.suffocation ) < \
                (Funciones.dist((self.x, self.y),(self.lastMountainX, self.lastMountainY)) * SUFFOCATION_GAIN):
            # print("Voy a respirar")
            self.hunger += LYNX_HUNGER_LOSS
            self.reproductive_need += LYNX_REPRODUCTIVE_FEELING_GAIN
            if terrain[self.x][self.y][0] >= 5:
                self.suffocation -= SUFFOCATION_LOSS
            else:
                self.suffocation += SUFFOCATION_GAIN
            self.goTo(self.lastMountainX, self.lastMountainY, terrain)
        elif self.hunger > LYNX_HUNGER_FEELING_LIMIT and terrain[self.x][self.y][0] >=5 \
                and self.lastGreenX is not None and self.suffocation < 0.8:
            # print("Voy a comer", terrain[self.lastGreenX][self.lastGreenY][0])
            self.hunger += LYNX_HUNGER_LOSS
            self.reproductive_need += LYNX_REPRODUCTIVE_FEELING_GAIN
            if terrain[self.x][self.y][0] >= 5:
                self.suffocation -= SUFFOCATION_LOSS
            else:
                self.suffocation += SUFFOCATION_GAIN
            self.goTo(self.lastGreenX, self.lastGreenY, terrain)
        else:

            #Check map with vision_field
            has_hunger = self.hunger > LYNX_HUNGER_FEELING_LIMIT
            want_reproduction = self.reproductive_need > REPRODUCTIONH_FEELING_LIMIT
            vision_scan, nearest_coord = NADA, (None, None)
            dist = None
            mountain = False
            if terrain[self.x][self.y][0] >= 5:
                mountain = True

            for i in range(self.x - self.vision_field,
                           self.x + self.vision_field):
                if i >= 0 and i<(HEIGTH/H_FACTOR):
                    for j in range(self.y - self.vision_field,
                                   self.y + self.vision_field):
                        if j >= 0 and j<(HEIGTH/H_FACTOR):
                            if not (i == self.x and
                                    j == self.y):  #no nos evaluamos a nosotros mismos
                                try:
                                    auxDist = Funciones.dist((i, j), (self.x, self.y))

                                    if mountain:
                                        if terrain[i][j][0] < 5:
                                            self.lastGreenX = i
                                            self.lastGreenY = j
                                    else:
                                        if terrain[i][j][0] >= 5:
                                            self.lastMountainX = i
                                            self.lastMountainY = j


                                    rabbit_set = {CONEJO, ZANAHORIA_CONEJO, CONEJO_CONEJO, CONEJO_REPRODUCCION}
                                    terrain_obj = terrain[i][j][1]
                                    if terrain_obj in rabbit_set:
                                        if vision_scan == CONEJO and has_hunger:
                                            if auxDist < dist:
                                                dist = auxDist
                                                nearest_coord = (i, j)
                                        else:
                                            vision_scan, nearest_coord = CONEJO, (i, j)
                                            dist = auxDist

                                    elif vision_scan != CONEJO and terrain_obj == CONEJO_LINCE and \
                                            self.hunger * self.risk_aversion < ATTACK_LIMIT and has_hunger:
                                        if vision_scan == CONEJO_LINCE:
                                            if auxDist < dist:
                                                dist = auxDist
                                                nearest_coord = (i, j)
                                        else:
                                            vision_scan, nearest_coord = CONEJO_LINCE, (
                                                i, j)
                                            dist = auxDist

                                    elif vision_scan != CONEJO and vision_scan != CONEJO_LINCE and want_reproduction and \
                                            terrain_obj == LINCE:
                                        if vision_scan == LINCE:
                                            if auxDist < dist:
                                                dist = auxDist
                                                nearest_coord = (i, j)
                                        else:
                                            vision_scan, nearest_coord = LINCE, (i, j)
                                            dist = auxDist
                                except IndexError:
                                    pass

            #veredicto final vision_scan
            if vision_scan == NADA:
                if terrain[self.x][self.y][1] < 5 and has_hunger:
                    self.flee(self.lastMountainX, self.lastMountainY, terrain)
                else:
                    self.moveRandom(terrain)
            else:
                if vision_scan == CONEJO_LINCE:
                    self.wants_fight = True
                elif vision_scan == LINCE:
                    self.wants_reproduction = True
                self.goTo(nearest_coord[0], nearest_coord[1],
                          terrain)  #vamos a comer o reproducirnos

            #Sumamos el hambre
            self.hunger += LYNX_HUNGER_LOSS
            self.reproductive_need += LYNX_REPRODUCTIVE_FEELING_GAIN
            if terrain[self.x][self.y][0] >= 5:
                self.suffocation -= SUFFOCATION_LOSS
            else:
                self.suffocation += SUFFOCATION_GAIN

    def move(self, diffX, diffY, terrain):
        lynx_possibilities = {NADA, CONEJO, ZANAHORIA_CONEJO, ZANAHORIA,
                                       CONEJO_REPRODUCCION, CONEJO_CONEJO,PELEA_CONEJO,
                                       LINCE}
        absDiffX = 0 if diffX == 0 else diffX // abs(diffX)
        absDiffY = 0 if diffY == 0 else diffY // abs(diffY)
        if (self.x + absDiffX) < 0 or (self.x + absDiffX) >= (WIDTH/W_FACTOR):
            absDiffX = 0
        if (self.y + absDiffY) < 0 or (self.y + absDiffY) >= (HEIGTH/H_FACTOR):
            absDiffY = 0
        if absDiffX != 0 or absDiffY != 0:  #Checking if there is movement
            if self.wants_fight:
                lynx_possibilities.add(CONEJO_LINCE)
                if terrain[self.x + absDiffX][self.y + absDiffY][1] not in lynx_possibilities:
                    diffSum = absDiffX + absDiffY
                    if diffSum == -1 or diffSum == 1:  #Moving in one axis
                        if absDiffX == 0:
                            if self.x < (HEIGTH/H_FACTOR)-1 and terrain[self.x + 1][self.y + absDiffY][1] in lynx_possibilities:
                                self.x += 1
                                self.y += absDiffY
                            elif self.x != 0 and terrain[self.x - 1][self.y + absDiffY][1] in lynx_possibilities:
                                self.x += -1
                                self.y += absDiffY
                        else:
                            if self.y < (HEIGTH/H_FACTOR)-1 and terrain[self.x + absDiffX][self.y + 1][1] in lynx_possibilities:
                                self.x += absDiffX
                                self.y += 1
                            elif self.y != 0 and terrain[self.x + absDiffX][self.y - 1][1] in lynx_possibilities:
                                self.x += absDiffX
                                self.y += -1
                    else:  # Moving in two axis
                        if terrain[self.x][self.y + absDiffY][1] in lynx_possibilities:
                            self.y += absDiffY
                        elif terrain[self.x +
                                     absDiffX][self.y][1] in lynx_possibilities:
                            self.x += absDiffX

                else:
                    self.x += absDiffX
                    self.y += absDiffY
            else:
                if terrain[self.x + absDiffX][self.y + absDiffY][1] not in lynx_possibilities:
                    diffSum = absDiffX + absDiffY
                    if diffSum == -1 or diffSum == 1:  #Moving in one axis
                        if absDiffX == 0:
                            if self.x < (HEIGTH/H_FACTOR)-1 and terrain[self.x + 1][self.y + absDiffY][1] in lynx_possibilities:
                                self.x += 1
                                self.y += absDiffY
                            elif self.x != 0 and terrain[self.x - 1][self.y + absDiffY][1] in lynx_possibilities:
                                self.x += -1
                                self.y += absDiffY
                        else:
                            if self.y < (HEIGTH/H_FACTOR)-1 and terrain[self.x + absDiffX][self.y + 1][1] in lynx_possibilities:
                                self.x += absDiffX
                                self.y += 1
                            elif self.y != 0 and terrain[self.x + absDiffX][self.y - 1][1] in lynx_possibilities:
                                self.x += absDiffX
                                self.y += -1
                    else:  # Moving in two axis
                        if terrain[self.x][self.y + absDiffY][1] in lynx_possibilities:
                            self.y += absDiffY
                        elif terrain[self.x + absDiffX][self.y][1] in lynx_possibilities:
                            self.x += absDiffX

                else:
                    self.x += absDiffX
                    self.y += absDiffY

            self.x = int(self.x%int(WIDTH/W_FACTOR))
            self.y = int(self.y%int(HEIGTH/H_FACTOR))

    def moveRandom(self, terrain):
        if self.x <= 0:
            random_eje_x = random.randint(0, 1)
        elif self.x >= (HEIGTH/H_FACTOR)-1:
            random_eje_x = random.randint(-1, 0)
        else:
            random_eje_x = random.randint(-1, 1)
        if self.y <= 0:
            random_eje_y = random.randint(0, 1)
        elif self.y >= (HEIGTH/H_FACTOR)-1:
            random_eje_y = random.randint(-1, 0)
        else:
            random_eje_y = random.randint(-1, 1)

        extra = EXTRA_STEP if self.strength_speed > random.random() else 0

        for _ in range(MOVES_PER_ACTION + extra + 1):
            diffX = random_eje_x
            diffY = random_eje_y

            self.move(diffX, diffY, terrain)

        self.display(terrain)

    def goTo(self, i, j, terrain):
        '''Función para ir a las coordenadas indicadas'''
        extra = EXTRA_STEP if self.strength_speed > random.random() else 0

        for _ in range(MOVES_PER_ACTION + extra + 1):
            diffX = i - self.x
            diffY = j - self.y

            self.move(diffX, diffY, terrain)

        # print(diffX, diffX, self.x, self.y)
        self.display(terrain)

    def reproduce(self, terrain, lynx_dict):

        aux_i = 0
        aux_j = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if terrain[(self.x+i)%int(WIDTH/W_FACTOR)][(self.y+j)%int(HEIGTH/H_FACTOR)][1] == NADA:
                    aux_i = i
                    aux_j = j
                    exit

        if aux_i != 0 or aux_j != 0:
            risk2, strength2 = lynx_reproduction_dict[str(self.x)+"-"+str(self.y)]
            risk_av_child, strength_speed_child = Funciones.cruce_and_mutate(self.risk_aversion, risk2, self.strength_speed, strength2)

            x_child = int((self.x+aux_i)%(WIDTH/W_FACTOR))
            y_child = int((self.y+aux_j)%(HEIGTH/H_FACTOR))
            aux_lynx = Lynx(terrain, x_child , y_child, risk_av_child, strength_speed_child)
            gv.lynx_dict[gv.lynx_id-1] = aux_lynx
            terrain[x_child][y_child][1] = LINCE

    def die(self, terrain, lynx_dict, mode):
        aux = terrain[self.x][self.y][1]

        if aux == LINCE:
            terrain[self.x][self.y][1] = NADA
        elif aux == CONEJO_LINCE:
            terrain[self.x][self.y][1] = CONEJO
        elif aux == ZANAHORIA_LINCE:
            terrain[self.x][self.y][1] = ZANAHORIA
        elif aux == LINCE_LINCE or aux == LINCE_REPRODUCCION or aux == PELEA_LINCE:
            terrain[self.x][self.y][1] = NADA

        gv.lynx_cont -= 1
        gv.lynx_df.loc[self.id-1] = [mode, self.strength_speed, self.risk_aversion, float(get_ticks() // 1000)]
        del gv.lynx_dict[self.id]

    def eat(self, terrain):
        self.eat_ticks += 1
        if self.eat_ticks == EAT_DELAY:
            self.eat_ticks = 0
            self.hunger -= HUNGER_QUENCH
            terrain[self.x][self.y][1] = LINCE  #solo estoy yo

    def flee(self, i, j, terrain):
        '''Función para huir de las coordenadas indicadas'''

        extra = EXTRA_STEP if self.strength_speed > random.random() else 0

        for _ in range(MOVES_PER_ACTION + extra):
            diffX = self.x - i
            diffY = self.y - j

            self.move(diffX, diffY, terrain)

        # print(diffX, diffX, self.x, self.y)
        self.display(terrain)


class Zanahoria():
    def __init__(self, terrain):
        '''
            Carrot class and generator. Carrots are only generated where the grass is lightGreen or green.
        '''

        carrotCondition = (terrain[:, :, 1] == 0) & (terrain[:, :, 0] >= 2) & (
            terrain[:, :, 0] <= 3)

        x, y = np.where(carrotCondition)

        i = random.randint(0, len(x)-1)

        random_pos = [x[i], y[i]]

        self.x = random_pos[0]
        self.y = random_pos[1]

        terrain[self.x][self.y][1] = ZANAHORIA
