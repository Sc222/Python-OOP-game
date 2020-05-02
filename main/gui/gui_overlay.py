import os

import pygame
from pygame.surface import Surface

from main.gui.game_utils import load_image


# !!!todo enum gui states, base gui class that checks enum and switches between overlays!!!

class GameOverlay:

    def __init__(self, scale, max_hp, max_mana, center_x, center_y):
        corner_margin = 3 * scale
        self.bar_filled = 51 * scale

        self.scale = scale
        self.max_hp = max_hp
        self.max_mana = max_mana

        self.bars = load_image(os.path.join("data", "gui", "bars.png"), scale)
        self.bars_pos = (corner_margin, corner_margin)

        self.inventory = load_image(os.path.join("data", "gui", "inventory.png"), scale)
        self.inventory_pos = (
        center_x - self.inventory.get_width() / 2, center_y * 2 - self.inventory.get_height() - corner_margin)

        self.hp_bar = load_image(os.path.join("data", "gui", "hp_bar.png"), scale)
        self.hp_bar_pos = (self.bars_pos[0] + 36 * scale, self.bars_pos[1] + 5 * scale)  # 36, 5 - for positioning

        self.mana_bar = load_image(os.path.join("data", "gui", "mana_bar.png"), scale)
        self.mana_bar_pos = (self.bars_pos[0] + 36 * scale, self.bars_pos[1] + 20 * scale)  # 36, 20 - for positioning

    def draw(self, display: Surface, hp, mana, items):
        self.draw_hp_and_mana(display, hp, mana)
        self.draw_inventory(display, items)

    def draw_hp_and_mana(self, display, hp, mana):
        # todo draw mana and hp
        hp_draw_width = hp // self.max_hp * self.bar_filled
        mana_draw_width = mana // self.max_mana * self.bar_filled

        display.blit(self.bars, self.bars_pos)
        display.blit(pygame.transform.scale(self.hp_bar, (hp_draw_width, self.hp_bar.get_height())), self.hp_bar_pos)
        display.blit(pygame.transform.scale(self.mana_bar, (mana_draw_width, self.mana_bar.get_height())),
                     self.mana_bar_pos)
        pass

    def draw_inventory(self, display, items):
        display.blit(self.inventory, self.inventory_pos)

        # todo draw items
        pass
