import os
from typing import AnyStr, List

import pygame


class Scroll:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class StaticDrawObject:
    def __init__(self, image, draw_x, draw_y):
        self.image = image  # устанавливаем имя
        self.draw_x = draw_x
        self.draw_y = draw_y

    def get_draw_coordinates(self, cam_scroll: Scroll):
        return self.draw_x + cam_scroll.x, self.draw_y + cam_scroll.y


def load_image(path):
    return pygame.image.load(path).convert_alpha()

def load_folder_images(path):
    """
    Загружает все картинки из папки.
    В папки не должно быть других файлов.
    """
    images = []
    for file_name in os.listdir(path):
        image = pygame.image.load(path + os.sep + file_name).convert_alpha()
        images.append(image)
    return images


class Resources:
    player = "player"
    backgrounds = ["grass", "pond_top", "pond_right", "pond_left", "pond_bottom"]
    terrain = ["house", "pine", "oak", "birch", "flower_purple", "fern", "bush"]
    player_anims_name = ["walk_front_","idle_front_"] # все папки должны иметь название ""+right
    bg_imgs = []
    terrain_imgs = []
    player_imgs = {}

    def __init__(self, directory):
        self.directory = directory
        self.load_backgrounds()
        self.load_terrain()
        self.load_player()

    def load_backgrounds(self):
        for background in self.backgrounds:
            path = os.path.join(self.directory, background) + ".png"
            self.bg_imgs.append(load_image(path))

    def load_terrain(self):
        for terrain_element in self.terrain:
            path = os.path.join(self.directory, terrain_element) + ".png"
            self.terrain_imgs.append(load_image(path))

    def load_player(self):
        for anim in self.player_anims_name:
            path = os.path.join(self.directory, self.player,anim)
            images_right = load_folder_images(path+"right")
            images_left = [pygame.transform.flip(image, True, False) for image in images_right]
            self.player_imgs[anim + "right"] = images_right
            self.player_imgs[anim+"left"]=images_left


class Parser:
    TILE_SIZE = 32
    TILE_SIZE_HALF = TILE_SIZE / 2
    TERRAIN_SHIFT = -6

    def parse_map_to_static_draw_objects(self, images, map, center_x, center_y, y_offset=0):
        result_ls = list()
        for row_nb, row in enumerate(map):  # draw surface
            for col_nb, tile in enumerate(row):
                tile = int(tile)
                if tile != 0:
                    tile_image = images[tile - 1]
                    cart_x = row_nb * self.TILE_SIZE_HALF
                    cart_y = col_nb * self.TILE_SIZE_HALF
                    iso_x = (cart_x - cart_y)
                    iso_y = (cart_x + cart_y) / 2
                    centered_x = center_x - self.TILE_SIZE_HALF + iso_x
                    centered_y = center_y / 2 - self.TILE_SIZE + iso_y + y_offset
                    result_ls.append(StaticDrawObject(tile_image, centered_x, centered_y))
        return result_ls
