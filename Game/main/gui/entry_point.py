import pygame

from main.gui.constants import WINDOW_HEIGHT, WINDOW_WIDTH, GAME_NAME, RESOURCES_FOLDER
from main.gui.game.game_utils import Resources
from main.gui.main_menu.main_menu import MainMenu

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
resources = Resources(RESOURCES_FOLDER)

main_menu = MainMenu(resources, screen, clock)
main_menu.launch()
# (is_ok, is_logged_in) = ServerErrorsHandler.try_is_logged_in()
# if not is_ok:
#     no_internet_menu = ServerUnreachableMenu(resources, screen, clock, ACTION_ENTRY)
#     no_internet_menu.launch()
# else:
#     if is_logged_in:
#         main_menu = MainMenu(resources, screen, clock)
#         main_menu.launch()
#     else:
#         login_menu = LoginMenu(resources, screen, clock)
#         login_menu.launch()
