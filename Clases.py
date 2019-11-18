HUNGER_LOSS = 0.005
HUNGER_FEELING_LIMIT = 0.3
REPRODUCTIONH_FEELING_LIMIT = 0.5
ATTACK_LIMIT = 0.1
MIN_SPEED = 5
MAX_SPEED = 20
EAT_DELAY = 2  #ticks
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

#Estructuras de datos
rabbit_fight_dict = dict()
rabbit_reproduction_dict = dict()
rabbit_cont = 0

# contadores de causas de muerte para estadísticas
rabbit_deaths_from_hunger = 0
rabbit_deaths_from_rabbit_fight = 0
rabbit_deaths_from_lynx_attack = 0
rabbit_deaths_from_max_time = 0  # muerte por viejo soba

lynx_deaths_from_hunger = 0
lynx_deaths_from_lynx_fight = 0
lynx_deaths_from_suffocation = 0
lynx_deaths_from_max_alive = 0

import Funciones
from PIL import Image
import numpy as np
import random
from Funciones import HEIGTH, W_FACTOR, WIDTH, H_FACTOR


class Animal:
    def __init__(self, id, x, y):

        #Survival attributes
        self.id = id
        self.hunger = 0
        self.strength_speed = 0
        self.reproductive_need = 0
        self.vision_field = 5
        self.risk_aversion = 0
        self.racionality = 0

        #Life attributes
        self.max_time_alive = 10000
        self.time_alive = 0

        #Map position
        self.x = x
        self.y = y

        self.lastX = self.x
        self.lastY = self.y

        self.wants_fight = False
        self.wants_reproduction = False

        self.eat_ticks = 0

    def move(self, diffX, diffY):
        if not (diffX == 0 or diffY == 0):
            self.x += int(diffX / abs(diffX))
            self.y += int(diffY / abs(diffY))
        else:
            self.x += 0
            self.y += 0


class Rabbit(Animal):
    def __init__(self, x, y):
        global rabbit_cont
        Animal.__init__(self, rabbit_cont, x, y)
        rabbit_cont += 1

    def display(self, terrain):
        '''Función para editar el valor x, y del mundo donde nos situamos ahora mismo'''
        if terrain[self.x][self.y][1] == ZANAHORIA_CONEJO:
            terrain[self.x][self.y][1] = PELEA_CONEJO
            rabbit_fight_dict[str(self.x) + "-" + str(
                self.y)] = self.strength_speed * numero_random_que_borraremos
        elif terrain[self.x][self.y][1] == ZANAHORIA:
            terrain[self.x][self.y][1] = ZANAHORIA_CONEJO
        elif terrain[self.x][self.y][1] == CONEJO and self.wants_reproduction:
            rabbit_reproduction_dict[str(self.x) + "-" +
                                     str(self.y)] = (self.strength_speed,
                                                     self.risk_aversion)
            terrain[self.x][self.y][1] = CONEJO_REPRODUCCION
        elif terrain[self.x][
                self.y][1] == CONEJO and not self.wants_reproduction:
            terrain[self.x][self.y][1] = CONEJO_CONEJO
        else:
            terrain[self.x][self.y][1] = CONEJO

        if not (self.x == self.lastX and self.y == self.lastY):

            if terrain[self.x][self.y][1] == ZANAHORIA_CONEJO:
                terrain[self.x][self.y][1] = PELEA_CONEJO
                rabbit_fight_dict[str(self.x) + "-" + str(
                    self.y
                )] = self.strength_speed * numero_random_que_borraremos
            elif terrain[self.x][self.y][1] == ZANAHORIA:
                terrain[self.x][self.y][1] = ZANAHORIA_CONEJO
            elif terrain[self.x][
                    self.y][1] == CONEJO and self.wants_reproduction:
                rabbit_reproduction_dict[str(self.x) + "-" +
                                         str(self.y)] = (self.strength_speed,
                                                         self.risk_aversion)
                terrain[self.x][self.y][1] = CONEJO_REPRODUCCION
            elif terrain[self.x][
                    self.y][1] == CONEJO and not self.wants_reproduction:
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

        # print('x', self.x, 'y', self.y)

    def action(self, terrain, rabbit_dict):
        '''Función para calcular nuestra siguiente acción.'''
        global rabbit_deaths_from_max_time
        global rabbit_deaths_from_rabbit_fight
        global rabbit_deaths_from_rabbit_fight
        global rabbit_deaths_from_hunger

        self.time_alive += 1
        if (self.time_alive == self.max_time_alive):
            rabbit_deaths_from_max_time += 1
            print('death max time alive', rabbit_deaths_from_max_time)
            self.die(terrain, rabbit_dict)

        if terrain[self.x][self.y][1] == ZANAHORIA_CONEJO:
            self.eat(terrain)

        elif terrain[self.x][self.y][
                1] == CONEJO_REPRODUCCION and self.reproductive_need < REPRODUCTIONH_FEELING_LIMIT:
            if rabbit_reproduction_dict[str(self.x) + "-" +
                                        str(self.y)] == None:
                terrain[self.x][self.y][1] == CONEJO_CONEJO
                self.reproductive_need = 1

            else:
                self.reproduce(terrain, rabbit_dict)
                rabbit_reproduction_dict[str(self.x) + "-" +
                                         str(self.y)] = None

        elif terrain[self.x][self.y][1] == PELEA_CONEJO:
            if rabbit_fight_dict[str(self.x) + "-" +
                                 str(self.y)] == None:  #Ganaste tu
                terrain[self.x][self.y][1] = ZANAHORIA_CONEJO
                self.eat(terrain)
                del rabbit_fight_dict[str(self.x) + "-" + str(self.y)]

            elif rabbit_fight_dict[str(self.x) + "-" +
                                   str(self.y)] == False:  #Gana el
                self.die(terrain, rabbit_dict)

                rabbit_deaths_from_rabbit_fight += 1
                print('death rabbit fight', rabbit_deaths_from_rabbit_fight)

                del rabbit_fight_dict[str(self.x) + "-" + str(self.y)]

            elif rabbit_fight_dict[str(self.x)+"-"+str(self.y)] \
                    > self.strength_speed * numero_random_que_borraremos: #El menor gana - Ganamos nosotros
                rabbit_fight_dict[str(self.x) + "-" + str(self.y)] = False
                self.eat(terrain)

            else:
                rabbit_fight_dict[str(self.x) + "-" +
                                  str(self.y)] = None  #Gana el
                self.die(terrain, rabbit_dict)

                rabbit_deaths_from_rabbit_fight += 1
                print('death rabbit fight', rabbit_deaths_from_rabbit_fight)

        elif terrain[self.x][self.y][1] == CONEJO_LINCE:
            pass

        elif self.hunger >= 1:
            # muerte por hambre
            rabbit_deaths_from_hunger += 1
            print('death from hunger', rabbit_deaths_from_hunger)

            self.die(terrain, rabbit_dict)
        else:
            if vision_scan == ZANAHORIA_CONEJO:
                self.wants_fight = True
            elif vision_scan == CONEJO:
                self.wants_reproduction = True
            self.goTo(nearest_coord[0], nearest_coord[1],
                      terrain)  #vamos a comer o reproducirnos

        else:
            #Check map with vision_field
            has_hunger = self.hunger > HUNGER_FEELING_LIMIT
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
                                    dist = Funciones.dist((self.x, self.y),
                                                          (i, j))

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
                                    vision_scan, nearest_coord = ZANAHORIA, (i,
                                                                             j)
                                    dist = Funciones.dist((self.x, self.y),
                                                          (i, j))

                            elif vision_scan < ZANAHORIA and terrain_obj == ZANAHORIA_CONEJO and\
                                    self.hunger * self.risk_aversion < ATTACK_LIMIT:
                                if vision_scan == ZANAHORIA_CONEJO:
                                    auxDist = Funciones.dist((i, j),
                                                             (self.x, self.y))
                                    if auxDist < dist:
                                        dist = auxDist
                                        nearest_coord = (i, j)
                                else:
                                    vision_scan, nearest_coord = ZANAHORIA_CONEJO, (
                                        i, j)
                                    dist = Funciones.dist((self.x, self.y),
                                                          (i, j))

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
                                    dist = Funciones.dist((self.x, self.y),
                                                          (i, j))
                        except IndexError:
                            pass

            #veredicto final vision_scan
            if vision_scan >= LINCE:
                self.flee(nearest_coord[0], nearest_coord[1])
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
            self.hunger += HUNGER_LOSS

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
        try:
            absDiffX = 0 if diffX == 0 else diffX // abs(diffX)
            absDiffY = 0 if diffY == 0 else diffY // abs(diffY)
            if (self.x + absDiffX) < 0 or (self.x + absDiffX) >= (WIDTH /
                                                                  W_FACTOR):
                absDiffX = 0
            if (self.y + absDiffY) < 0 or (self.y + absDiffY) >= (HEIGTH /
                                                                  H_FACTOR):
                absDiffY = 0
            if absDiffX != 0 or absDiffY != 0:  #Checking if there is movement
                if self.wants_fight:
                    if terrain[self.x + absDiffX][self.y +
                                                  absDiffY][1] > ZANAHORIA:
                        diffSum = absDiffX + absDiffY
                        if diffSum == -1 or diffSum == 1:  #Moving in one axis
                            if absDiffX == 0:
                                if self.x < (HEIGTH / H_FACTOR
                                             ) - 1 and terrain[self.x + 1][
                                                 self.y +
                                                 absDiffY][1] <= ZANAHORIA:
                                    self.x += 1
                                    self.y += absDiffY
                                elif self.x != 0 and terrain[self.x - 1][
                                        self.y + absDiffY][1] <= ZANAHORIA:
                                    self.x += -1
                                    self.y += absDiffY
                            else:
                                if self.y < (HEIGTH / H_FACTOR) - 1 and terrain[
                                        self.x + absDiffX][self.y +
                                                           1][1] <= ZANAHORIA:
                                    self.x += absDiffX
                                    self.y += 1
                                elif self.y != 0 and terrain[
                                        self.x + absDiffX][self.y -
                                                           1][1] <= ZANAHORIA:
                                    self.x += absDiffX
                                    self.y += -1
                        else:  # Moving in two axis
                            if terrain[self.x][self.y +
                                               absDiffY][1] <= ZANAHORIA:
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

            self.x = int(self.x % int(WIDTH / W_FACTOR))
            self.y = int(self.y % int(HEIGTH / H_FACTOR))
        except:
            import sys
            print(HEIGTH, WIDTH, H_FACTOR, W_FACTOR, self.x, self.y)
            type, value, traceback = sys.exc_info()
            print('Error opening %s: %s' % (value.filename, value.strerror))

    def goTo(self, i, j, terrain):
        '''Función para ir a las coordenadas indicadas'''
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
        self.eat_ticks += 1
        if self.eat_ticks == EAT_DELAY:
            self.eat_ticks = 0
            self.hunger -= HUNGER_QUENCH
            terrain[self.x][self.y][1] = CONEJO  #solo estoy yo

    def attack(self):
        pass

    def reproduce(self, terrain, rabbit_dict):
        print('reproducing...')
        #mutar y juntar con rabbit_reproduction_dict
        aux_i = 0
        aux_j = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if terrain[(self.x + i) %
                           int(WIDTH / W_FACTOR)][(self.y + j) % int(
                               HEIGTH / H_FACTOR)][1] == NADA:
                    aux_i = i
                    aux_j = j
                    exit

        if aux_i != 0 or aux_j != 0:
            rabbit_dict[rabbit_cont] = Rabbit(rabbit_cont, self.x + aux_i,
                                              self.y + aux_j)

        self.reproductive_need = 1

        global rabbit_cont
        if aux_i != 0 or aux_j != 0:
            aux_rabbit = Rabbit(int((self.x + aux_i) % (WIDTH / W_FACTOR)),
                                int((self.y + aux_j) % (HEIGTH / H_FACTOR)))
            rabbit_dict[rabbit_cont - 1] = aux_rabbit
            terrain[int((self.x + aux_i) % (WIDTH / W_FACTOR))][int(
                (self.y + aux_j) % (HEIGTH / H_FACTOR))][1] = CONEJO

    def die(self, terrain, rabbit_dict):
        aux = terrain[self.x][self.y][1]

        if aux == CONEJO:
            terrain[self.x][self.y][1] = NADA
        elif aux == ZANAHORIA_CONEJO:
            terrain[self.x][self.y][1] = ZANAHORIA
        elif aux == CONEJO_CONEJO or aux == CONEJO_REPRODUCCION:
            terrain[self.x][self.y][1] = CONEJO
        elif aux == CONEJO_LINCE:
            terrain[self.x][self.y][1] = LINCE
        elif aux == PELEA_CONEJO:
            terrain[self.x][self.y][1] = ZANAHORIA_CONEJO

        del rabbit_dict[self.id]


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
