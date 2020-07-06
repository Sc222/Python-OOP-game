from pygame.rect import Rect

from main.gui.game.static_entity import StaticEntity


class Camera:

    def __init__(self, x, y, visible_rect: Rect):
        self.x_shift = x
        self.y_shift = y
        self.visible_rect = visible_rect

    def update(self, x_movement: int, y_movement: int):
        self.x_shift += x_movement
        self.y_shift += y_movement

    def is_visible(self, draw_object: StaticEntity):
        return self.visible_rect.colliderect(draw_object.get_visibility_rect(self))

    def set_new_pos(self, x, y):
        self.x_shift = x
        self.y_shift = y
