# import the pygame module, so you can use it
import pygame
from TerrainGenerator import Terrain
import Clases
import time, random, numpy as np


# define a main function
def main():
    width, height = 800, 800
    w_factor = 4
    h_factor = 4

    terrain = Terrain((width // w_factor, height // h_factor), 100.0, 22.55,
                      89.55, 6, 0.45, 2)
    terrain.add_color()
    print("World size: ", width // w_factor, height // h_factor)

    clock = pygame.time.Clock()

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Proyecto Simulacion")

    screen = pygame.display.set_mode((width, height))

    rabo = Clases.Rabbit()
    running = True
    zanahorias = []
    down_pressed = None

    while running:

        if random.random() < 4:
            zanahorias.append(Clases.Zanahoria(terrain.manipulable_world))

        # for z in zanahorias:
        #     z.display(terrain.manipulable_world)

        # conejo se mueve en manipulable world
        rabo.action(terrain.manipulable_world)
        # rabo.goTo(200, 200, terrain.manipulable_world)

        # generamos terrain.world from manipulable world
        terrain.recalculate_world()

        # generamos la imagen y la updateamos
        image = pygame.image.frombuffer(
            terrain.world, (width // w_factor, height // h_factor), "RGB")
        image = pygame.transform.scale(image, (width, height))

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
