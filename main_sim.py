# import the pygame module, so you can use it
import pygame
from TerrainGenerator import Terrain
import Clases
import time, random, numpy as np
import matplotlib.pyplot as plt
import global_variables as gv

from Funciones import HEIGTH, W_FACTOR, WIDTH, H_FACTOR

plt.style.use('ggplot')
xs = np.linspace(0,1,101)[0:-1]
ys = np.zeros_like(xs)

def live_plotter(x_vec,y1_data,line1,identifier='',pause_time=0.01):
    if line1==[]:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,alpha=0.8)        
        #update plot label/title
        plt.ylabel('Y Label')
        # plt.ylim(top=rabbit_cont + 20)
        plt.title('Title: {}'.format(identifier))
        plt.show()
        
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1

def simulation_analysis():
    print('\n\nSimulation analysis:\n')
    print(gv.rabbit_df.describe())

    plt.close()
    plt.ioff()
    plt.figure(figsize=(5, 5))
    plt.plot(gv.rabbit_df.Age, gv.rabbit_df.Speed, alpha=0.8)        
    plt.ylabel('Speed value')
    plt.title('Speed evolution')
    plt.show()


# define a main function
def main():
    global ys, xs

    terrain = Terrain((WIDTH // W_FACTOR, HEIGTH // H_FACTOR), 100.0, 22.55,
                      89.55, 6, 0.45, 2)
    terrain.add_color()
    print("World size: ", WIDTH // W_FACTOR, HEIGTH // H_FACTOR)

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Proyecto Simulacion: Modelo Evolutivo")

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


    running = True
    down_pressed = None
    sample_time = 20

    line1 = []
    plt.ion()

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
        
        # para el live plotting de las estadísticas
        ys[-1] = int(gv.rabbit_cont)
        np.append(xs, int(pygame.time.get_ticks() // 1000))
        line1 = live_plotter(xs,ys,line1, 'Rabbit count')
        ys = np.append(ys[1:],0.0)

    

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
    simulation_analysis()
