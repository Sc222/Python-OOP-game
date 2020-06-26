import pygame
import thorpy
from tabulate import tabulate
from main.gui.constants import FPS, GUI_SCALE
from main.gui import main_menu
from main.gui.gui_utils import create_button
from main.gui.leaderboards_menu_utils import ScrollingBackgroundVertical, create_leaderboards_element, \
    resize_leaderboard_element_text
from main.server_connector.server_connector import ServerConnector


class LeaderboardsMenu:

    def __init__(self, res, screen, clock):
        self.is_opened = True
        self.res = res
        self.screen = screen
        self.clock = clock
        self.background_image = res.load_leaderboards_background()
        scroll_height = self.background_image.get_height()
        self.background_top = ScrollingBackgroundVertical(self.background_image, 0, scroll_height * (-1), scroll_height)
        self.background_bottom = ScrollingBackgroundVertical(self.background_image, 0, 0, scroll_height)

        button_leaderboards = create_button(res.load_button_images("quit_leaderboards"), self.launch_main_menu)
        button_leaderboards.set_topleft((68 * GUI_SCALE, 24 * GUI_SCALE))

        button_lvl_one = create_button(res.load_button_images("lvl_1"), self.change_to_level_one)
        button_lvl_one.set_topleft((61 * GUI_SCALE, 72 * GUI_SCALE))

        button_lvl_two = create_button(res.load_button_images("lvl_2"), self.change_to_level_two)
        button_lvl_two.set_topleft((61 * GUI_SCALE, 98 * GUI_SCALE))

        button_lvl_three = create_button(res.load_button_images("lvl_3"), self.change_to_level_three)
        button_lvl_three.set_topleft((61 * GUI_SCALE, 124 * GUI_SCALE))

        formatted_leaderboard=ServerConnector.get_leaderboards_formatted(1)

        # leaderboards element
        self.leaderboards_element = create_leaderboards_element(formatted_leaderboard)

        # leaderboards bg
        leaderboards_bg = thorpy.Background()
        leaderboards_bg.set_topleft((79 * GUI_SCALE, 55 * GUI_SCALE))
        leaderboards_bg.set_size(size=(150 * GUI_SCALE, 121 * GUI_SCALE))
        leaderboards_bg.set_image(res.load_leaderboards_menu_background())

        self.container = thorpy.Ghost(
            elements=[button_leaderboards, button_lvl_one, button_lvl_two, button_lvl_three, leaderboards_bg,
                      self.leaderboards_element])
        self.menu = thorpy.Menu(self.container)
        for leaderboard_records_element in self.menu.get_population():
            leaderboard_records_element.surface = screen

    def launch_main_menu(self):
        self.is_opened = False
        menu = main_menu.MainMenu(self.res, self.screen, self.clock)
        menu.launch()

    def change_to_level_one(self):
        self.change_leaderboard_level(1)

    def change_to_level_two(self):
        self.change_leaderboard_level(2)

    def change_to_level_three(self):
        self.change_leaderboard_level(3)

    def change_leaderboard_level(self, level: int):
        print("change level: " + str(level))
        formatted_leaderboard=ServerConnector.get_leaderboards_formatted(level)
        element= self.leaderboards_element.get_elements()[0]
        element.set_text(formatted_leaderboard)
        resize_leaderboard_element_text(element)



    def launch(self):
        while self.is_opened:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_opened = False
                    break
                self.menu.react(event)
            self.background_top.update(dt)
            self.background_bottom.update(dt)
            self.background_top.draw(self.screen)
            self.background_bottom.draw(self.screen)
            self.container.blit()
            self.container.update()
            pygame.display.flip()
