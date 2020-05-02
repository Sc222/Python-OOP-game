import math
import os

import pygame
from pygame.constants import MOUSEBUTTONDOWN, BUTTON_LEFT
from pygame.rect import Rect

from main.gui.constants import *
from main.gui.game_utils import Parser, Resources, Camera
from main.gui.gui_overlay import GameOverlay
from main.gui.player import PlayerSprite, Player, CreatureState

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)  # set the display mode, window title and FPS clock
display = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))  # todo surface size - game x*32 +16 , game y*16+32
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()
# todo move large setup to fie
resources = Resources("data", SCALE)
parser = Parser(SCALE)
center_x = display.get_rect().centerx
center_y = display.get_rect().centery
playerSprite = PlayerSprite((center_x - PLAYER_SIZE / 2, center_y - PLAYER_SIZE / 2), (PLAYER_SIZE, PLAYER_SIZE),
                            resources.player_imgs)
playerCollideRect = Rect((center_x - PLAYER_COLLIDE_WIDTH / 2,
                          center_y - PLAYER_COLLUDE_HEIGHT / 2 + PLAYER_SIZE / 2 - 5 * SCALE, PLAYER_COLLIDE_WIDTH,
                          PLAYER_COLLUDE_HEIGHT))
playerDraw = pygame.sprite.RenderPlain(playerSprite)
player = Player("sc222", 10, 20, 20, 30, 5, 1, 0, playerSprite, playerCollideRect)

camera = Camera(0, 0, Rect(300, 200, 300, 200))  # todo debug size for render demo

gui = GameOverlay(3, player.hp, player.mana, center_x,
                  center_y)  # todo store items somewhere #gui scale is smaller than game scale

# todo это временно, в финальной версии уровень будет грузиться из базы данных
map_bg = open(os.path.join("demo", "background.txt"), "r").read().split()
map_terrain = open(os.path.join("demo", "terrain.txt"), "r").read().split()

# todo 2d list for storing map obstacles
print(center_x, center_y)
background_draw_ls = parser.parse_map_to_static_draw_objects(resources.bg_imgs, map_bg, center_x, center_y)
terrain_draw_ls = parser.parse_map_to_static_draw_objects(resources.terrain_imgs, map_terrain, center_x, center_y,
                                                          TERRAIN_SHIFT)


def update():
    camera.update(-playerSprite.velocity.x, -playerSprite.velocity.y)
    playerSprite.update(dt, playerState, camera)
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

    # todo ЭЛЕМЕНТЫ ВНЕ КАМЕРЫ НЕ ДОЛЖНЫ РИСОВАТЬСЯ!!!
    # todo draw clouds
    # todo player should be drawed in priority before far objets and after close objects
    # todo (использовать ordered render из примера)
    # todo player isometric speed IS DIFFERENT (use cos \ sin \ web)

    playerDraw.draw(display)
    move_rect = player.collide_rect.move(playerSprite.velocity.x * MOVE_COLLIDE_RECT_OFFSET,
                                         playerSprite.velocity.y * MOVE_COLLIDE_RECT_OFFSET)
    pygame.draw.rect(display, PL, move_rect, 5)
    pygame.draw.rect(display, DEBUG, camera.visible_rect, 5)
    gui.draw(display, player.hp, player.mana, None)  # todo store items somewhere
    screen.blit(display, (0, 0))


draw()
playerState = CreatureState.idle
is_attack = 0

while True:
    mousex, mousey = pygame.mouse.get_pos()

    xx = playerSprite.x - 210 + camera.x_shift
    yy = playerSprite.y - 70 + camera.y_shift

    cellx = math.floor((2 * yy + xx - center_x - center_y + 5 * TILEWIDTH_HALF) / (2 * TILEWIDTH_HALF))
    celly = math.floor((2 * yy - xx + center_x - center_y + 3 * TILEWIDTH_HALF) / (2 * TILEWIDTH_HALF))
    print(cellx, celly)

    dt = clock.tick(FPS)

    if not is_attack:
        mousex, mousey = pygame.mouse.get_pos()

        xx = mousex - center_x + camera.x_shift
        yy = mousey - center_y / 2 + camera.y_shift

        cellx = math.floor((xx / TILEWIDTH_HALF + yy / TILEHEIGHT_HALF) / 2)
        celly = math.floor((yy / TILEHEIGHT_HALF - (xx / TILEWIDTH_HALF)) / 2)
        print(cellx, celly)

        playerDx = playerSprite.rect.centerx - mousex
        playerDy = playerSprite.rect.centery - mousey
        if abs(playerDx) > MOUSE_IDLE_DELTA:
            playerSprite.velocity.x = -playerDx
        else:
            playerSprite.velocity.x = 0

        if abs(playerDy) > MOUSE_IDLE_DELTA:
            playerSprite.velocity.y = -playerDy
        else:
            playerSprite.velocity.y = 0

        if playerSprite.velocity.x != 0 or playerSprite.velocity.y != 0:
            playerState = CreatureState.walk
            playerSprite.velocity.normalize_ip()
            playerSprite.velocity *= player.speed
            for terr in filter(camera.is_visible, terrain_draw_ls):
                move_rect_x = player.collide_rect.move(playerSprite.velocity.x * MOVE_COLLIDE_RECT_OFFSET,
                                                       0)
                move_rect_y = player.collide_rect.move(0,
                                                       playerSprite.velocity.y * MOVE_COLLIDE_RECT_OFFSET)
                collide_x = move_rect_x.colliderect(terr.get_taken_place_rect(SCALE))
                collide_y = move_rect_y.colliderect(terr.get_taken_place_rect(SCALE))
                if collide_x:
                    print("collides x")
                    playerSprite.velocity.x = 0
                if collide_y:
                    print("collides y")
                    playerSprite.velocity.y = 0
                if collide_x and collide_y:
                    playerState = CreatureState.idle

        else:
            playerState = CreatureState.idle

    if is_attack and playerSprite.is_animation_end():
        is_attack = False

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            if event.button == BUTTON_LEFT:
                is_attack = True
                playerSprite.velocity.x = 0
                playerSprite.velocity.y = 0
                playerState = CreatureState.attack

    update()
    draw()
    pygame.display.flip()
