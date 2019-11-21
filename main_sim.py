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
rabbit_data = np.zeros_like(xs)
lynx_data = np.zeros_like(xs)
final_graph_r = np.array([0])
final_graph_l = np.array([0])
final_graph_x = np.array([0])


def live_plotter(x_vec, y1_data, y2_data, line1, line2, identifier='', pause_time=0.01):
    if line1==[] and line2 == []:
        # this is the call to matplotlib that allows dynamic plotting
        plt.ion()
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        # create a variable for the line so we can later update it
        line1, = ax.plot(x_vec,y1_data,alpha=0.8)        
        #update plot label/title
        plt.ylabel('Conejos')
        # plt.ylim(top=rabbit_cont + 20)
        plt.title(identifier)

        ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
        color = [0, 0, 0]
        ax2.set_ylabel('Linces', color=color)  # we already handled the x-label with ax1
        line2, = ax2.plot(x_vec, y2_data, color=color, alpha=0.5)
        ax2.tick_params(axis='y', labelcolor=color)

        plt.show()
        
    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    line2.set_ydata(y2_data)
    # adjust limits if new data goes beyond bounds
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data),np.max(y1_data)+np.std(y1_data)])
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1, line2

def simulation_analysis():
    print('\n\nSimulation analysis:\n')
    print(gv.rabbit_df.describe())

    plt.close()
    plt.ioff()
    plt.figure(figsize=(5, 5))
    x = np.arange(len(rabbit_data[:-1]))
    plt.plot(final_graph_x[:-1], final_graph_r[:-1], final_graph_x[:-1], final_graph_l[:-1])    
    plt.legend(['Rabbits', 'Lynxes'])  
    plt.ylabel('Number of entities')
    plt.title('Population evolution')
    plt.show()


# define a main function
def main():
    global rabbit_data, lynx_data, xs, final_graph_l, final_graph_r, final_graph_x

    terrain = Terrain((WIDTH // W_FACTOR, HEIGTH // H_FACTOR), 100.0, 22.55,
                      89.55, 6, 0.45, 2)
    terrain.add_color()
    print("World size: ", WIDTH // W_FACTOR, HEIGTH // H_FACTOR)

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Proyecto Simulacion: Modelo Evolutivo")

    screen = pygame.display.set_mode((WIDTH, HEIGTH))

    for _ in range(200):
        gv.rabbit_dict[gv.rabbit_id-1] = Clases.Rabbit(terrain.manipulable_world)

    for _ in range(100):
        gv.lynx_dict[gv.lynx_id-1] = Clases.Lynx(terrain.manipulable_world)

    running = True
    down_pressed = None
    sample_time = 20

    line1 = []
    line2 = []
    plt.ion()

    while running:

        if random.random() < 5:
            Clases.Zanahoria(terrain.manipulable_world)

        rabbits = list(gv.rabbit_dict.values())
        if len(rabbits) == 0:
            running = False
        for x in rabbits:
            x.action(terrain.manipulable_world, gv.rabbit_dict)

        lynxes = list(gv.lynx_dict.values())
        for x in lynxes:
            x.action(terrain.manipulable_world, gv.lynx_dict)


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
        rabbit_data[-1] = int(gv.rabbit_cont)
        lynx_data[-1] = int(gv.lynx_cont)

        final_graph_l = np.append(final_graph_l, int(gv.lynx_cont))
        final_graph_r = np.append(final_graph_r, int(gv.rabbit_cont))
        final_graph_x = np.append(final_graph_x, int(pygame.time.get_ticks() // 1000))

        # np.append(xs, int(pygame.time.get_ticks() // 1000))
        line1, line2 = live_plotter(xs, rabbit_data, lynx_data, line1, line2, 'Contador Conejos vs Linces')
        rabbit_data = np.append(rabbit_data[1:], 0.0)
        lynx_data = np.append(lynx_data[1:], 0.0)
        

    

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
    simulation_analysis()
