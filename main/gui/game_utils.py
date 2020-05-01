import os
import re

import pygame
from pygame.rect import Rect


# object for drawing terrain and background
class StaticDrawObject:
    def __init__(self, image, draw_x, draw_y, y_offset):
        self.image = image  # устанавливаем имя
        self.draw_x = draw_x
        self.draw_y = draw_y
        self.y_offset = y_offset

    def get_draw_coordinates(self, camera):
        return self.draw_x + camera.x_shift, self.draw_y + camera.y_shift + self.y_offset

    def get_dimensions(self):
        return self.image.get_rect().width, self.image.get_rect().height

    # для отрисовки видимых объектов (не учитывает сдвиг по y, учитывает положение камеры)
    def get_visibility_rect(self, camera):
        coordinates = (self.draw_x + camera.x_shift, self.draw_y + camera.y_shift)
        return Rect(coordinates, self.get_dimensions())

    # для проверки могут ли сущности двигаться в определенном направлении
    # одинаков для всех препятсвий и совпадает с размером клетки травы
    # не учитывает сдвиг по y, не учитывает положение камеры
    def get_taken_place_rect(self,camera,scale):
        visibility_rect = self.get_visibility_rect(camera).inflate(-20*scale,-27*scale).move(0,4*scale)
        return visibility_rect


class Camera:

    def __init__(self, x_shift: int, y_shift: int, visible_rect: Rect):
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.visible_rect = visible_rect

    def update(self, x_movement: int, y_movement: int):
        self.x_shift += x_movement
        self.y_shift += y_movement

    def should_draw(self, draw_object: StaticDrawObject):
        return self.visible_rect.colliderect(draw_object.get_visibility_rect(self))


def load_image(path, scale):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))


def load_folder_images(path, scale):
    """
    Загружает все картинки из папки.
    В папке не должно быть других файлов.
    Картинки сортируются по имени, поэтому именоваться они должны в порядке анимации
    и имя файла должно состоять только из цифр (1,2,3,4...)
    """
    images = []
    files = os.listdir(path)
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    for file_name in files:
        img = pygame.image.load(path + os.sep + file_name).convert_alpha()
        images.append(pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale)))
    return images


class Resources:
    player = "player"
    backgrounds = ["grass", "pond_top", "pond_right", "pond_left", "pond_bottom"]
    terrain = ["house", "pine", "oak", "birch", "flower_purple", "fern", "bush","invisible"]
    player_anims_name = ["walk_", "idle_", "attack_"]  # все папки должны иметь название ""+right
    bg_imgs = []
    terrain_imgs = []
    player_imgs = {}

    def __init__(self, directory, scale):
        self.directory = directory
        self.scale = scale
        self.load_backgrounds()
        self.load_terrain()
        self.load_player()

    def load_backgrounds(self):
        for background in self.backgrounds:
            path = os.path.join(self.directory, background) + ".png"
            self.bg_imgs.append(load_image(path, self.scale))

    def load_terrain(self):
        for terrain_element in self.terrain:
            path = os.path.join(self.directory, terrain_element) + ".png"
            self.terrain_imgs.append(load_image(path, self.scale))

    def load_player(self):
        for anim in self.player_anims_name:
            path = os.path.join(self.directory, self.player, anim)
            images_right = load_folder_images(path + "right", self.scale)
            images_left = [pygame.transform.flip(image, True, False) for image in images_right]
            self.player_imgs[anim + "right"] = images_right
            self.player_imgs[anim + "left"] = images_left


class Parser:
    TILE_SIZE = 32
    TILE_SIZE_HALF = TILE_SIZE / 2
    TERRAIN_SHIFT = -6

    def __init__(self, scale):
        self.scale = scale
        self.TILE_SIZE *= scale
        self.TILE_SIZE_HALF *= scale
        self.TERRAIN_SHIFT *= scale

    def parse_map_to_static_draw_objects(self, images, game_map, center_x, center_y, extra_y_offset=0):
        result_ls = list()
        for map_x, row in enumerate(game_map):
            for map_y, tile in enumerate(row):
                tile = int(tile)
                if tile != 0:
                    tile_image = images[tile - 1]
                    x_shift = center_x - self.TILE_SIZE_HALF
                    y_shift = center_y*0.5-self.TILE_SIZE
                    centered_x = x_shift + (map_x-map_y)*self.TILE_SIZE_HALF
                    centered_y = y_shift + (map_x+map_y)*0.5*self.TILE_SIZE_HALF
                    result_ls.append(StaticDrawObject(tile_image, centered_x, centered_y, extra_y_offset * self.scale))
        return result_ls
