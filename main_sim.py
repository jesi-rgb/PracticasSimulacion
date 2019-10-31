# import the pygame module, so you can use it
import pygame
from TerrainGenerator import Terrain
import Clases
import time


# define a main function
def main():
    width, height = 800, 800

    terrain = Terrain((width, height), 500.0, 6, 0.45, 2)
    terrain.add_color()

    clock = pygame.time.Clock()

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Proyecto Simulacion")

    screen = pygame.display.set_mode((width, height))

    rabo = Clases.Rabbit()
    running = True

    while running:
        # event handling, gets all event from the event queue

        # conejo se mueve en manipulable world
        rabo.goTo(110, 110)
        rabo.display_rabbit(terrain.manipulable_world)

        # generamos terrain.world from manipulable world
        terrain.recalculate_world()

        # generamos la imagen y la updateamos
        image = pygame.image.frombuffer(terrain.world, (width, height), "RGB")

        screen.blit(image, (0, 0))
        pygame.display.update()

        terrain.reset_worlds()

        time.sleep(.033)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN
                                             and event.key == pygame.K_ESCAPE):
                running = False


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
