import math
import random

import noise
import numpy as np
# import matplotlib.pyplot as plt

from main.generators.forest import constants


class ForestIslandGenerator:
    THRESHOLD = 0.6
    WATER_THRESHOLD = THRESHOLD + 0.05
    BEACH_THRESHOLD = THRESHOLD + 0.1
    FOREST_THRESHOLD = THRESHOLD + 0.26
    PERLIN_OCTAVES = 6
    PERLIN_PERSISTENCE = 0.5
    PERLIN_LACUNARITY = 2.05

    GRAD_SHRINK = 2.5

    MAX_BASE = 12000000

    WATER_SPACING = 1  # amount of water cells around island

    # warning: island is usually smaller then desired size
    def __init__(self, width, height, scale, grad=GRAD_SHRINK):
        self.width = width
        self.height = height
        self.scale = scale
        self.grad_shrink = grad

    '''
    def dump(self, world, name: str):
        blue = [65 / 255, 105 / 255, 225 / 255]
        beach = [238 / 255, 214 / 255, 175 / 255]
        forest = [34 / 255, 139 / 255, 34 / 255]
        taiga = [0 / 255, 100 / 255, 0 / 255]
        color_world = np.zeros(world.shape + (3,))
        for i in range(self.width):
            for j in range(self.height):
                if world[i][j] < self.WATER_THRESHOLD:
                    color_world[i][j] = blue
                elif world[i][j] < self.BEACH_THRESHOLD:
                    color_world[i][j] = beach
                elif world[i][j] < self.FOREST_THRESHOLD:
                    color_world[i][j] = forest
                else:
                    color_world[i][j] = taiga
        plt.imsave(os.path.join(name + ".png"), color_world)
    '''

    def map_bg_to_terrain(self, bg, island_w, island_h):
        res = {}
        for x in range(island_w):
            for y in range(island_h):
                if bg[(x, y)] == constants.BG_WATER:
                    val = constants.TERRAIN_INVISIBLE_WALL
                else:
                    val = constants.TERRAIN_EMPTY
                res[(x, y)] = val
        return res

    def convert_to_map_background(self, world):
        res = {}
        for x in range(self.width):
            for y in range(self.height):
                if world[x][y] < self.WATER_THRESHOLD:
                    val = constants.BG_WATER
                elif world[x][y] < self.BEACH_THRESHOLD:
                    val = constants.BG_SAND
                elif world[x][y] < self.FOREST_THRESHOLD:
                    val = constants.BG_GRASS
                else:
                    val = constants.BG_DARK_GRASS
                res[(x, y)] = val
        return res

    def shrink_to_island(self, map, water_spacing=WATER_SPACING):
        res, new_height = self.shrink_to_island_h(map)
        res, new_width = self.shrink_to_island_w(res, new_height)
        res = self.add_water_borders(res, new_width, new_height, water_spacing)
        return res, new_width + water_spacing * 2, new_height + water_spacing * 2

    def shrink_to_island_h(self, map):
        res = {}
        skipped_rows = 0
        for y in range(self.height):
            is_only_water = True
            tmp = {}
            for x in range(self.width):
                tmp[(x, y - skipped_rows)] = map[(x, y)]
                if map[x, y] != constants.BG_WATER:
                    is_only_water = False
            if not is_only_water:
                res.update(tmp)
            else:
                skipped_rows = skipped_rows + 1
        return res, self.height - skipped_rows

    def shrink_to_island_w(self, map, new_height):
        res = {}
        skipped_cols = 0
        for x in range(self.width):
            is_only_water = True
            tmp = {}
            for y in range(new_height):
                tmp[(x - skipped_cols, y)] = map[(x, y)]
                if map[x, y] != constants.BG_WATER:
                    is_only_water = False
            if not is_only_water:
                res.update(tmp)
            else:
                skipped_cols = skipped_cols + 1
        return res, self.width - skipped_cols

    def add_water_borders(self, map, new_width, new_height, water_spacing):
        res = {}
        for x in range(new_width):
            for y in range(new_height):
                res[(x + water_spacing, y + water_spacing)] = map[x, y]

        for x in range(0, new_width + water_spacing * 2):
            for y in range(0, water_spacing):
                res[(x, y)] = constants.BG_WATER
                res[(x, y + new_height + water_spacing)] = constants.BG_WATER
        for y in range(0, new_height + water_spacing * 2):
            for x in range(0, water_spacing):
                res[(x, y)] = constants.BG_WATER
                res[(x + new_width + water_spacing, y)] = constants.BG_WATER
        return res

    def generate_island(self, random_base=None):
        if random_base is None:
            random_base = random.randint(0, self.MAX_BASE)

        world = np.zeros((self.width, self.height))
        for x in range(self.width):
            for y in range(self.height):
                # todo: needs attention!!! replace with dividing by width and height???
                world[x][y] = 1 + noise.pnoise2(x / self.scale,
                                                y / self.scale,
                                                octaves=self.PERLIN_OCTAVES,
                                                persistence=self.PERLIN_PERSISTENCE,
                                                lacunarity=self.PERLIN_LACUNARITY,
                                                repeatx=self.MAX_BASE,
                                                repeaty=self.MAX_BASE,
                                                base=random_base)
        center_x, center_y = self.width // 2, self.height // 2

        circle_grad = np.zeros_like(world)
        for x in range(self.width):
            for y in range(self.height):
                distx = abs(x - center_x)
                disty = abs(y - center_y)
                dist = math.sqrt(distx * distx + disty * disty)
                circle_grad[x][y] = dist

        # get it between -1 and 1
        max_grad = np.max(circle_grad)
        circle_grad = circle_grad / max_grad
        circle_grad -= 0.5
        circle_grad *= 2.0

        min_depth = np.min(world)
        max_depth = np.max(world)
        circle_grad = circle_grad / ((max_depth - min_depth) * self.grad_shrink)
        world_with_gradient = np.zeros_like(world)
        for x in range(self.width):
            for y in range(self.height):
                world_with_gradient[x][y] = (world[x][y] - circle_grad[x][y])

        # get it between 0 and 1
        max_grad = np.max(world_with_gradient)
        world_with_gradient = world_with_gradient / max_grad
        return world_with_gradient
