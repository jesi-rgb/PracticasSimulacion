# import the pygame module, so you can use it
import pygame
from TerrainGenerator import Terrain
import Clases
import numpy as np
import matplotlib.pyplot as plt
import global_variables as gv

from Funciones import HEIGTH, W_FACTOR, WIDTH, H_FACTOR

initial_rabbits = 150
initial_lynxes = 40

xs = np.linspace(0,1,101)[0:-1]
rabbit_data = np.zeros_like(xs) 
lynx_data = np.zeros_like(xs) 
final_graph_r = np.array([initial_rabbits])
final_graph_l = np.array([initial_lynxes])
final_graph_speed_r = np.array([])
final_graph_speed_l = np.array([])
final_graph_risk_r = np.array([])
final_graph_risk_l = np.array([])
final_graph_x = np.array([0])
final_graph_rain = np.array([])

ax = plt.figure(figsize=(6, 5)).add_subplot(111)
ax2 = ax.twinx()


def live_plotter(x_vec, y1_data, y2_data, line1, line2, identifier='', pause_time=0.01):

    global ax, ax2

    if line1==[] and line2 == []:
        # create a variable for the line so we can later update it
        plt.ion()
        plt.title(identifier)

        
        ax.set_ylabel('Conejos', color='tab:blue')
        ax.set_ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])

        ax2.set_ylabel('Linces', color='tab:orange')
        ax2.set_ylim([np.min(y2_data) - np.std(y2_data), np.max(y2_data) + np.std(y2_data)])

        line1, = ax.plot(x_vec,y1_data, alpha=0.8, linewidth=2)    
        line2, = ax2.plot(x_vec, y2_data, color='tab:orange', alpha=0.8, linewidth=2)    

        plt.show()

    
    # after the figure, axis, and line are created, we only need to update the y-data
    line1.set_ydata(y1_data)
    line2.set_ydata(y2_data)

    # adjust limits if new data goes beyond bounds
    if np.min(y1_data) <= line1.axes.get_ylim()[0] or np.max(y1_data) >= line1.axes.get_ylim()[1]:
        ax.set_ylim([np.min(y1_data) - np.std(y1_data), np.max(y1_data) + np.std(y1_data)])

    if np.min(y2_data) <= line2.axes.get_ylim()[0] or np.max(y2_data) >= line2.axes.get_ylim()[1]:
        ax2.set_ylim([np.min(y2_data) - np.std(y2_data), np.max(y2_data) + np.std(y2_data)])
    
    
    # this pauses the data so the figure/axis can catch up - the amount of pause can be altered above
    plt.pause(pause_time)
    
    # return line so we can update it again in the next iteration
    return line1, line2

def simulation_analysis():
    print('\n\nSimulation analysis:\n')
    print(gv.rabbit_df.describe())

    plt.close()
    plt.ioff()
    filas, columnas = 2, 3

    # Gráfica de evolución de la población
    rx = plt.figure(figsize=(12, 7)).add_subplot(filas, columnas, 1)
    lx = rx.twinx()
    x = np.arange(len(rabbit_data[:-1]))
    

    rx.plot(final_graph_x[:-1], final_graph_r[:-1], linewidth=1.5, color='tab:blue')
    rx.set_ylabel('Conejos', color='tab:blue')   
    lx.plot(final_graph_x[:-1], final_graph_l[:-1], linewidth=1.5, color='tab:orange')
    lx.set_ylabel('Linces', color='tab:orange')

    plt.xlabel('Ticks de la simulación')
    plt.title('Evolución de la población')
    
    # Barras de muertes de conejos
    r_death_causes = gv.rabbit_df.groupby('Death_cause').count()

    plt.subplot(filas, columnas, 2)
    plt.bar(r_death_causes.index, height=r_death_causes.Speed, color=['tab:orange', 'tab:blue', 'forestgreen', 'gold'])
    plt.title('Cuenta de muertes en conejos')
    plt.ylabel('Número de muertes')

    
    # Barras de muertes de linces 
    l_death_causes = gv.lynx_df.groupby('Death_cause').count()

    plt.subplot(filas, columnas, 3)
    plt.bar(l_death_causes.index, height=l_death_causes.Speed, color=['tab:orange', 'tab:blue', 'forestgreen', 'gold'])
    plt.title('Cuenta de muertes en linces')
    plt.ylabel('Número de muertes')

    # Gráfica de lluvia
    plt.subplot(filas, columnas, 4)
    plt.plot(final_graph_x[:-1], final_graph_rain)
    plt.title('Momentos en los que ha llovido')
    plt.xlabel('Ticks del juego')


    # Gráfica de evolución de velocidad
    plt.subplot(filas, columnas, 5)

    plt.plot(final_graph_x[:-1], final_graph_speed_r, final_graph_x[:-1], final_graph_speed_l)
    plt.title('Evolución del gen Velocidad/Fuerza')
    plt.legend(['Conejos', 'Linces'])

    # Gráfica de evolución de velocidad
    plt.subplot(filas, columnas, 6)

    plt.plot(final_graph_x[:-1], final_graph_risk_r, final_graph_x[:-1], final_graph_risk_l)
    plt.title('Evolución del gen Aversión al riesgo')
    plt.legend(['Conejos', 'Linces'])


    plt.tight_layout()
    plt.show()




# define a main function
def main():
    global rabbit_data, lynx_data, xs, final_graph_l, final_graph_rain, final_graph_r, final_graph_x, final_graph_speed_l, final_graph_speed_r, final_graph_risk_r, final_graph_risk_l

    terrain = Terrain((WIDTH // W_FACTOR, HEIGTH // H_FACTOR), 100.0, 22.55,
                      89.55, 6, 0.45, 2)
    terrain.add_color()
    print("World size: ", WIDTH // W_FACTOR, HEIGTH // H_FACTOR)

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Proyecto Simulacion: Modelo Evolutivo")

    screen = pygame.display.set_mode((WIDTH, HEIGTH), flags=pygame.SRCALPHA)

    for _ in range(initial_rabbits):
        gv.rabbit_dict[gv.rabbit_id-1] = Clases.Rabbit(terrain.manipulable_world)

    for _ in range(initial_lynxes):
        gv.lynx_dict[gv.lynx_id-1] = Clases.Lynx(terrain.manipulable_world)

    for _ in range(50):
        Clases.Zanahoria(terrain.manipulable_world)

    running = True
    down_pressed = None
    raining = False
    carrot_probability = 0.3

    line1 = []
    line2 = []
    plt.ion()

    while running:

        if np.random.random() < 0.006:
            raining = not raining

        if raining:
            # carrot_probability = 0.8
            Clases.Zanahoria(terrain.manipulable_world)
            Clases.Zanahoria(terrain.manipulable_world)
            Clases.Zanahoria(terrain.manipulable_world)
        else:
            Clases.Zanahoria(terrain.manipulable_world)
            Clases.Zanahoria(terrain.manipulable_world)
        
        
        rabbits = list(gv.rabbit_dict.values())
        lynxes = list(gv.lynx_dict.values())
        
        if len(rabbits) == 0 or len(lynxes) == 0:
            running = False
        
        aux_mean_speed_r = np.array([])
        aux_mean_risk_r = np.array([])
        for x in rabbits:
            x.action(terrain.manipulable_world, gv.rabbit_dict)
            aux_mean_speed_r = np.append(aux_mean_speed_r, x.strength_speed)
            aux_mean_risk_r = np.append(aux_mean_risk_r, x.risk_aversion)

        final_graph_speed_r = np.append(final_graph_speed_r, np.mean(aux_mean_speed_r))
        final_graph_risk_r = np.append(final_graph_risk_r, np.mean(aux_mean_risk_r))


        aux_mean_speed_l = np.array([])
        aux_mean_risk_l = np.array([])
        for x in lynxes:
            x.action(terrain.manipulable_world, gv.lynx_dict)
            aux_mean_speed_l = np.append(aux_mean_speed_l, x.strength_speed)
            aux_mean_risk_l = np.append(aux_mean_risk_l, x.risk_aversion)

        final_graph_speed_l = np.append(final_graph_speed_l, np.mean(aux_mean_speed_l))
        final_graph_risk_l = np.append(final_graph_risk_l, np.mean(aux_mean_risk_l))

        # generamos terrain.world from manipulable world
        terrain.recalculate_world()

        # generamos la imagen y la updateamos
        image = pygame.image.frombuffer(
            terrain.world, (WIDTH // W_FACTOR, HEIGTH // H_FACTOR), "RGBA")
        image = pygame.transform.scale(image, (WIDTH, HEIGTH))

        # finalmente, reproducimos la nueva imagen
        screen.blit(image, (0, 0))

        if raining:
            screen.fill((0, 0, 100, 0.5), special_flags=pygame.BLEND_RGBA_ADD)
            final_graph_rain = np.append(final_graph_rain, 'Raining')
        else:
            final_graph_rain = np.append(final_graph_rain, 'Not Raining')

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

        line1, line2 = live_plotter(xs, rabbit_data, lynx_data, line1, line2, 'Contador Conejos vs Linces')
        rabbit_data = np.append(rabbit_data[1:], 0.0)
        lynx_data = np.append(lynx_data[1:], 0.0)

    

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
    simulation_analysis()