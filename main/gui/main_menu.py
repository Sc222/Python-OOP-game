import pygame
import thorpy


from main.gui.constants import WINDOW_HEIGHT, WINDOW_WIDTH, FPS, FONT, GAME_NAME
from main.gui.game_utils import load_image, Resources
from main.gui.main_menu_utils import ScrollingBackground, create_button, PlayerMenu


def start_transformation():
    player_menu.start_transformation()

def launch_game():
    print("launch game")
    player_menu.stop_transformation()

def launch_leaderboards():
    print("launch leaderboards")


def quit_game():
    print("quit game")
    pygame.quit()


clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption(GAME_NAME)
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

resources = Resources("../../data")

player_menu = PlayerMenu((475,200), resources.load_menu_player())

background_image = resources.load_menu_background()
scroll_width = background_image.get_width()
background_left = ScrollingBackground(background_image, scroll_width * (-1), 0, scroll_width)
background_right = ScrollingBackground(background_image, 0, 0, scroll_width)

title_game = thorpy.make_text(GAME_NAME, 150, (0, 105, 170))
title_game.set_font(FONT)
title_game.set_topleft((115, 50))

button_play = create_button(resources.load_button_images("play"), start_transformation)
button_play.set_topleft((50 - 5, 250))
button_leaderboards = create_button(resources.load_button_images("leaderboards"), launch_leaderboards)
button_leaderboards.set_topleft((125 - 5, 350 + 5))
button_exit = create_button(resources.load_button_images("exit"), quit_game)
button_exit.set_topleft((200 - 5, 450 + 5 * 2))
container = thorpy.Ghost(elements=[title_game, button_play, button_leaderboards, button_exit])
menu = thorpy.Menu(container)
for element in menu.get_population():
    element.surface = screen
container.blit()
container.update()

playing_game = True
while True:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing_game = False
            break
        menu.react(event)  # the menu automatically integrate your elements

    if player_menu.is_transformation_finished():
        launch_game()

    background_left.update(dt)
    background_right.update(dt)
    player_menu.update(dt)
    background_left.draw(screen)
    background_right.draw(screen)
    player_menu.draw(screen)
    container.blit()
    container.update()
    pygame.display.flip()
