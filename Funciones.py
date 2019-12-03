import math
import random

WIDTH, HEIGTH = 800, 800
W_FACTOR = 4
H_FACTOR = 4

def dist(position, target):
    '''Devuelve la distancia euclidea de las dos coordenadas'''
    return math.sqrt((position[0] - target[0])**2 +
                     (position[1] - target[1])**2)

def cruce_and_mutate(risk_av1, risk_av2, strength_spe1, strength_spe2):
    #Cruce
    percentaje_risk = random.random()
    risk_av = risk_av1*percentaje_risk + risk_av2*(1-percentaje_risk)

    percentaje_strenth_spe = random.random()
    strength_spe = strength_spe1*percentaje_strenth_spe + strength_spe2*(1-percentaje_strenth_spe)

    #Mutación
    if random.random() < 0.005:
        risk_av = random.random()
    if random.random() < 0.005:
        strength_spe = random.random()


    return risk_av, strength_spe