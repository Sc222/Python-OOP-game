import pygame
import thorpy
from tabulate import tabulate
from main.gui.constants import FPS, WHITE, GUI_SCALE
from main.gui import main_menu
from main.gui.leaderboards_menu_utils import ScrollingBackgroundVertical
from main.gui.main_menu_utils import create_button


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

        # todo ЭТИ ДАННЫЕ ИЗ БД
        formatted_leaderboard = tabulate(
            [
                ["Sc222", "19", "223132"],
                ["Balandin", "17", "190200"],
                ["Danil", "17", "180200"],
                ["Vlad M", "16", "170200"],
                ["Yakiy Pes", "16", "160200"],
                ["Andrey", "15", "159200"],
                ["Vasya123", "14", "149200"],
                ["VasYa", "14", "140200"],
                ["VaSSya", "13", "139200"],
                ["VasYaN", "12", "134200"],
                ["Vasya", "11", "120200"],
                ["Ivan", "10", "11020"],
            ],
            ["Name", "Level", "Score"],
            tablefmt="simple")
        print(formatted_leaderboard)
        leaderboard_entries = formatted_leaderboard.splitlines()

        elements = []
        # add elements
        for entry in leaderboard_entries:
            element = thorpy.make_text(entry)
            elements.append(element)

        # style elements
        for e in elements:
            e.center()
            e.set_font_color(WHITE)
            e.set_size((132 * GUI_SCALE, 0))
            e.set_font_size(25)
            e.set_font("Determination Mono(RUS BY LYAJK")

        # leaderboards bg
        leaderboards_bg = thorpy.Background()
        leaderboards_bg.set_topleft((79 * GUI_SCALE, 55 * GUI_SCALE))
        leaderboards_bg.set_size(size=(150 * GUI_SCALE, 121 * GUI_SCALE))
        leaderboards_bg.set_image(res.load_leaderboards_menu_background())

        # leaderboard_container
        leaderboard_box = thorpy.Box(elements=elements)
        leaderboard_box.set_topleft((92 * GUI_SCALE, 62 * GUI_SCALE))
        leaderboard_box.scale_to_content()
        leaderboard_box.set_size((132 * GUI_SCALE, 109 * GUI_SCALE))
        leaderboard_box.add_lift()

        leaderboard_box.set_main_color((220, 220, 220, 0))  # set box color and opacity
        self.container = thorpy.Ghost(elements=[button_leaderboards, leaderboards_bg, leaderboard_box])
        self.menu = thorpy.Menu(self.container)
        for element in self.menu.get_population():
            element.surface = screen

    def launch_main_menu(self):
        self.is_opened = False
        menu = main_menu.MainMenu(self.res, self.screen, self.clock)
        menu.launch()

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
