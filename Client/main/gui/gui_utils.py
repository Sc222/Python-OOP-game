from thorpy import Clickable
from thorpy.painting.painters.imageframe import ImageButton


def create_button(images, func):
    e = Clickable("", finish=False)
    e.user_func = func
    painter = ImageButton(images["normal"], images["pressed"], images["hover"], force_convert_alpha=True)
    e.set_painter(painter)
    e.finish()
    return e

def render_text(screen, font, pos, text, color):
    text = font.render(text, False, color)
    text_rect = text.get_rect()
    text_rect.move_ip(pos)
    screen.blit(text, text_rect)