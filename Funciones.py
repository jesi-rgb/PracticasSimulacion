import math


def dist(mySelf, target):
    '''Devuelve la distancia euclidea de las dos coordenadas'''
    return math.sqrt(
        pow((mySelf[0] - target[0]), 2) + pow((mySelf[1] - target[1]), 2))


def nextTime(rabbit_list, lynx_list):
    pass