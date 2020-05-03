import pygame
from main.gui.constants import WINDOW_HEIGHT, WINDOW_WIDTH, GAME_NAME, DATA_FOLDER
from main.gui.game_utils import Resources
from main.gui.main_menu import MainMenu

clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
resources = Resources(DATA_FOLDER)
main_menu = MainMenu(resources, screen, clock)
main_menu.launch()
