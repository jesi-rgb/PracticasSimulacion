# import the pygame module, so you can use it
import pygame
from TerrainGenerator import Terrain
import Clases
import time, random, numpy as np

from Funciones import HEIGTH, W_FACTOR, WIDTH, H_FACTOR

# define a main function
def main():

    terrain = Terrain((WIDTH // W_FACTOR, HEIGTH // H_FACTOR), 100.0, 22.55,
                      89.55, 6, 0.45, 2)
    terrain.add_color()
    print("World size: ", WIDTH // W_FACTOR, HEIGTH // H_FACTOR)

    clock = pygame.time.Clock()

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Proyecto Simulacion")

    screen = pygame.display.set_mode((WIDTH, HEIGTH))

    rabbit_dict = dict()
    rabbit_cont = 0

    lynx_dict = dict()
    lynx_cont = 0

    for _ in range(10):
        rabbit_dict[rabbit_cont] = Clases.Rabbit(terrain.manipulable_world)
        rabbit_cont+=1

    for _ in range(10):
        lynx_dict[lynx_cont] = Clases.Lynx(terrain.manipulable_world)
        lynx_cont+=1

    # rabo = Clases.Rabbit(40, 40)
    # rabbit_dict[rabbit_cont] = rabo
    # rabbit_cont+=1
    # rabo2 = Clases.Rabbit(35, 35)
    # rabbit_dict[rabbit_cont] = rabo2

    running = True
    down_pressed = None

    while running:
        if random.random() < 0.1:
            Clases.Zanahoria(terrain.manipulable_world)

        # conejo se mueve en manipulable world
        rabbits = list(rabbit_dict.values())
        # if len(rabbits) == 0:
        #     running = False
        for x in rabbits:
            x.action(terrain.manipulable_world, rabbit_dict)

        lynxes = list(lynx_dict.values())
        # if len(lynxes) == 0:
        #     running = False
        for x in lynxes:
            x.action(terrain.manipulable_world, lynx_dict)


        # generamos terrain.world from manipulable world
        terrain.recalculate_world()

        # generamos la imagen y la updateamos
        image = pygame.image.frombuffer(
            terrain.world, (WIDTH // W_FACTOR, HEIGTH // H_FACTOR), "RGB")
        image = pygame.transform.scale(image, (WIDTH, HEIGTH))

        # finalmente, reproducimos la nueva imagen
        screen.blit(image, (0, 0))
        pygame.display.update()

        # reseteamos los mundos para la siguiente iteración
        terrain.reset_worlds()

        # rutina para poder salir de la aplicación
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                             and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    down_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    down_pressed = False

        if down_pressed:
            time.sleep(.33)


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
