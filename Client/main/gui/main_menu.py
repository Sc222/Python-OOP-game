import pygame
import thorpy

from main.gui import game_main, leaderboards_menu, gui_utils
from main.gui.constants import FPS, GAME_NAME, MAIN_MENU_HEADER, WHITE, RED, RED_DARK, GREEN, ACTION_GET_USER
from main.gui.gui_utils import create_button, render_text
from main.gui.main_menu_utils import ScrollingBackgroundHorizontal, PlayerMenu
from main.gui.no_internet_menu import NoInternetMenu
from main.server_connector.server_connector import ServerConnector
from main.server_connector.server_errors_handler import ServerErrorsHandler


class MainMenu:

    def __init__(self, resources, screen, clock):
        self.is_opened = True
        self.resources = resources
        self.screen = screen
        self.clock = clock
        self.player_menu = PlayerMenu((475, 230), resources.load_menu_player())
        self.background_image = resources.load_main_menu_background()
        scroll_width = self.background_image.get_width()

        self.text_name = gui_utils.create_text("", (0, 0), RED_DARK, 60)
        self.text_level = gui_utils.create_text("", (0, 0), GREEN, 35)
        text_game_title = gui_utils.create_text(GAME_NAME, (115, 15), MAIN_MENU_HEADER, 150)

        self.background_left = ScrollingBackgroundHorizontal(self.background_image, scroll_width * (-1), 0,
                                                             scroll_width)
        self.background_right = ScrollingBackgroundHorizontal(self.background_image, 0, 0, scroll_width)
        button_play = create_button(resources.load_button_images("play"), self.start_transformation)
        button_play.set_topleft((50 - 5, 250))
        button_leaderboards = create_button(resources.load_button_images("leaderboards"), self.launch_leaderboards)
        button_leaderboards.set_topleft((125 - 5, 350 + 5))
        button_exit = create_button(resources.load_button_images("exit"), self.quit_game)
        button_exit.set_topleft((200 - 5, 450 + 5 * 2))
        self.container = thorpy.Ghost(elements=[button_play, button_leaderboards,
                                                button_exit, text_game_title,
                                                self.text_name,
                                                self.text_level])

        # try to get user from server
        self.try_load_user(clock, resources, screen)

        self.menu = thorpy.Menu(self.container)
        for element in self.menu.get_population():
            element.surface = screen

    def try_load_user(self, clock, resources, screen):
        self.is_opened, user = ServerErrorsHandler.try_get_user()
        if user is None:
            no_internet_menu = NoInternetMenu(resources, screen, clock, ACTION_GET_USER)
            no_internet_menu.launch()
        else:
            self.text_name.set_text(user["nickname"])
            self.text_level.set_text("Level " + str(user["playerLevel"]))
            self.text_name.set_center_pos((684, 230))
            self.text_level.set_center_pos((684, 275))

    def start_transformation(self):
        self.text_name.set_text("")
        self.text_level.set_text("")
        self.player_menu.start_transformation()

    def launch_game(self):
        print("launch game")
        self.is_opened = False
        self.player_menu.stop_transformation()
        game = game_main.Game(self.resources, self.screen, self.clock)
        game.launch()

    def launch_leaderboards(self):
        self.is_opened = False
        leaderboards_screen = leaderboards_menu.LeaderboardsMenu(self.resources, self.screen, self.clock)
        leaderboards_screen.launch()

    def quit_game(self):
        pygame.quit()

    def launch(self):
        while self.is_opened:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_opened = False
                    break
                self.menu.react(event)
            if self.player_menu.is_transformation_finished():
                self.launch_game()
            self.background_left.update(dt)
            self.background_right.update(dt)
            self.player_menu.update(dt)
            self.background_left.draw(self.screen)
            self.background_right.draw(self.screen)
            self.player_menu.draw(self.screen)
            self.container.blit()
            self.container.update()
            pygame.display.flip()
