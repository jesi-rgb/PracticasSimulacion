# import the pygame module, so you can use it
import pygame
from TerrainGenerator import Terrain
import Clases
import time, random, numpy as np


# define a main function
def main():
    width, height = 800, 800

    terrain = Terrain((width, height), 500.0, 6, 0.45, 2)
    terrain.add_color()

    clock = pygame.time.Clock()

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Proyecto Simulacion")

    screen = pygame.display.set_mode((width, height))

    rabo = Clases.Rabbit()
    running = True
    zanahorias = []

    while running:

        if random.random() < .4:
            zanahorias.append(Clases.Zanahoria())

        for z in zanahorias:
            z.display(terrain.manipulable_world)

        # conejo se mueve en manipulable world
        rabo.goTo(200, 200)
        rabo.display(terrain.manipulable_world)

        # generamos terrain.world from manipulable world
        terrain.recalculate_world()

        # generamos la imagen y la updateamos
        image = pygame.image.frombuffer(terrain.world, (width, height), "RGB")

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


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
