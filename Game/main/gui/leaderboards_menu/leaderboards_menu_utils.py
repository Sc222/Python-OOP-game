import pygame
import thorpy

from main.gui.constants import WHITE, TRANSPARENT, GUI_SCALE, MONOSPACE_FONT, \
    LEADERBOARD_INTIAL_FONT_SIZE


def create_leaderboards_element(formatted_leaderboard: str):
    leaderboard_element_text = thorpy.make_text(formatted_leaderboard)
    leaderboard_element_text.set_font(MONOSPACE_FONT)
    leaderboard_element_text.set_font_color(WHITE)

    resize_leaderboard_element_text(leaderboard_element_text)

    leaderboard_element_container = thorpy.Box(elements=[leaderboard_element_text])
    leaderboard_element_container.set_topleft((92 * GUI_SCALE, 62 * GUI_SCALE))
    leaderboard_element_container.set_size((132 * GUI_SCALE, 109 * GUI_SCALE))
    leaderboard_element_container.add_lift()
    leaderboard_element_container.set_main_color(TRANSPARENT)

    return leaderboard_element_container


def resize_leaderboard_element_text(leaderboard_element_text):
    font_size = LEADERBOARD_INTIAL_FONT_SIZE
    leaderboard_element_text.set_font_size(LEADERBOARD_INTIAL_FONT_SIZE)
    leaderboard_element_text.scale_to_title()
    # масштабирование текста
    while leaderboard_element_text.get_size()[0] > 125 * GUI_SCALE and font_size > 2:
        font_size = font_size - 1
        leaderboard_element_text.set_font_size(font_size)
        leaderboard_element_text.scale_to_title()


class ScrollingBackgroundVertical(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scroll_height):
        super(ScrollingBackgroundVertical, self).__init__()
        self.image = image
        self.x = x
        self.y = y
        self.animation_time = 15
        self.current_time = 0
        self.rect = self.image.get_rect()
        self.scroll_height = scroll_height

    def scroll(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.y -= 1
            if self.y < -self.scroll_height:
                self.y = self.scroll_height

    def update(self, dt):
        self.scroll(dt)

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))
