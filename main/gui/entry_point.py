import pygame
from main.gui.constants import WINDOW_HEIGHT, WINDOW_WIDTH, GAME_NAME
from main.gui.game_utils import  Resources
from main.gui.main_menu import MainMenu


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)  # set the display mode, window title and FPS clock

resources = Resources("../../data")

main_menu=MainMenu(resources,screen,clock)

main_menu.launch()

#while True:
#    dt = clock.tick(FPS)

    #todo something with displau
 #   screen.blit(display, (0, 0))
#    pygame.display.flip()
