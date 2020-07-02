import pygame
import thorpy
from main.gui.constants import FPS, GUI_SCALE, ACTION_GET_LEADERBOARDS
from main.gui.main_menu import main_menu
from main.gui.gui_utils import create_button
from main.gui.leaderboards_menu.leaderboards_menu_utils import ScrollingBackgroundVertical, create_leaderboards_element
from main.gui.server_unreachable_menu.server_unreachable_menu import ServerUnreachableMenu
from main.server_connector.server_errors_handler import ServerErrorsHandler


class LeaderboardsMenu:

    def __init__(self, res, screen, clock, formatted_leaderboards=None):
        self.container = None
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

        # get from server or from constructor arg
        if formatted_leaderboards is None:
            self.leaderboards_element = create_leaderboards_element("\n")
            self.show_leaderboard_level(1)
        else:
            self.leaderboards_element = create_leaderboards_element(formatted_leaderboards)

        # leaderboards bg
        leaderboards_bg = thorpy.Background()
        leaderboards_bg.set_topleft((79 * GUI_SCALE, 55 * GUI_SCALE))
        leaderboards_bg.set_size(size=(150 * GUI_SCALE, 121 * GUI_SCALE))
        leaderboards_bg.set_image(res.load_leaderboards_menu_background())

        self.container = thorpy.Ghost(
            elements=[button_leaderboards, button_lvl_one, button_lvl_two, button_lvl_three, leaderboards_bg,
                      self.leaderboards_element])
        self.menu = thorpy.Menu(self.container)
        for element in self.menu.get_population():
            element.surface = screen

    def launch_main_menu(self):
        self.is_opened = False
        menu = main_menu.MainMenu(self.res, self.screen, self.clock)
        menu.launch()

    def change_to_level_one(self):
        self.show_leaderboard_level(1)

    def change_to_level_two(self):
        self.show_leaderboard_level(2)

    def change_to_level_three(self):
        self.show_leaderboard_level(3)

    def show_leaderboard_level(self, level: int):
        print("change level: " + str(level))
        self.is_opened, formatted_leaderboard = ServerErrorsHandler.try_get_leaderboards_formatted(level)
        if formatted_leaderboard is None:
            no_internet_menu = ServerUnreachableMenu(self.res, self.screen, self.clock, ACTION_GET_LEADERBOARDS, level)
            no_internet_menu.launch()
        else:
            if not self.container is None:
                self.container.remove_elements([self.leaderboards_element])
                self.leaderboards_element = create_leaderboards_element(formatted_leaderboard)
                self.leaderboards_element.surface = self.screen
                self.container.add_element(self.leaderboards_element)
                self.menu.remove_from_population(self.container)
                self.menu.add_to_population(self.container)
            else:
                self.leaderboards_element = create_leaderboards_element(formatted_leaderboard)

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
