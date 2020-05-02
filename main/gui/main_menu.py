import pygame
import thorpy

from main.gui import game_main
from main.gui.constants import FPS, GAME_NAME
from main.gui.main_menu_utils import ScrollingBackground, create_button, PlayerMenu, render_text


class MainMenu:

    def __init__(self, resources, screen, clock):
        self.is_opened = True
        self.resources = resources
        self.screen = screen
        self.clock = clock
        self.player_menu = PlayerMenu((475, 200), resources.load_menu_player())
        self.background_image = resources.load_menu_background()
        scroll_width = self.background_image.get_width()
        self.background_left = ScrollingBackground(self.background_image, scroll_width * (-1), 0, scroll_width)
        self.background_right = ScrollingBackground(self.background_image, 0, 0, scroll_width)
       # title_game = thorpy.make_text(GAME_NAME, 150)
       # title_game.set_font(FONT)
       # title_game.set_topleft((115, 50))
        button_play = create_button(resources.load_button_images("play"), self.start_transformation)
        button_play.set_topleft((50 - 5, 250))
        button_leaderboards = create_button(resources.load_button_images("leaderboards"), self.launch_leaderboards)
        button_leaderboards.set_topleft((125 - 5, 350 + 5))
        button_exit = create_button(resources.load_button_images("exit"), self.quit_game)
        button_exit.set_topleft((200 - 5, 450 + 5 * 2))
        self.container = thorpy.Ghost(elements=[button_play, button_leaderboards, button_exit])
        self.menu = thorpy.Menu(self.container)
        for element in self.menu.get_population():
            element.surface = screen

    def start_transformation(self):
        self.player_menu.start_transformation()

    def launch_game(self):
        print("launch game")
        self.is_opened = False
        self.player_menu.stop_transformation()
        game = game_main.Game(self.resources,self.screen,self.clock)
        game.launch()

    def launch_leaderboards(self):
        # TODO LAUNCH LEADERBOARDS HERE
        print("launch leaderboards")

    def quit_game(self):
        # TODO QUIT GAME HERE
        print("quit game")
        pygame.quit()

    def launch(self):
        font_resource = self.resources.load_font(150)
        while self.is_opened:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_opened = False
                    break
                self.menu.react(event)  # the menu automatically integrate your elements
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
            render_text(self.screen,font_resource, (115, 50),GAME_NAME)
            pygame.display.flip()