import pygame
from main.gui.constants import WINDOW_HEIGHT, WINDOW_WIDTH, GAME_NAME, DATA_FOLDER, ACTION_ENTRY
from main.gui.game_utils import Resources
from main.gui.login_menu import LoginMenu
from main.gui.main_menu import MainMenu
from main.gui.no_internet_menu import NoInternetMenu
from main.server_connector.server_connector import ServerConnector
from main.server_connector.server_errors_handler import ServerErrorsHandler

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
resources = Resources(DATA_FOLDER)

#print(ServerConnector.get_saved_username())

(is_ok,is_logged_in) =ServerErrorsHandler.try_is_logged_in()
if not is_ok:
    no_internet_menu = NoInternetMenu(resources, screen, clock,ACTION_ENTRY)
    no_internet_menu.launch()
else:
    if is_logged_in:
        main_menu = MainMenu(resources, screen, clock)
        main_menu.launch()
    else:
        login_menu = LoginMenu(resources, screen, clock)
        login_menu.launch()

'''
try:
    is_logged_in = ServerConnector.is_logged_in()
except Exception:
    no_internet_menu = NoInternetMenu(resources, screen, clock,ACTION_ENTRY)
    no_internet_menu.launch()
else:
    print("no errors")
    if is_logged_in:
        main_menu = MainMenu(resources, screen, clock)
        main_menu.launch()
    else:
        login_menu = LoginMenu(resources, screen, clock)
        login_menu.launch()'''
