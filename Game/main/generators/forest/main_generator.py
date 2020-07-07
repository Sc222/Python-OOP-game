# one large island with beach, forest and taiga forest
import random

from main.generators.forest import island_generator, constants
from main.generators.forest import trees_generator
from main.generators.forest.ponds_generator import PondsGenerator


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
        self.free_places = {}  # dictionary of free map points BY BACKGROUND (sand, forest, etc)

    def generate(self, island_random_base=None):
        self.generate_island(island_random_base, water_spacing=3)
        self.place_trees()
        self.update_free_places()
        self.generate_ponds()
        self.update_free_places()
        #todo !!!generate ponds!!!


    # call only when free_places were updated
    # location is same thing as background element
    def spawn_player(self, location=None):
        if location is None:
            location = random.choice(constants.SPAWN_LOCATIONS)
        return random.choice(self.free_places[location])

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

    def generate_ponds(self):
        #generator = PondsGenerator(self.x_size, self.y_size,self.free_places)
        #generator.generate_ponds()
        pass

    def update_free_places(self):
        for x in range(self.x_size):
            for y in range(self.y_size):
                if self.terrain[(x, y)] == constants.TERRAIN_EMPTY:
                    if not self.background[(x, y)] in self.free_places:
                        self.free_places[self.background[(x, y)]]=[]
                    else:
                        self.free_places[self.background[(x, y)]].append((x, y))
