import os
import pygame
from game_utils import Resources
from game_utils import Parser
from game_utils import Camera
from player import PlayerSprite
from player import CreatureState
from player import Player

pygame.init()

FPS = 60
clock = pygame.time.Clock()
TERRAIN_SHIFT = -6
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
SCALEDWIDTH = 900  # 180
SCALEDHEGHT = 600  # 120
SCALE = 5
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)  # set the display mode, window title and FPS clock
display = pygame.Surface((SCALEDWIDTH, SCALEDHEGHT))  # todo surface size - game x*32 +16 , game y*16+32
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

SKY = (0, 205, 249)

TILEWIDTH = 32 * SCALE  # holds the tile width and height
TILEHEIGHT = 32 * SCALE
TILEHEIGHT_HALF = TILEHEIGHT / 2
TILEWIDTH_HALF = TILEWIDTH / 2

MOUSE_IDLE_DELTA = 40  # когда разница в координатах меньше этого числа игрок стоит на месте

# todo move to file


camera = Camera(SCALEDWIDTH, SCALEDHEGHT, 0, 0)

resources = Resources("data", SCALE)
parser = Parser(SCALE)
center_x = display.get_rect().centerx
center_y = display.get_rect().centery

playerSprite = PlayerSprite((center_x - 18 * SCALE / 2, center_y - 24 * SCALE / 2), (18 * SCALE, 24 * SCALE),
                            resources.player_imgs)
playerDraw = pygame.sprite.RenderPlain(playerSprite)
player = Player("sc222", 10, 20, 30, 3, 1, 0, playerSprite)

# todo это временно, в финальной версии уровень будет грузиться из базы данных
map_bg = open(os.path.join("demo", "background.txt"), "r").read().split()
map_terrain = open(os.path.join("demo", "terrain.txt"), "r").read().split()
background_draw_ls = parser.parse_map_to_static_draw_objects(resources.bg_imgs, map_bg, center_x, center_y)
terrain_draw_ls = parser.parse_map_to_static_draw_objects(resources.terrain_imgs, map_terrain, center_x, center_y,
                                                          TERRAIN_SHIFT)


def draw():
    display.fill(SKY)
    for background in background_draw_ls:
        display.blit(background.image, background.get_draw_coordinates(camera))
    for terrain in terrain_draw_ls:
        display.blit(terrain.image, terrain.get_draw_coordinates(camera))

    # todo player should be drawed in priority before far objets and after close objects
    # todo (использовать ordered render из примера)
    # todo player isometric speed IS DIFFERENT (use cos \ sin \ web)
    playerDraw.draw(display)
    screen.blit(display, (0, 0))


draw()
playerState = CreatureState.idle
value = 0

while True:
    mousex, mousey = pygame.mouse.get_pos()
    mousex = mousex
    mousey = mousey

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
    else:
        playerState = CreatureState.idle

    dt = clock.tick(FPS)
    value += 1
    if value == 10:
        value = 0
        print("mouse: " + str(mousex) + " " + str(mousey))
        # print("cam: " + str(camera.x) + " " + str(camera.y))
        print("player: " + str(playerSprite.rect.centerx) + " " + str(playerSprite.rect.centery))
    # print(playerSprite.rect.centery)
    # if playerSprite.rect.centerx + camera.x > 90:
    #     camera.x -= 1
    # elif playerSprite.rect.centerx + camera.x < 90:
    #     camera.x += 1
    # if playerSprite.rect.centery + camera.y > 60:
    #     camera.y -= 1
    # elif playerSprite.rect.centery + camera.y < 60:
    #     camera.y += 1

    # if 10*1.4142*3-playerSprite.rect.centerx<10:
    #     camera_scroll.x-=1

    # if playerSprite.rect.y > 100:
    #     camera_scroll.x -= 1
    # camera_scroll.x=center_x-playerSprite.rect.x
    #  for surface in surface_draw_ls:
    #      display.blit(surface.image, surface.get_draw_coordinates(camera_scroll))  # display the actual tile
    #      screen.blit(pygame.transform.scale(display, (WINDOWWIDTH, WINDOWHEIGHT)), (0, 0))

    for event in pygame.event.get():
        ##TODO CODE QUIT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerState = CreatureState.walk

                playerSprite.velocity.x = 1
            elif event.key == pygame.K_LEFT:
                playerState = CreatureState.walk
                playerSprite.velocity.x = -1
            elif event.key == pygame.K_DOWN:
                playerState = CreatureState.walk
                playerSprite.velocity.y = 1
            elif event.key == pygame.K_UP:
                playerState = CreatureState.walk
                playerSprite.velocity.y = -1
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerState = CreatureState.idle
                playerSprite.velocity.x = 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerState = CreatureState.idle
                playerSprite.velocity.y = 0

    camera.x = WINDOWWIDTH / 2 - playerSprite.x
    camera.y = WINDOWHEIGHT / 2 - playerSprite.y
    playerSprite.update(dt, playerState, camera)
    draw()

    pygame.display.flip()
