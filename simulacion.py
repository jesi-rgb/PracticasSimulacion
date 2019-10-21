# import the pygame module, so you can use it
import pygame

# define a main function
def main():
    x, y = 800, 600
    clock = pygame.time.Clock()

    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)


    # initialize the pygame module
    pygame.init()
    # load and set the logo
    # logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Proyecto Simulacion")
    # create a surface on screen that has the size of 240 x 180
    screen = pygame.display.set_mode((x, y))

    # define a variable to control the main loop
    running = True

    # main loop
    while running:
        # event handling, gets all event from the event queue
        if pygame.time.get_ticks() % 10 == 0:
            screen.fill(red)
        else:
            if pygame.time.get_ticks() % 10 == 10:
                screen.fill(green)
            else:
                if pygame.time.get_ticks() % 10 == 20:
                    screen.fill(blue)
        pygame.display.update()

        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
