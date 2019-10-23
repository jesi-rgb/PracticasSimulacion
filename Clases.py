class Animal:

	def __init__(self):
		self.strength_speed = 0
		self.reproductive_need = 0
		self.vision_fiel = 0
		self.hunger = 0
		self.risk_aversion = 0
		self.racionality = 0
		self.max_time_alive = 100		
		self.time_alive = 0
        
class Rabbit(Animal):
    
    def __init__(self):
        Animal.__init__(self)
        
        
class Lynx(Animal):
    
    def __init__(self):
        Animal.__init__(self)
        self.suffocation = 0