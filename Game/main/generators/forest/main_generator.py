# one large island with beach, forest and taiga forest
import random

from main.generators.forest import island_generator, constants
from main.generators.forest import trees_generator


class ForestLocationGenerator:

    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.player_x = -1
        self.player_y = -1
        self.teleport_x = -1
        self.teleport_y = -1
        self.background = {}
        self.terrain = {}
        self.free_places = []  # array of points where player / monsters can be spawned

    def generate(self, island_random_base=None):
        self.generate_island(island_random_base, water_spacing=3)
        self.place_trees()
        self.update_free_places_array()

    # call only when free_places were updated
    def spawn_player(self):
        return random.choice(self.free_places)

    def generate_island(self, random_base=None, water_spacing=island_generator.ForestIslandGenerator.WATER_SPACING):
        generator = island_generator.ForestIslandGenerator(self.x_size, self.y_size, max(self.y_size, self.x_size))
        island = generator.generate_island(random_base)
        bg, island_w, island_h = generator.shrink_to_island(generator.convert_to_map_background(island), water_spacing)
        terrain = generator.map_bg_to_terrain(bg, island_w, island_h)
        # self.free_places = self.generate_free_places_array()
        self.background = bg
        self.terrain = terrain
        self.x_size = island_w
        self.y_size = island_h

    def place_trees(self):
        generator = trees_generator.ForestTreesGenerator(self.x_size, self.y_size)
        self.terrain = generator.place_trees(self.background, self.terrain)
        f = open("terrain.txt", "w")
        for x in range(self.x_size):
            row = ""
            for y in range(self.y_size):
                if (x, y) in self.terrain:
                    row = row + self.terrain[(x, y)]
                else:
                    row = row + " "
            row = row + "\n"
            f.write(row)
        f.close()

        f = open("background.txt", "w")
        for x in range(self.x_size):
            row = ""
            for y in range(self.y_size):
                if (x, y) in self.background:
                    row = row + self.background[(x, y)]
                else:
                    row = row + " "
            row = row + "\n"
            f.write(row)
        f.close()

    def update_free_places_array(self):
        self.free_places = []
        for x in range(self.x_size):
            for y in range(self.y_size):
                if self.terrain[(x, y)] == constants.TERRAIN_EMPTY:
                    self.free_places.append((x, y))
