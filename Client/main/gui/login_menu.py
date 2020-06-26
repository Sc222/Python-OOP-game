import pygame
import thorpy

from main.gui import game_main, leaderboards_menu
from main.gui.constants import FPS, GAME_NAME, MAIN_MENU_HEADER, GUI_SCALE
from main.gui.gui_utils import create_button, render_text
from main.gui.main_menu_utils import ScrollingBackgroundHorizontal, PlayerMenu


class LoginMenu:

    def __init__(self, res, screen, clock):
        self.is_opened = True
        self.resources = res
        self.screen = screen
        self.clock = clock
        self.background_image = res.load_login_background()
        scroll_width = self.background_image.get_width()
        self.background_left = ScrollingBackgroundHorizontal(self.background_image, scroll_width * (-1), 0,
                                                             scroll_width)
        self.background_right = ScrollingBackgroundHorizontal(self.background_image, 0, 0, scroll_width)

        button_exit_login = create_button(res.load_button_images("exit_login_menu"), self.exit_login_menu)
        button_exit_login.set_topleft((68 * GUI_SCALE, 24 * GUI_SCALE))

        login_bg = thorpy.Background()
        login_bg.set_topleft((79 * GUI_SCALE, 55 * GUI_SCALE))
        login_bg.set_size(size=(150 * GUI_SCALE, 121 * GUI_SCALE))
        login_bg.set_image(res.load_login_menu_background())

        self.container = thorpy.Ghost(elements=[button_exit_login,login_bg])
        self.menu = thorpy.Menu(self.container)
        for element in self.menu.get_population():
            element.surface = screen

    def exit_login_menu(self):
        # TODO QUIT GAME HERE
        print("quit game")
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
