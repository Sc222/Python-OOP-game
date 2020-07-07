from pygame.rect import Rect


class Camera:

    def __init__(self, x, y, visible_rect: Rect):
        self.x_shift = x
        self.y_shift = y
        self.visible_rect = visible_rect

    def update(self, x_movement: int, y_movement: int):
        self.x_shift += x_movement
        self.y_shift += y_movement

    def set_new_pos(self, x, y):
        self.x_shift = x
        self.y_shift = y
