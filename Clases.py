HUNGER_LOSS = 0.01
HUNGER_FEELING_LIMIT = 0.5
REPRODUCTIONH_FEELING_LIMIT = 0.5
ATTACK_LIMIT = 0.1

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
        Animal.action(terrain)

        #Check map with vision_field
        has_hunger = self.hunger < HUNGER_FEELING_LIMIT
        want_reproduction = self.reproductive_need < REPRODUCTIONH_FEELING_LIMIT
        for i in range(self.x - self.vision_field, self.x + self.vision_field):
            for j in range(self.x - self.vision_field, self.x + self.vision_field):
                if terrain[i][j] > 3:
                    pass #Hay un lince, huye
                elif has_hunger and terrain[i][j] == 1:
                    pass #Ve a comer zanahoria
                elif terrain[i][j] == 3 and self.hunger*self.risk_aversion < ATTACK_LIMIT:
                    pass #Ataca al conejo
                elif want_reproduction and terrain[i][j] == 2:
                    pass #A triscar

        
        
class Lynx(Animal):
    
    def __init__(self):
        Animal.__init__(self)
        self.suffocation = 0

# 0 = Nada
# 1 = Zanahoria
# 2 = Conejo
# 3 = Zanahoria-Conejo
# 4 = Lince
# 5 = Zanahoria-Lince
# 6 = Conejo-Lince