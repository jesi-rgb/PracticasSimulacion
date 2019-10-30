import Clases
from TerrainGenerator import Terrain

terrain = Terrain((800, 800), 500.0, 6, 0.45, 2)
terrain.add_color()

rabo = Clases.Rabbit()

rabo.display_rabbit(terrain.world, 200, 200)

terrain.display_world()