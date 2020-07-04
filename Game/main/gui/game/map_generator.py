import random

from noise import pnoise2


class MapGenerator:

    def __init__(self, x_size, y_size):
        self.x_size = x_size
        self.y_size = y_size
        self.map = [[0 for x in range(x_size)] for y in range(y_size)]
        self.player_x = -1
        self.player_y = -1
        self.teleport_x = -1
        self.teleport_y = -1
        # print(self.map)

    def print_map(self):
        for row in self.map:
            print(row)

    def map_as_string(self):
        res = ""
        for row in self.map:
            for cell in row:
                res = res + str(cell)
            res = res + '\n'
        return res

    def spawn_player(self):
        print(random.randint(0, 1))

    def generate_trees(self,R,val):
        base = random.randint(0,100)
        blue_noise = [[0 for x in range(self.x_size)] for y in range(self.y_size)]
        for y in range(0,self.y_size):
            for x in range(0,self.x_size):
                nx = x / self.x_size - 0.5
                ny = y / self.y_size - 0.5
                blue_noise[y][x] = pnoise2(50 * nx, 50 * ny,base=base)

        for y in range(0, self.y_size):
            for x in range(0, self.x_size):
                max = 0
                for y_n in range(y-R,y+R+1):
                    for x_n in range(x - R, x + R + 1):
                        if 0 <= y_n < self.y_size and 0 <= x_n < self.x_size:
                            e = blue_noise[y_n][x_n]
                            if e > max:
                                max = e
                if blue_noise[y][x]==max:
                    self.map[y][x]=val
