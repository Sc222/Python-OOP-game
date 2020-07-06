import random

import numpy as np
from noise import pnoise2

from main.generators.forest import constants


class ForestTreesGenerator:
    PERLIN_OCTAVES = 6
    PERLIN_PERSISTENCE = 0.5
    PERLIN_LACUNARITY = 2.1
    MAX_BASE = 12000000
    SCALE = 50  # todo find better value if works bad
    GRASS_COLOR = [34 / 255, 139 / 255, 34 / 255]
    TREE_COLOR = [0 / 255, 100 / 255, 0 / 255]

    def __init__(self, width, height, scale=SCALE):
        self.width = width
        self.height = height
        self.scale = scale

    def place_trees(self, background, terrain, random_base=None):
        if random_base is None:
            random_base = random.randint(0, self.MAX_BASE)
        res = {}
        res.update(terrain)
        blue_noise = np.zeros((self.width, self.height))
        # trees_map = np.zeros(blue_noise.shape + (3,))
        for x in range(self.width):
            for y in range(self.height):
                nx = x / self.width - 0.5
                ny = y / self.height - 0.5
                blue_noise[x][y] = pnoise2(self.SCALE * nx, self.SCALE * ny,
                                           octaves=self.PERLIN_OCTAVES,
                                           persistence=self.PERLIN_PERSISTENCE,
                                           lacunarity=self.PERLIN_LACUNARITY,
                                           repeatx=self.MAX_BASE,
                                           repeaty=self.MAX_BASE,
                                           base=random_base)

        for x in range(self.width):
            for y in range(self.height):
                max = 0
                radius = constants.TREE_RADIUS_BY_BG[background[(x, y)]]
                if radius is None:  # skip water location
                    continue
                for y_n in range(y - radius, y + radius + 1):
                    for x_n in range(x - radius, x + radius + 1):
                        if 0 <= y_n < self.height and 0 <= x_n < self.width:
                            e = blue_noise[x_n][y_n]
                            if e > max:
                                max = e
                if blue_noise[x][y] == max and background[(x,y)] is not constants.BG_WATER:
                    res[(x, y)] = random.choice(constants.TREES_BY_BG[background[(x, y)]])
        return res
        # plt.imsave(os.path.join("output", "trees", f"base:{base} scale: {SCALE}.png"), trees_map)
