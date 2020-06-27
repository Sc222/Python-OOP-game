import thorpy
from thorpy import Clickable
from thorpy.painting.painters.imageframe import ImageButton

from main.gui.constants import TRANSPARENT, GUI_SCALE, WHITE, MONOSPACE_FONT


def create_button(images, func):
    e = Clickable("", finish=False)
    e.user_func = func
    painter = ImageButton(images["normal"], images["pressed"], images["hover"], force_convert_alpha=True)
    e.set_painter(painter)
    e.finish()
    return e


def create_inserter(res):
    inserter = thorpy.Inserter(value="")
    inserter.set_iwriter_font_size(25)
    bg_normal = res.load_inserter_bg_normal()
    painter = ImageButton(bg_normal,
                          bg_normal,
                          bg_normal, force_convert_alpha=True)
    painter.set_color(TRANSPARENT)
    painter.set_size((100 * GUI_SCALE, 22 * GUI_SCALE))
    painter.set_clip((-10 * GUI_SCALE, 0))
    inserter.set_main_color(TRANSPARENT)
    inserter._iwriter.set_font_color(WHITE)
    inserter._iwriter.set_font(MONOSPACE_FONT)
    inserter.set_painter(painter)
    inserter.finish()
    return inserter

def create_text(text:str,pos,font_color,font_size,font=MONOSPACE_FONT):
    text = thorpy.make_text(text)
    text.set_topleft(pos)
    text.set_font(font)
    text.set_font_color(font_color)
    text.set_font_size(font_size)
    return text

def render_text(screen, font, pos, text, color):
    text = font.render(text, False, color)
    text_rect = text.get_rect()
    text_rect.move_ip(pos)
    screen.blit(text, text_rect)
