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
        self.hunger += 0.01
        if self.hunger == 1:
            pass #Die

        #Check map with vision_field

        
class Rabbit(Animal):
    
    def __init__(self):
        Animal.__init__(self)
        
        
class Lynx(Animal):
    
    def __init__(self):
        Animal.__init__(self)
        self.suffocation = 0