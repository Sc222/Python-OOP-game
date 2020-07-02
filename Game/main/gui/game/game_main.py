import os

import pygame
from pygame.rect import Rect
from main.gui import main_menu
from main.gui.constants import *
from main.gui.game.game_utils import Parser, Camera, Resources
from main.gui.game.gui_overlay import GameOverlay
from main.gui.game.monster import MonsterSprite, Monster
from main.gui.game.player import PlayerSprite, Player
from main.server_connector.server_connector import ServerConnector


# TODO !!! CHECK OBJECTS AND MAP BORDERS COLLISION USING COORDINATES, NOT RECTANGLES
# todo spawn next lvl teleporter and generate map, make lots of locations and boss in the end
# todo (like risk of rain but isometric)
class Game:

    def __init__(self, res, screen, clock):
        self.is_opened = True
        self.res = res
        self.screen = screen
        self.clock = clock
        self.display = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.c_x = self.display.get_rect().centerx
        self.c_y = self.display.get_rect().centery

        # todo debug size for render demo
        # self.camera = Camera(0, 0, Rect(300, 200, 300, 200))
        self.camera = Camera(0, 0, Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        # todo игрок всегда в центре экрана
        self.playerSprite = PlayerSprite(
            (self.c_x - PL_SIZE / 2, self.c_y - PL_SIZE / 2), (PL_SIZE, PL_SIZE), res.load_creature(Resources.player))
        player_collide_rect = Rect((self.c_x - PL_COLLIDE_W / 2,
                                    self.c_y - PL_COLLIDE_H / 2 + PL_SIZE / 2 - 5 * SCALE,
                                    PL_COLLIDE_W,
                                    PL_COLLIDE_H))
        # todo get from bd, pass as constructor params
        self.player = Player("sc222", 10, 20, 20, 30, 6, 1, 0, self.playerSprite, player_collide_rect)

        # todo store items somewhere
        self.gui = GameOverlay(self.res.load_game_overlay_images(), self.player.hp, self.player.mana, self.c_x,
                               self.c_y)

        # todo change hp and mana for demo
        self.player.hp = 7
        self.player.mana = 17

        # level = ServerConnector.get_level(1)

        # TODO !!!CREATE MONSTERS!!!
        # print(level.monsters)
        # for monster in level.monsters:
        #    print(monster.name)
        # TODO пример спавна, это нужно вынести в метод
        # todo working map coordinates -> screen coordinates
        monster_x = 0
        monster_y = 0
        x_shift = self.c_x - M_WIDTH / 2  # '''self.c_x -'''
        y_shift = - M_HEIGHT/2+CREATURE_SHIFT  # '''self.c_y * 0.5'''
        centered_x = x_shift + (monster_x - monster_y) * TILE_SIZE_HALF
        centered_y = y_shift + (monster_x + monster_y) * 0.5 * TILE_SIZE_HALF

        self.monsterSprite = MonsterSprite(
            (centered_x, centered_y), (M_WIDTH, M_HEIGHT), res.load_creature(Resources.monster_mushroom))

        monster_collide_rect = self.monsterSprite.rect.inflate(-70 * SCALE, -40 * SCALE)
        monster_collide_rect.move_ip(0, self.monsterSprite.rect.height / 2 - monster_collide_rect.height - 5 * SCALE)

        self.monster = Monster("mushroom", 100, 20, 20, 30, 3, 1, 0, self.monsterSprite, monster_collide_rect,
                               self.camera)

        parser = Parser()
        # todo load level from server
        # self.background_draw_ls = parser.map_to_draw_objects_from_server(res.load_backgrounds(), level.backgrounds,
        #                                                                 self.c_x, self.c_y)
        # self.terrain_draw_ls = parser.map_to_draw_objects_from_server(res.load_terrain(), level.terrains, self.c_x,
        #                                                              self.c_y, TERRAIN_SHIFT)

        # TODO MONSTERS TO DRAW OBJECTS
        # self.monsters_draw_ls = parser.monsters_to_draw_objects(res.load_creatures(), level.monsters, self.c_x,
        #
        #                                                        self.c_y)
        # todo load level from text file
        map_bg = open(os.path.join(self.res.directory, "demo", "background.txt"), "r").read().split()
        map_terrain = open(os.path.join(self.res.directory, "demo", "terrain.txt"), "r").read().split()
        self.background_draw_ls = parser.map_to_draw_objects(res.load_backgrounds_text(), map_bg, self.c_x, self.c_y)
        self.terrain_draw_ls = parser.map_to_draw_objects(res.load_terrain_text(), map_terrain, self.c_x, self.c_y,
                                                          TERRAIN_SHIFT)

    def launch_main_menu(self):
        self.is_opened = False
        menu = main_menu.main_menu.MainMenu(self.res, self.screen, self.clock)
        menu.launch()

    def process_input(self):
        self.player.perform_movement(pygame.mouse.get_pos(), filter(self.camera.is_visible, self.terrain_draw_ls))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_opened = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.launch_main_menu()
                # todo pause menu
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    self.player.perform_attack()

    def update(self, dt):
        player_pos = (self.player.collide_rect.centerx, self.player.collide_rect.centery)
        self.monster.perform_movement(player_pos, filter(self.camera.is_visible, self.terrain_draw_ls), self.camera)
        self.camera.update(-self.player.velocity.x, -self.player.velocity.y)
        self.player.update(dt)
        self.monster.update(dt)

        # TODO CHECK HIT FOR MONSTERS AND PLAYERS
        self.monster.check_hit(self.player, self.camera)

        for background in self.background_draw_ls:
            background.update(self.camera)
        for terrain in self.terrain_draw_ls:
            terrain.update(self.camera)

    def draw(self):
        self.display.fill(SKY)

        for background in filter(self.camera.is_visible, self.background_draw_ls):
            background.draw(self.display)

        for terrain in filter(self.camera.is_visible, self.terrain_draw_ls):
            terrain.draw(self.display)
            # todo debug draw
            # pygame.draw.rect(self.display, TR, terrain.get_taken_place_rect(SCALE), 5)

        # todo draw clouds
        # todo player should be drawed in priority before far objects and after close objects
        # todo (использовать ordered render)
        # TODO МЕНЮ ПАУЗЫ

        self.playerSprite.draw(self.display)

        self.monsterSprite.draw(self.display, self.camera)
        atk_rect = self.player.get_attack_rect()
        pygame.draw.rect(self.display, PL, atk_rect, 5)
        pygame.draw.rect(self.display, DEBUG, self.monster.get_hit_rect(self.camera), 5)

        self.gui.draw(self.display, self.player.hp, self.player.mana, None)  # todo store items somewhere
        self.screen.blit(self.display, (0, 0))

    def launch(self):
        while self.is_opened:
            dt = self.clock.tick(FPS)
            self.process_input()
            # self.update(dt)
            self.draw()
            pygame.display.flip()
