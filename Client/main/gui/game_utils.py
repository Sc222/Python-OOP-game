import os
import re

import pygame
from pygame.rect import Rect

# object for drawing terrain and background
from main.gui.constants import SCALE, GUI_SCALE, PLAYER_MENU_SCALE


class StaticDrawObject:
    def __init__(self, image, start_x, start_y, y_offset):
        self.image = image  # устанавливаем имя
        self.start_x = start_x
        self.start_y = start_y
        self.y_offset = y_offset
        self.draw_x = start_x
        self.draw_y = start_y

    # для отрисовки видимых объектов (не учитывает сдвиг по y, учитывает положение камеры)
    def get_visibility_rect(self):
        coordinates = (self.draw_x, self.draw_y)
        return Rect(coordinates, (self.image.get_rect().width, self.image.get_rect().height))

    # для проверки могут ли сущности двигаться в определенном направлении
    # одинаков для всех препятсвий и совпадает с размером клетки травы
    # не учитывает сдвиг по y, не учитывает положение камеры
    def get_taken_place_rect(self, scale=SCALE):
        visibility_rect = self.get_visibility_rect().inflate(-20 * scale, -27 * scale).move(0, 4 * scale)
        return visibility_rect

    def draw(self, display):
        display.blit(self.image, (self.draw_x, self.draw_y + self.y_offset))

    def update(self, camera):
        self.draw_x = self.start_x + camera.x_shift
        self.draw_y = self.start_y + camera.y_shift


class Camera:

    def __init__(self, x_shift: int, y_shift: int, visible_rect: Rect):
        self.x_shift = x_shift
        self.y_shift = y_shift
        self.visible_rect = visible_rect

    def update(self, x_movement: int, y_movement: int):
        self.x_shift += x_movement
        self.y_shift += y_movement

    def is_visible(self, draw_object: StaticDrawObject):
        return self.visible_rect.colliderect(draw_object.get_visibility_rect())


def load_image(path, scale=SCALE):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))


def load_folder_images(path, scale=SCALE):
    """
    Загружает все картинки из папки.
    В папке не должно быть других файлов.
    Картинки сортируются по имени, поэтому именоваться они должны в порядке анимации
    и имя файла должно состоять только из цифр (1,2,3,4...)
    """
    images = []
    files = os.listdir(path)
    files.sort(key=lambda f: int(re.sub(r'\D', '', f)))
    for file_name in files:
        img = pygame.image.load(path + os.sep + file_name).convert_alpha()
        images.append(pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale)))
    return images


class Resources:
    monster = "monster"
    player = "player"
    gui = "gui"
    font = "font.otf"
    backgrounds = ["grass", "pond_top", "pond_right", "pond_left", "pond_bottom"]
    terrain = ["house", "pine", "oak", "birch", "flower_purple", "fern", "bush", "invisible"]
    creature_anims_name = ["walk_", "idle_", "attack_","take_damage_","die_"]  # все папки должны иметь название ""+right
    menu_player_anims = ["menu_idle", "menu_transform"]
    game_gui_images = ["bars", "inventory", "hp_bar", "mana_bar"]

    def __init__(self, directory, scale=SCALE):
        self.directory = directory
        self.scale = scale

    def load_backgrounds(self):
        result = {}
        for background in self.backgrounds:
            path = os.path.join(self.directory, background) + ".png"
            result.update({background:load_image(path, self.scale)})
        return result

    def load_terrain(self):
        result = {}
        for terrain_element in self.terrain:
            path = os.path.join(self.directory, terrain_element) + ".png"
            result.update({terrain_element:load_image(path, self.scale)})
        return result

    def load_creature(self,type:str):
        result = {}
        for anim in self.creature_anims_name:
            path = os.path.join(self.directory, type, anim)
            images_right = load_folder_images(path + "right", self.scale)
            images_left = [pygame.transform.flip(image, True, False) for image in images_right]
            result[anim + "right"] = images_right
            result[anim + "left"] = images_left
        return result

    def load_menu_player(self):
        result = {}
        for anim in self.menu_player_anims:
            path = os.path.join(self.directory, self.player, anim)
            images = load_folder_images(path, PLAYER_MENU_SCALE)
            result[anim] = images
        return result

    # кнопки лежат в папке gui и имеют название button_name_state (state - normal/pressed/hover)
    def load_button_images(self, name):
        result = {}
        gui_dir = os.path.join(self.directory, self.gui, "button_")
        result["normal"] = load_image(f"{gui_dir}{name}_normal.png", GUI_SCALE)
        result["pressed"] = load_image(f"{gui_dir}{name}_pressed.png", GUI_SCALE)
        result["hover"] = load_image(f"{gui_dir}{name}_hover.png", GUI_SCALE)
        return result

    def load_inserter_bg_normal(self):
        return load_image(os.path.join(self.directory,self.gui, "inserter_bg_normal.png"), GUI_SCALE)

    def load_inserter_bg_active(self):
        return load_image(os.path.join(self.directory,self.gui, "inserter_bg_active.png"), GUI_SCALE)

    def load_main_menu_background(self):
        return load_image(os.path.join(self.directory, "main_menu_bg.png"), GUI_SCALE)

    def load_login_background(self):
        return load_image(os.path.join(self.directory, "login_bg.png"), GUI_SCALE)

    def load_no_internet_background(self):
        return load_image(os.path.join(self.directory, "no_internet_bg.png"), GUI_SCALE)

    def load_leaderboards_background(self):
        return load_image(os.path.join(self.directory, "leaderboards_bg.png"), GUI_SCALE)

    def load_leaderboards_menu_background(self):
        return load_image(os.path.join(self.directory, self.gui,  "leaderboards_menu_bg.png"), GUI_SCALE)

    def load_login_menu_background(self):
        return load_image(os.path.join(self.directory, self.gui, "login_menu_bg.png"), GUI_SCALE)

    def load_game_overlay_images(self):
        result = {}
        for image in self.game_gui_images:
            path = os.path.join(self.directory, self.gui, f"{image}.png")
            result[image] = load_image(path, GUI_SCALE)
        return result

    def load_font(self, size):
        return pygame.font.Font(os.path.join(self.directory, self.gui, self.font), size)


class Parser:
    TILE_SIZE = 32
    TILE_SIZE_HALF = TILE_SIZE / 2
    TERRAIN_SHIFT = -6

    def __init__(self, scale=SCALE):
        self.scale = scale
        self.TILE_SIZE *= scale
        self.TILE_SIZE_HALF *= scale
        self.TERRAIN_SHIFT *= scale

    def map_to_draw_objects(self, images, game_map, center_x, center_y, extra_y_offset=0):
        result_ls = list()
        for map_x, row in enumerate(game_map):
            print(map_x)
            print(row)
            for map_y, tile in enumerate(row):
                tile = int(tile)
                if tile != 0:
                    tile_image = images[tile - 1]
                    x_shift = center_x - self.TILE_SIZE_HALF
                    y_shift = center_y * 0.5 - self.TILE_SIZE
                    centered_x = x_shift + (map_x - map_y) * self.TILE_SIZE_HALF
                    centered_y = y_shift + (map_x + map_y) * 0.5 * self.TILE_SIZE_HALF
                    result_ls.append(StaticDrawObject(tile_image, centered_x, centered_y, extra_y_offset * self.scale))
        return result_ls

    def map_to_draw_objects_from_server(self, images, game_map, center_x, center_y, extra_y_offset=0):
        result_ls = list()
        for map_obj in game_map:
                tile_image=images[map_obj.name]
                x_shift = center_x - self.TILE_SIZE_HALF
                y_shift = center_y * 0.5 - self.TILE_SIZE
                centered_x = x_shift + (map_obj.x - map_obj.y) * self.TILE_SIZE_HALF
                centered_y = y_shift + (map_obj.x + map_obj.y) * 0.5 * self.TILE_SIZE_HALF
                result_ls.append(StaticDrawObject(tile_image, centered_x, centered_y, extra_y_offset * self.scale))
        return result_ls