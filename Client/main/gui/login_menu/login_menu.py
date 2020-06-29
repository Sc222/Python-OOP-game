import pygame
import thorpy

from main.gui import gui_utils
from main.gui.constants import FPS, GUI_SCALE, WHITE, RED
from main.gui.gui_utils import create_button
from main.gui.main_menu import main_menu
from main.gui.main_menu.main_menu_utils import ScrollingBackgroundHorizontal
from main.server_connector.server_connector import ServerConnector


class LoginMenu:

    def __init__(self, res, screen, clock):
        self.is_opened = True
        self.res = res
        self.screen = screen
        self.clock = clock
        self.background_image = res.load_login_background()
        scroll_width = self.background_image.get_width()
        self.background_left = ScrollingBackgroundHorizontal(self.background_image, scroll_width * (-1), 0,
                                                             scroll_width)
        self.background_right = ScrollingBackgroundHorizontal(self.background_image, 0, 0, scroll_width)

        button_exit_login = create_button(res.load_button_images("exit_login_menu"), self.exit_login_menu)
        button_exit_login.set_topleft((68 * GUI_SCALE, 24 * GUI_SCALE))

        button_login = create_button(res.load_button_images("login"), self.login)
        button_login.set_topleft((95 * GUI_SCALE, 146 * GUI_SCALE))

        button_register = create_button(res.load_button_images("register"), self.register)
        button_register.set_topleft((149 * GUI_SCALE, 146 * GUI_SCALE))

        text_username = gui_utils.create_text("Username:", (110 * GUI_SCALE, 65 * GUI_SCALE), WHITE, 10 * GUI_SCALE)
        text_password = gui_utils.create_text("Password:", (110 * GUI_SCALE, 102 * GUI_SCALE), WHITE, 10 * GUI_SCALE)
        self.text_error = gui_utils.create_text("", (108 * GUI_SCALE, 135 * GUI_SCALE), RED, 8 * GUI_SCALE)

        self.inserter_username = gui_utils.create_inserter(res)
        inserter_username_container = thorpy.Ghost(elements=[self.inserter_username])
        inserter_username_container.set_topleft((108 * GUI_SCALE, 76 * GUI_SCALE))

        self.inserter_password = gui_utils.create_inserter(res)
        inserter_password_container = thorpy.Ghost(elements=[self.inserter_password])
        inserter_password_container.set_topleft((108 * GUI_SCALE, 113 * GUI_SCALE))

        login_bg = thorpy.Background()
        login_bg.set_topleft((79 * GUI_SCALE, 55 * GUI_SCALE))
        login_bg.set_size(size=(150 * GUI_SCALE, 121 * GUI_SCALE))
        login_bg.set_image(res.load_login_menu_background())

        self.container = thorpy.Ghost(elements=[login_bg, button_exit_login, button_login, button_register,
                                                text_username,
                                                text_password,
                                                self.text_error,
                                                inserter_username_container,
                                                inserter_password_container])
        self.menu = thorpy.Menu(self.container)
        for element in self.menu.get_population():
            element.surface = screen

    def exit_login_menu(self):
        print("quit game")
        pygame.quit()

    def login(self):
        username = self.inserter_username.get_value()
        password = self.inserter_password.get_value()
        print("login: " + username + " " + password)
        res = ServerConnector.login(username, password)
        if res[0] != 200:
            self.text_error.set_font_color(RED)
            self.text_error.set_text(res[1])
        else:
            self.text_error.set_text("")
            self.is_opened = False
            main_menu = main_menu.MainMenu(self.res, self.screen, self.clock)
            main_menu.launch()

    def register(self):
        username = self.inserter_username.get_value()
        password = self.inserter_password.get_value()
        print("register: " + username + " " + password)
        res = ServerConnector.register(username, password)
        if res[0] != 200:
            self.text_error.set_font_color(RED)
            self.text_error.set_text(res[1])
        else:
            self.text_error.set_font_color(WHITE)
            self.text_error.set_text(res[1])

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
