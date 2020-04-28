import os

import pygame
from pygame.locals import *

from game_utils import Resources
from game_utils import Parser
import sys

from game_utils import Scroll

from game_utils import load_image

from player import PlayerSprite

from player import CreatureState

from player import Player

pygame.init()

FPS=60
clock = pygame.time.Clock()
TERRAIN_SHIFT = -6
WINDOWWIDTH = 900
WINDOWHEIGHT = 600
screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), 0, 32)  # set the display mode, window title and FPS clock
display = pygame.Surface((180, 120))  # todo surface size - game x*32 +16 , game y*16+32
pygame.display.set_caption('Map Rendering Demo')
FPSCLOCK = pygame.time.Clock()

SKY = (0, 205, 249)

TILEWIDTH = 32  # holds the tile width and height
TILEHEIGHT = 32
TILEHEIGHT_HALF = TILEHEIGHT / 2
TILEWIDTH_HALF = TILEWIDTH / 2



# todo move to file


camera_scroll = Scroll(0, 0)

resources = Resources("data")
parser = Parser()
center_x = display.get_rect().centerx
center_y = display.get_rect().centery

playerSprite = PlayerSprite((center_x-42/2, center_y-42/2), (42, 42), resources.player_imgs)
playerDraw = pygame.sprite.RenderPlain(playerSprite)
player = Player("sc222",10,20,30,1,0,playerSprite)

#playerSprite.update(CreatureState.idle)
#all_sprites = pygame.sprite.Group(playerSprite)
#all_sprites.draw(display)

# todo это временно, в финальной версии уровень будет грузиться из базы данных
map_bg = open(os.path.join("demo", "background.txt"), "r").read().split()
map_terrain = open(os.path.join("demo", "terrain.txt"), "r").read().split()
background_draw_ls = Parser().parse_map_to_static_draw_objects(resources.bg_imgs, map_bg, center_x, center_y)
terrain_draw_ls = Parser().parse_map_to_static_draw_objects(resources.terrain_imgs, map_terrain, center_x, center_y,
                                                            TERRAIN_SHIFT)


def draw():
    display.fill(SKY)
    for background in background_draw_ls:
        display.blit(background.image, background.get_draw_coordinates(camera_scroll))



    for terrain in terrain_draw_ls:
        display.blit(terrain.image, terrain.get_draw_coordinates(camera_scroll))

    #todo player should be drawed in priority before far objets and after close objects
    #todo player isometric speed IS DIFFERENT (use cos \ sin \ web)
    playerDraw.draw(display)

    screen.blit(pygame.transform.scale(display, (WINDOWWIDTH, WINDOWHEIGHT)), (0, 0))


draw()
playerState = CreatureState.idle
while True:
    dt = clock.tick(FPS)
    print(playerSprite.rect.centerx)
    print(playerSprite.rect.centery)
    if playerSprite.rect.centerx+camera_scroll.x>100:
        camera_scroll.x-= 2
    elif playerSprite.rect.centerx + camera_scroll.x < 80:
        camera_scroll.x += 2
    if playerSprite.rect.centery+camera_scroll.y>65:
        camera_scroll.y-= 1
    elif playerSprite.rect.centery + camera_scroll.y < 55:
        camera_scroll.y += 1

   # if playerSprite.rect.y > 100:
   #     camera_scroll.x -= 1
    #camera_scroll.x=center_x-playerSprite.rect.x
    #  for surface in surface_draw_ls:
    #      display.blit(surface.image, surface.get_draw_coordinates(camera_scroll))  # display the actual tile
    #      screen.blit(pygame.transform.scale(display, (WINDOWWIDTH, WINDOWHEIGHT)), (0, 0))

    for event in pygame.event.get():
        ##TODO CODE QUIT

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                playerState=CreatureState.walk
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
                playerState=CreatureState.idle
                playerSprite.velocity.x = 0
            elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                playerState = CreatureState.idle
                playerSprite.velocity.y = 0

    #playerSprite.rect.x=camera_scroll.x
   # playerSprite.rect.y= camera_scroll.y
    playerSprite.update(dt, playerState)
    draw()

    pygame.display.flip()
