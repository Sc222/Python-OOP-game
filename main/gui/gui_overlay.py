import os

from game_utils import load_image
from pygame.surface import Surface


# !!!todo enum gui states, base gui class that checks enum and switches between overlays!!!

class GameOverlay:

    def __init__(self, scale, max_hp, max_mana, center_x, center_y):
        corner_margin = 3 * scale

        self.scale = scale
        self.max_hp = max_hp
        self.max_mana = max_mana
        self.bars = load_image(os.path.join("data", "gui", "bars.png"), scale)
        self.bars_pos = (corner_margin, corner_margin)
        self.inventory = load_image(os.path.join("data", "gui", "inventory.png"), scale)
        self.inventory_pos = (
        center_x - self.inventory.get_width() / 2, center_y * 2 - self.inventory.get_height() - corner_margin)

    def draw(self, display: Surface, hp, mana, items):
        self.draw_hp_and_mana(display, hp, mana)
        self.draw_inventory(display, items)

    def draw_hp_and_mana(self, display, hp, mana):
        # todo draw mana and hp

        display.blit(self.bars, self.bars_pos)
        pass

    def draw_inventory(self, display, items):
        display.blit(self.inventory, self.inventory_pos)

        # todo draw items
        pass
