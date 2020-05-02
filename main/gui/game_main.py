import os

import pygame
from pygame.constants import MOUSEBUTTONDOWN, BUTTON_LEFT
from pygame.rect import Rect

from main.gui.constants import *
from main.gui.game_utils import Parser, Resources, Camera
from main.gui.gui_overlay import GameOverlay
from main.gui.player import PlayerSprite, Player

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)  # set the display mode, window title and FPS clock
display = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Python OOP Game')
FPSCLOCK = pygame.time.Clock()
# todo move large setup to fie
resources = Resources("data")
parser = Parser()
center_x = display.get_rect().centerx
center_y = display.get_rect().centery
playerSprite = PlayerSprite((center_x - PLAYER_SIZE / 2, center_y - PLAYER_SIZE / 2), (PLAYER_SIZE, PLAYER_SIZE),
                            resources.load_player())
playerCollideRect = Rect((center_x - PLAYER_COLLIDE_WIDTH / 2,
                          center_y - PLAYER_COLLUDE_HEIGHT / 2 + PLAYER_SIZE / 2 - 5 * SCALE, PLAYER_COLLIDE_WIDTH,
                          PLAYER_COLLUDE_HEIGHT))

player = Player("sc222", 10, 20, 20, 30, 5, 1, 0, playerSprite, playerCollideRect)


camera = Camera(0, 0, Rect(300, 200, 300, 200))  # todo debug size for render demo

gui = GameOverlay(GUI_SCALE, player.hp, player.mana, center_x,
                  center_y)  # todo store items somewhere #gui scale is smaller than game scale

#todo change hp and mana for demo
player.hp=7
player.mana=17

# todo это временно, в финальной версии уровень будет грузиться из базы данных
map_bg = open(os.path.join("demo", "background.txt"), "r").read().split()
map_terrain = open(os.path.join("demo", "terrain.txt"), "r").read().split()

# todo 2d list for storing map obstacles
print(center_x, center_y)
background_draw_ls = parser.parse_map_to_static_draw_objects(resources.load_backgrounds(), map_bg, center_x, center_y)
terrain_draw_ls = parser.parse_map_to_static_draw_objects(resources.load_terrain(), map_terrain, center_x, center_y,
                                                          TERRAIN_SHIFT)


def process_input():
    player.perform_movement(pygame.mouse.get_pos(), filter(camera.is_visible, terrain_draw_ls))

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT:
                player.perform_attack()


def update(dt):
    camera.update(-player.velocity.x, -player.velocity.y)
    player.update(dt)
    for background in background_draw_ls:
        background.update(camera)
    for terrain in terrain_draw_ls:
        terrain.update(camera)


def draw():
    display.fill(SKY)

    # todo here
    for background in filter(camera.is_visible, background_draw_ls):
        background.draw(display)

    for terrain in filter(camera.is_visible, terrain_draw_ls):
        terrain.draw(display)
        pygame.draw.rect(display, TR, terrain.get_taken_place_rect(SCALE), 5)

    # todo draw clouds
    # todo player should be drawed in priority before far objects and after close objects
    # todo (использовать ordered render из примера)

    playerSprite.draw(display)
    move_rect = player.collide_rect.move(player.velocity.x * MOVE_COLLIDE_RECT_OFFSET,
                                         player.velocity.y * MOVE_COLLIDE_RECT_OFFSET)
    pygame.draw.rect(display, PL, move_rect, 5)
    pygame.draw.rect(display, DEBUG, camera.visible_rect, 5)
    gui.draw(display, player.hp, player.mana, None)  # todo store items somewhere
    screen.blit(display, (0, 0))


draw()


while True:
    # xx = playerSprite.x - 210 + camera.x_shift
    # yy = playerSprite.y - 70 + camera.y_shift
    # cellx = math.floor((2 * yy + xx - center_x - center_y + 5 * TILEWIDTH_HALF) / (2 * TILEWIDTH_HALF))
    # celly = math.floor((2 * yy - xx + center_x - center_y + 3 * TILEWIDTH_HALF) / (2 * TILEWIDTH_HALF))
    # print(cellx, celly)
    dt = clock.tick(FPS)
    process_input()
    update(dt)
    draw()
    pygame.display.flip()
