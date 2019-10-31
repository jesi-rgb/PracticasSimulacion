import math


def dist(position, target):
    '''Devuelve la distancia euclidea de las dos coordenadas'''
    return math.sqrt((position[0] - target[0])**2 +
                     (position[1] - target[1])**2)


def nextTime(rabbit_list, lynx_list):
    pass