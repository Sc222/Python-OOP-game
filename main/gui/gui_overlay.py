import pygame
from pygame.surface import Surface
from main.gui.constants import GUI_SCALE


class GameOverlay:

    def __init__(self, images, max_hp, max_mana, center_x, center_y):
        corner_margin = 3 * GUI_SCALE
        self.bar_filled = 51 * GUI_SCALE
        self.max_hp = max_hp
        self.max_mana = max_mana
        self.bars = images["bars"]
        self.bars_pos = (corner_margin, corner_margin)
        self.inventory = images["inventory"]
        self.inventory_pos = (center_x - self.inventory.get_width() / 2,
                              center_y * 2 - self.inventory.get_height() - corner_margin)
        self.hp_bar = images["hp_bar"]
        self.hp_bar_pos = (self.bars_pos[0] + 36 * GUI_SCALE,
                           self.bars_pos[1] + 5 * GUI_SCALE)  # 36, 5 - for positioning
        self.mana_bar = images["mana_bar"]
        self.mana_bar_pos = (self.bars_pos[0] + 36 * GUI_SCALE,
                             self.bars_pos[1] + 20 * GUI_SCALE)  # 36, 20 - for positioning

    def draw(self, display: Surface, hp, mana, items):
        self.draw_hp_and_mana(display, hp, mana)
        self.draw_inventory(display, items)

    def draw_hp_and_mana(self, display, hp, mana):
        hp_draw_width = int((hp / self.max_hp) * self.bar_filled)
        mana_draw_width = int((mana / self.max_mana) * self.bar_filled)
        display.blit(self.bars, self.bars_pos)
        display.blit(pygame.transform.scale(self.hp_bar, (hp_draw_width, self.hp_bar.get_height())), self.hp_bar_pos)
        display.blit(pygame.transform.scale(self.mana_bar, (mana_draw_width, self.mana_bar.get_height())),
                     self.mana_bar_pos)

    def draw_inventory(self, display, items):
        display.blit(self.inventory, self.inventory_pos)
        # todo draw items
