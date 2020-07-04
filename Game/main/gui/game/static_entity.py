from pygame.rect import Rect

from main.gui.constants import SCALE


class StaticEntity:
    def __init__(self, image, start_x, start_y):
        self.image = image  # устанавливаем имя
        self.start_x = start_x
        self.start_y = start_y
        self.draw_x = start_x
        self.draw_y = start_y

    # для отрисовки видимых объектов (не учитывает сдвиг по y, учитывает положение камеры)
    def get_visibility_rect(self, camera):
        coordinates = (self.draw_x+camera.x_shift, self.draw_y+camera.y_shift)
        return Rect(coordinates, (self.image.get_rect().width, self.image.get_rect().height))

    # для проверки могут ли сущности двигаться в определенном направлении
    # одинаков для всех препятсвий и совпадает с размером клетки травы
    # не учитывает сдвиг по y, не учитывает положение камеры
    def get_taken_place_rect(self,camera):
        visibility_rect = self.get_visibility_rect(camera).inflate(-20 * SCALE, -27 * SCALE).move(0, 4 * SCALE)
        return visibility_rect

    def draw(self, display,camera):
        display.blit(self.image, (self.draw_x+camera.x_shift, self.draw_y+camera.y_shift))

    def update(self, camera):
        self.draw_x = self.start_x + camera.x_shift
        self.draw_y = self.start_y + camera.y_shift