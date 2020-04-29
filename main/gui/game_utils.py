import os
from typing import AnyStr, List

import pygame


class Camera:
    def __init__(self, width,height,x, y):
        self.width=width
        self.height=height
        self.x = x
        self.y = y


class StaticDrawObject:
    def __init__(self, image, draw_x, draw_y):
        self.image = image  # устанавливаем имя
        self.draw_x = draw_x
        self.draw_y = draw_y

    def get_draw_coordinates(self, cam_scroll: Camera):
        return self.draw_x + cam_scroll.x, self.draw_y + cam_scroll.y

    #def get_draw_coordinates(self, player_x,player_y):
    #    return self.draw_x -90+player_x, self.draw_y -60+ player_y


def load_image(path,scale):
    img =  pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))

def load_folder_images(path,scale):
    """
    Загружает все картинки из папки.
    В папки не должно быть других файлов.
    """
    images = []
    for file_name in os.listdir(path):
        img = pygame.image.load(path + os.sep + file_name).convert_alpha()
        images.append(pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale)))
    return images


class Resources:
    player = "player"
    backgrounds = ["grass", "pond_top", "pond_right", "pond_left", "pond_bottom"]
    terrain = ["house", "pine", "oak", "birch", "flower_purple", "fern", "bush"]
    player_anims_name = ["walk_front_","idle_front_"] # все папки должны иметь название ""+right
    bg_imgs = []
    terrain_imgs = []
    player_imgs = {}

    def __init__(self, directory,scale):
        self.directory = directory
        self.scale=scale
        self.load_backgrounds()
        self.load_terrain()
        self.load_player()

    def load_backgrounds(self):
        for background in self.backgrounds:
            path = os.path.join(self.directory, background) + ".png"
            self.bg_imgs.append(load_image(path,self.scale))

    def load_terrain(self):
        for terrain_element in self.terrain:
            path = os.path.join(self.directory, terrain_element) + ".png"
            self.terrain_imgs.append(load_image(path,self.scale))

    def load_player(self):
        for anim in self.player_anims_name:
            path = os.path.join(self.directory, self.player,anim)
            images_right = load_folder_images(path+"right",self.scale)
            images_left = [pygame.transform.flip(image, True, False) for image in images_right]
            self.player_imgs[anim + "right"] = images_right
            self.player_imgs[anim+"left"]=images_left


class Parser:
    TILE_SIZE = 32
    TILE_SIZE_HALF = TILE_SIZE / 2
    TERRAIN_SHIFT = -6

    def __init__(self, scale):
        self.scale=scale
        self.TILE_SIZE*=scale
        self.TILE_SIZE_HALF *= scale
        self.TERRAIN_SHIFT *= scale

    def parse_map_to_static_draw_objects(self, images, game_map, center_x, center_y, y_offset=0):
        result_ls = list()
        for row_nb, row in enumerate(game_map):  # draw surface
            for col_nb, tile in enumerate(row):
                tile = int(tile)
                if tile != 0:
                    tile_image = images[tile - 1]
                    cart_x = row_nb * self.TILE_SIZE_HALF
                    cart_y = col_nb * self.TILE_SIZE_HALF
                    iso_x = (cart_x - cart_y)
                    iso_y = (cart_x + cart_y) / 2
                    centered_x = center_x - self.TILE_SIZE_HALF + iso_x
                    centered_y = center_y / 2 - self.TILE_SIZE + iso_y + y_offset*self.scale
                    print(center_x,center_y)
                    result_ls.append(StaticDrawObject(tile_image, centered_x, centered_y))
        return result_ls
