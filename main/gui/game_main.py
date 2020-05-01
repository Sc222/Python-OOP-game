import math
import os
import pygame
from game_utils import Resources
from game_utils import Parser
from game_utils import Camera
from player import PlayerSprite
from player import CreatureState
from player import Player
from pygame.constants import MOUSEBUTTONDOWN, BUTTON_LEFT

from gui_overlay import GameOverlay
from pygame.rect import Rect

pygame.init()

FPS = 60
clock = pygame.time.Clock()
TERRAIN_SHIFT = -6
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
SCALE = 5
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)  # set the display mode, window title and FPS clock
display = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))  # todo surface size - game x*32 +16 , game y*16+32
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

SKY = (0, 205, 249)
DEBUG = (255, 0, 64)
PL = (0,255,0)
TR=(0,0,255)

TILECOLLIDEWIDTH = 21 * SCALE
TILEWIDTH = 32 * SCALE  # holds the tile width and height
TILEHEIGHT = 32 * SCALE
TILEHEIGHT_HALF = TILEHEIGHT / 2
TILEWIDTH_HALF = TILEWIDTH / 2

MOUSE_IDLE_DELTA = 40  # когда разница в координатах меньше этого числа игрок стоит на месте

# todo move large setup to fie


resources = Resources("data", SCALE)
parser = Parser(SCALE)

center_x = display.get_rect().centerx
center_y = display.get_rect().centery

PLAYER_SIZE=24*SCALE
PLAYER_COLLIDE_WIDTH= 6 * SCALE
PLAYER_COLLUDE_HEIGHT=5*SCALE
playerSprite = PlayerSprite((center_x - PLAYER_SIZE / 2, center_y -PLAYER_SIZE / 2), (PLAYER_SIZE, PLAYER_SIZE),
                            resources.player_imgs)
playerCollideRect = Rect((center_x - PLAYER_COLLIDE_WIDTH / 2, center_y - PLAYER_COLLUDE_HEIGHT / 2 + PLAYER_SIZE / 2 - 5 * SCALE, PLAYER_COLLIDE_WIDTH, PLAYER_COLLUDE_HEIGHT))
playerDraw = pygame.sprite.RenderPlain(playerSprite)
player = Player("sc222", 10, 20, 20, 30, 5, 1, 0, playerSprite,playerCollideRect)

camera = Camera(0, 0, Rect(300, 200, 300, 200))

gui = GameOverlay(3, player.hp, player.mana, center_x,
                  center_y)  # todo store items somewhere #gui scale is smaller than game scale

# todo это временно, в финальной версии уровень будет грузиться из базы данных
map_bg = open(os.path.join("demo", "background.txt"), "r").read().split()
map_terrain = open(os.path.join("demo", "terrain.txt"), "r").read().split()

# todo 2d list for storing map obstacles
print(center_x,center_y)
background_draw_ls = parser.parse_map_to_static_draw_objects(resources.bg_imgs, map_bg, center_x, center_y)
terrain_draw_ls = parser.parse_map_to_static_draw_objects(resources.terrain_imgs, map_terrain, center_x, center_y,
                                                          TERRAIN_SHIFT)


# TODO MOVE TO DRAW UTILS SOMETHING LIKE THIS

# list(filter(lambda x: "n" in x, fruit))


def draw():
    display.fill(SKY)

    # todo here
    for background in filter(camera.should_draw, background_draw_ls):
        #print(background.get_draw_coordinates(camera))
        display.blit(background.image, background.get_draw_coordinates(camera))

    for terrain in filter(camera.should_draw, terrain_draw_ls):
        display.blit(terrain.image, terrain.get_draw_coordinates(camera))
        pygame.draw.rect(display, TR, terrain.get_taken_place_rect(camera,SCALE),5)

    # todo ЭЛЕМЕНТЫ ВНЕ КАМЕРЫ НЕ ДОЛЖНЫ РИСОВАТЬСЯ!!!
    # todo draw clouds
    # todo player should be drawed in priority before far objets and after close objects
    # todo (использовать ordered render из примера)
    # todo player isometric speed IS DIFFERENT (use cos \ sin \ web)

    playerDraw.draw(display)
    move_rect = player.collide_rect.move(playerSprite.velocity.x, playerSprite.velocity.y)
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

    cellx = math.floor((2*yy+xx-center_x-center_y+5*TILEWIDTH_HALF)/(2*TILEWIDTH_HALF))
    celly = math.floor((2*yy-xx+center_x-center_y+3*TILEWIDTH_HALF)/(2*TILEWIDTH_HALF))
    print(cellx, celly)

    dt = clock.tick(FPS)

    if not is_attack:
        mousex, mousey = pygame.mouse.get_pos()

        xx= mousex - center_x + camera.x_shift
        yy= mousey - center_y / 2 + camera.y_shift

        cellx = math.floor((xx / TILEWIDTH_HALF + yy / TILEHEIGHT_HALF) / 2)
        celly = math.floor((yy / TILEHEIGHT_HALF - (xx / TILEWIDTH_HALF)) / 2)
        print(cellx,celly)

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
            for terr in terrain_draw_ls:
                move_rect = player.collide_rect.move(playerSprite.velocity.x, playerSprite.velocity.y)

                if move_rect.colliderect(terr.get_taken_place_rect(camera,SCALE)):
                    print("collides with: ")
                    playerSprite.velocity.x=0
                    playerSprite.velocity.y=0

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

    # camera.y = WINDOWHEIGHT / 2 - playerSprite.y
    #print((-playerSprite.velocity.x, -playerSprite.velocity.y))
    camera.update(-playerSprite.velocity.x, -playerSprite.velocity.y)
    playerSprite.update(dt, playerState, camera)

    draw()
    pygame.display.flip()
