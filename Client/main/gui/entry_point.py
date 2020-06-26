import pygame
from main.gui.constants import WINDOW_HEIGHT, WINDOW_WIDTH, GAME_NAME, DATA_FOLDER
from main.gui.game_utils import Resources
from main.gui.main_menu import MainMenu
from main.server_connector.server_connector import ServerConnector

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
resources = Resources(DATA_FOLDER)

#ServerConnector.login("Sc222","Sc222")
if ServerConnector.is_logged_in():
    main_menu = MainMenu(resources, screen, clock)
    main_menu.launch()
else:
    pass
