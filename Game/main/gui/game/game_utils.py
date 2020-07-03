import os
import re

import pygame

from main.gui.constants import SCALE, GUI_SCALE, PLAYER_MENU_SCALE


class Resources:
    monster_mushroom = "monster_mushroom"
    creatures = ["monster_mushroom", "monster_goblin"]
    player = "player"
    gui = "gui"
    font = "font.otf"
    backgrounds = ["grass", "pond_top", "pond_right", "pond_left", "pond_bottom"]
    terrain = ["house", "pine", "oak", "birch", "flower_purple", "fern", "bush", "invisible"]
    creature_anims_name = ["walk_", "idle_", "attack_", "take_damage_",
                           "die_"]  # все папки должны иметь название ""+right
    menu_player_anims = ["menu_idle", "menu_transform"]
    game_gui_images = ["bars", "inventory", "hp_bar", "mana_bar"]

    def __init__(self, directory):
        self.directory = directory

    def load_backgrounds_text(self):
        result = []
        for background in self.backgrounds:
            path = os.path.join(self.directory, background) + ".png"
            result.append(Resources.load_image(path))
        return result

    def load_terrain_text(self):
        result = []
        for terrain_element in self.terrain:
            path = os.path.join(self.directory, terrain_element) + ".png"
            result.append(Resources.load_image(path))
        return result

    def load_backgrounds(self):
        result = {}
        for background in self.backgrounds:
            path = os.path.join(self.directory, background) + ".png"
            result.update({background: Resources.load_image(path)})
        return result

    def load_terrain(self):
        result = {}
        for terrain_element in self.terrain:
            path = os.path.join(self.directory, terrain_element) + ".png"
            result.update({terrain_element: Resources.load_image(path)})
        return result

    def load_creatures(self):
        result = {}
        for creature in self.creatures:
            creature_resources = self.load_creature(creature)
            result.update({creature: creature_resources})
        return result

    def load_creature(self, type: str):
        result = {}
        for anim in self.creature_anims_name:
            path = os.path.join(self.directory, type, anim)
            images_right = Resources.load_folder_images(path + "right")
            images_left = [pygame.transform.flip(image, True, False) for image in images_right]
            result[anim + "right"] = images_right
            result[anim + "left"] = images_left
        return result

    def load_menu_player(self):
        result = {}
        for anim in self.menu_player_anims:
            path = os.path.join(self.directory, self.player, anim)
            images = Resources.load_folder_images(path, PLAYER_MENU_SCALE)
            result[anim] = images
        return result

    # кнопки лежат в папке gui и имеют название button_name_state (state - normal/pressed/hover)
    def load_button_images(self, name):
        result = {}
        gui_dir = os.path.join(self.directory, self.gui, "button_")
        result["normal"] = Resources.load_image(f"{gui_dir}{name}_normal.png", GUI_SCALE)
        result["pressed"] = Resources.load_image(f"{gui_dir}{name}_pressed.png", GUI_SCALE)
        result["hover"] = Resources.load_image(f"{gui_dir}{name}_hover.png", GUI_SCALE)
        return result

    def load_inserter_bg_normal(self):
        return Resources.load_image(os.path.join(self.directory, self.gui, "inserter_bg_normal.png"), GUI_SCALE)

    def load_inserter_bg_active(self):
        return Resources.load_image(os.path.join(self.directory, self.gui, "inserter_bg_active.png"), GUI_SCALE)

    def load_main_menu_background(self):
        return Resources.load_image(os.path.join(self.directory, "main_menu_bg.png"), GUI_SCALE)

    def load_login_background(self):
        return Resources.load_image(os.path.join(self.directory, "login_bg.png"), GUI_SCALE)

    def load_no_internet_background(self):
        return Resources.load_image(os.path.join(self.directory, "no_internet_bg.png"), GUI_SCALE)

    def load_leaderboards_background(self):
        return Resources.load_image(os.path.join(self.directory, "leaderboards_bg.png"), GUI_SCALE)

    def load_leaderboards_menu_background(self):
        return Resources.load_image(os.path.join(self.directory, self.gui, "leaderboards_menu_bg.png"), GUI_SCALE)

    def load_login_menu_background(self):
        return Resources.load_image(os.path.join(self.directory, self.gui, "login_menu_bg.png"), GUI_SCALE)

    def load_game_overlay_images(self):
        result = {}
        for image in self.game_gui_images:
            path = os.path.join(self.directory, self.gui, f"{image}.png")
            result[image] = Resources.load_image(path, GUI_SCALE)
        return result

    def load_font(self, size):
        return pygame.font.Font(os.path.join(self.directory, self.gui, self.font), size)

    @staticmethod
    def load_image(path, scale=SCALE):
        img = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))

    @staticmethod
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
