HUNGER_LOSS = 0.01
HUNGER_FEELING_LIMIT = 0.5
REPRODUCTIONH_FEELING_LIMIT = 0.5
ATTACK_LIMIT = 0.1
MIN_SPEED = 5
MAX_SPEED = 20
EAT_DELAY = 3 #ticks
HUNGER_QUENCH = 0.3
MOVES_PER_ACTION = 2
EXTRA_STEP = 1
numero_random_que_borraremos = 2

#CASILLAS
NADA = 0
CONEJO = 1
ZANAHORIA_CONEJO = 2
ZANAHORIA = 3
PELEA_CONEJO = 4
PELEA_LINCE = 5
LINCE = 6
ZANAHORIA_LINCE = 7
CONEJO_LINCE = 8

import Funciones

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
        self.x = 0
        self.y = 0

    def action(self, terrain):
        self.hunger += HUNGER_LOSS
        if self.hunger == 1:
            pass #Die



class Rabbit(Animal):
    
    def __init__(self):
        Animal.__init__(self)

    def action(self, terrain):
        '''Función para calcular nuestra siguiente acción.'''


        Animal.action(terrain)

        #Check map with vision_field
        has_hunger = self.hunger < HUNGER_FEELING_LIMIT
        want_reproduction = self.reproductive_need < REPRODUCTIONH_FEELING_LIMIT
        vision_scan, nearest_coord = NADA, (None, None)
        dist = None
        for i in range(self.x - self.vision_field, self.x + self.vision_field):
            for j in range(self.x - self.vision_field, self.x + self.vision_field):
                
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
                elif vision_scan < LINCE and has_hunger and terrain[i][j][0] == ZANAHORIA:
                    if vision_scan == ZANAHORIA:
                        auxDist = Funciones.dist((i, j), (self.x, self.y))
                        if auxDist < dist:
                            dist = auxDist
                            nearest_coord = (i, j)
                    else:
                        vision_scan, nearest_coord = ZANAHORIA, (i, j)
                        dist = Funciones.dist((self.x, self.y), (i, j))

                elif vision_scan < ZANAHORIA and terrain[i][j][0] == ZANAHORIA_CONEJO and self.hunger*self.risk_aversion < ATTACK_LIMIT:
                    if vision_scan == ZANAHORIA_CONEJO:
                        auxDist = Funciones.dist((i, j), (self.x, self.y))
                        if auxDist < dist:
                            dist = auxDist
                            nearest_coord = (i, j)
                    else:
                        vision_scan, nearest_coord = ZANAHORIA_CONEJO, (i, j)
                        dist = Funciones.dist((self.x, self.y), (i, j))
                    
                elif vision_scan < ZANAHORIA_CONEJO and want_reproduction and terrain[i][j][0] == 2:
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
                pass #nos movemos random e inteligentemente
            else:
                self.goTo(nearest_coord[0], nearest_coord[1]) #vamos a comer o follar


        def move(self, diffX, diffY):
            if diffX != 0 or diffY != 0: #Cheking if there is movement

                absDiffX = 0 if diffX==0 else diffX/abs(diffX)
                absDiffY = 0 if diffY==0 else diffY / abs(diffY)
                if terrain[self.x+absDiffX][self.y+absDiffY][0] > 3:
                    diffSum = absDiffX + absDiffY
                    if diffSum == -1 or diffSum == 1: #Moving in one axis
                        if absDiffX == 0:
                            if terrain[self.x+1][self.y+absDiffY][0] <= 3:
                                self.x += 1
                                self.y += absDiffY
                            elif terrain[self.x-1][self.y+absDiffY][0] <= 3:
                                self.x += -1
                                self.y += absDiffY
                        else:
                            if terrain[self.x][self.y+absDiffY+1][0] <= 3:
                                self.x += absDiffX
                                self.y += 1
                            elif terrain[self.x][self.y+absDiffY-1][0] <= 3:
                                self.x += absDiffX
                                self.y += -1
                    else: # Moving in two axis
                        if terrain[self.x][self.y+absDiffY][0] <= 3:
                            self.y += absDiffY
                        elif terrain[self.x+absDiffX][self.y][0] <= 3:
                            self.x += absDiffX

                else:
                    self.x += absDiffX
                    self.y += absDiffY



    def goTo(self, i, j):
        '''Función para ir a las coordenadas indicadas'''

        extra = EXTRA_STEP if self.strength_speed > numero_random_que_borraremos else 0

        for _ in range(MOVES_PER_ACTION+extra):
            diffX = i - self.x
            diffY = j - self.j

            self.move(diffX, diffY)

    def flee(self, i, j):
        '''Función para huir de las coordenadas indicadas'''


        diffX = (self.x - i) * (MOVES_PER_ACTION+EXTRA_STEP)
        diffY = (self.y - j) * (MOVES_PER_ACTION+EXTRA_STEP)

        self.goTo(i + diffX, j + diffY)

    def eat(self, terrain):
        #pasan los ticks de comer
        self.hunger -= HUNGER_QUENCH
        terrain[self.x][self.y] = CONEJO #solo estoy yo


    def attack(self):
        pass

    def reproduce(self):
        pass


        
        
class Lynx(Animal):
    
    def __init__(self):
        Animal.__init__(self)
        self.suffocation = 0

