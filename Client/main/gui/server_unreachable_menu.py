import pygame
import thorpy

from main.gui import gui_utils, leaderboards_menu
from main.gui import login_menu
from main.gui import main_menu
from main.gui.constants import FPS, GUI_SCALE, YELLOW_LIGHT, ACTION_ENTRY, ACTION_GET_USER, RED_CONTRAST, \
    ACTION_GET_LEADERBOARDS
from main.gui.gui_utils import create_button
from main.gui.main_menu_utils import ScrollingBackgroundHorizontal
from main.server_connector.server_connector import ServerConnector
from main.server_connector.server_errors_handler import ServerErrorsHandler


class ServerUnreachableMenu:

    # todo pass action
    #action: entry, ...
    def __init__(self, res, screen, clock,action:str, action_arg = 1):
        self.action = action
        self.action_arg = action_arg
        self.is_opened = True
        self.res = res
        self.screen = screen
        self.clock = clock
        self.background_image = res.load_no_internet_background()
        scroll_width = self.background_image.get_width()
        self.background_left = ScrollingBackgroundHorizontal(self.background_image, scroll_width * (-1), 0,
                                                             scroll_width)
        self.background_right = ScrollingBackgroundHorizontal(self.background_image, 0, 0, scroll_width)

        button_retry = create_button(res.load_button_images("retry"), self.retry)
        button_retry.set_topleft((102 * GUI_SCALE, 72 * GUI_SCALE))

        button_close = create_button(res.load_button_images("close"), self.close)
        button_close.set_topleft((102 * GUI_SCALE, 136 * GUI_SCALE))

        text_header = gui_utils.create_text("Server unreachable", (15 * GUI_SCALE, 19 * GUI_SCALE), YELLOW_LIGHT, 30 * GUI_SCALE)
        self.text_error = gui_utils.create_text(action, (0,0), RED_CONTRAST,
                                                14 * GUI_SCALE)
        self.text_error.set_center_pos((151 * GUI_SCALE, 59 * GUI_SCALE))

        self.container = thorpy.Ghost(elements=[button_retry,button_close, text_header,self.text_error])
        self.menu = thorpy.Menu(self.container)
        for element in self.menu.get_population():
            element.surface = screen

    def retry(self):

        if self.action == ACTION_ENTRY:
            self.process_action_entry()
        if self.action == ACTION_GET_USER:
            self.process_get_user()
        if self.action == ACTION_GET_LEADERBOARDS:
            self.process_get_leaderboards()

    def process_get_user(self):
        (is_success, user) = ServerErrorsHandler.try_get_user()
        if is_success:
            self.is_opened = False
            menu = main_menu.MainMenu(self.res, self.screen, self.clock, user)
            menu.launch()
        else:
            self.text_error.set_text(ACTION_GET_USER)
            self.text_error.set_center_pos((151 * GUI_SCALE, 59 * GUI_SCALE))

    def process_get_leaderboards(self):
        (is_success,formatted_leaderboards)=ServerErrorsHandler.try_get_leaderboards_formatted(self.action_arg)
        if is_success:
            self.is_opened = False
            leaderboards = leaderboards_menu.LeaderboardsMenu(self.res, self.screen, self.clock, formatted_leaderboards)
            leaderboards.launch()
        else:
            self.text_error.set_text(ACTION_GET_LEADERBOARDS)
            self.text_error.set_center_pos((151 * GUI_SCALE, 59 * GUI_SCALE))

    def process_action_entry(self):
        (is_success, is_logged_in) = ServerErrorsHandler.try_is_logged_in()
        if is_success:
            self.is_opened=False
            if is_logged_in:
                menu = main_menu.MainMenu(self.res, self.screen, self.clock)
                menu.launch()
            else:
                login = login_menu.LoginMenu(self.res, self.screen, self.clock)
                login.launch()
        else:
            self.text_error.set_text(ACTION_ENTRY)
            self.text_error.set_center_pos((151 * GUI_SCALE, 59 * GUI_SCALE))

    def close(self):
        pygame.quit()

    def launch(self):
        while self.is_opened:
            dt = self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_opened = False
                    break
                self.menu.react(event)
            self.background_left.update(dt)
            self.background_right.update(dt)
            self.background_left.draw(self.screen)
            self.background_right.draw(self.screen)
            self.container.blit()
            self.container.update()
            pygame.display.flip()
