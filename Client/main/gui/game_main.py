import os
import pygame
import requests
import  json
from  main.gui.DTO_models import level_from_json,map_obj_from_json, monster_obj_from_json
from pygame.rect import Rect
from main.gui import main_menu
from main.gui.constants import *
from main.gui.game_utils import Parser, Camera
from main.gui.gui_overlay import GameOverlay
from main.gui.player import PlayerSprite, Player


class Game:

    def __init__(self, res, screen, clock):
        self.is_opened = True
        self.res = res
        self.screen = screen
        self.clock = clock
        self.display = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.c_x = self.display.get_rect().centerx
        self.c_y = self.display.get_rect().centery

        # todo игрок всегда в центре экрана
        self.playerSprite = PlayerSprite(
            (self.c_x - PL_SIZE / 2, self.c_y - PL_SIZE / 2), (PL_SIZE, PL_SIZE), res.load_player())
        player_collide_rect = Rect((self.c_x - PL_COLLIDE_W / 2,
                                    self.c_y - PL_COLLIDE_H / 2 + PL_SIZE / 2 - 5 * SCALE,
                                    PL_COLLIDE_W,
                                    PL_COLLIDE_H))

        self.player = Player("sc222", 10, 20, 20, 30, 5, 1, 0, self.playerSprite, player_collide_rect)

        # todo debug size for render demo
        # self.camera = Camera(0, 0, Rect(300, 200, 300, 200))
        self.camera = Camera(0, 0, Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))

        # todo store items somewhere
        self.gui = GameOverlay(self.res.load_game_overlay_images(), self.player.hp, self.player.mana, self.c_x,
                               self.c_y)

        # todo change hp and mana for demo
        self.player.hp = 7
        self.player.mana = 17

        # todo это временно, в финальной версии уровень будет грузиться из базы данных
        level_response = requests.get('http://127.0.0.1:5000/level/1');
        level_dict = json.loads(level_response.text)
        backgrounds = [map_obj_from_json(o['x'],o['y'],o['name']) for o in level_dict['backgrounds']]
        terrains = [map_obj_from_json(o['x'],o['y'],o['name']) for o in level_dict['terrains']]
        monsters = [monster_obj_from_json(o['x'],o['y'],o['name'],o['hp'],o['attack'],o['defemce'])
                    for o in level_dict['monsters']]
        level = level_from_json(backgrounds,monsters,terrains)
        #map_bg = open(os.path.join(self.res.directory, "demo", "background.txt"), "r").read().split()
        #map_terrain = open(os.path.join(self.res.directory, "demo", "terrain.txt"), "r").read().split()
        parser = Parser()
        self.background_draw_ls = parser.map_to_draw_objects_from_server(res.load_backgrounds(),level.backgrounds,self.c_x,self.c_y)
        self.terrain_draw_ls = parser.map_to_draw_objects_from_server(res.load_terrain(), level.terrains, self.c_x, self.c_y,TERRAIN_SHIFT)
        #self.background_draw_ls = parser.map_to_draw_objects(res.load_backgrounds(), map_bg, self.c_x, self.c_y)
        #self.terrain_draw_ls = parser.map_to_draw_objects(res.load_terrain(), map_terrain, self.c_x, self.c_y,
                                                          #TERRAIN_SHIFT)

    def launch_main_menu(self):
        self.is_opened = False
        menu = main_menu.MainMenu(self.res, self.screen, self.clock)
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
        self.camera.update(-self.player.velocity.x, -self.player.velocity.y)
        self.player.update(dt)
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

        # todo debug draw
        # move_rect = self.player.collide_rect.move(self.player.velocity.x * MOVE_COLLIDE_RECT_OFFSET,
        #                                          self.player.velocity.y * MOVE_COLLIDE_RECT_OFFSET)
        # pygame.draw.rect(self.display, PL, move_rect, 5)
        # pygame.draw.rect(self.display, DEBUG, self.camera.visible_rect, 5)

        self.gui.draw(self.display, self.player.hp, self.player.mana, None)  # todo store items somewhere
        self.screen.blit(self.display, (0, 0))

    def launch(self):
        while self.is_opened:
            # xx = playerSprite.x - 210 + camera.x_shift
            # yy = playerSprite.y - 70 + camera.y_shift
            # cellx = math.floor((2 * yy + xx - center_x - center_y + 5 * TILEWIDTH_HALF) / (2 * TILEWIDTH_HALF))
            # celly = math.floor((2 * yy - xx + center_x - center_y + 3 * TILEWIDTH_HALF) / (2 * TILEWIDTH_HALF))
            # print(cellx, celly)
            dt = self.clock.tick(FPS)
            self.process_input()
            self.update(dt)
            self.draw()
            pygame.display.flip()
