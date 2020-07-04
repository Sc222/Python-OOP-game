from enum import Enum
import pygame
from pygame.rect import Rect

from main.gui.constants import MOUSE_IDLE_DELTA, MOVE_COLLIDE_RECT_OFFSET, SCALE, WINDOW_W_HALF, PL_SIZE_HALF, \
    WINDOW_H_HALF, TILE_SIZE_HALF, PL_X_SHIFT, PL_Y_SHIFT, TILE_SIZE, PL_Y_SHIFT_DOUBLE
from main.gui.game.camera import Camera


class CreatureState(Enum):
    idle = 0
    walk = 1
    attack = 2
    take_damage = 3
    die = 4


class CreatureDirection(Enum):
    left = 0
    right = 1


# здесь логика отрисовки
class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, position, size, images):  # images is a dictionary of image lists (key is animation name)
        super(PlayerSprite, self).__init__()
        self.animation_time = 70
        self.current_time = 0
        self.curr_index = 0
        self.curr_state = "idle_right"
        self.rect = pygame.Rect(position, size)
        self.images = images
        self.image = images[self.curr_state][self.curr_index]  # 'image' is the current image of the animation.
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def is_animation_end(self):
        return self.curr_index == len(self.images[self.curr_state]) - 1

    def upd(self, dt, state: str):
        if state != self.curr_state:  # когда начинается другая анимация счетчик сбрасывается
            self.curr_index = 0
        self.curr_state = state
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.curr_index = (self.curr_index + 1) % len(self.images[self.curr_state])
            self.image = self.images[self.curr_state][self.curr_index]

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


# здесь игровая логика
class Player:
    def __init__(self, nickname, hp, mana, attack, defence, speed, level, xp, sprite, collide_rect):
        self.nickname = nickname
        self.hp = hp
        self.mana = mana
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.playerLevel = level
        self.xp = xp
        self.playerSprite = sprite
        self.collide_rect = collide_rect
        self.state = CreatureState.idle
        self.direction = CreatureDirection.right
        self.velocity = pygame.math.Vector2()

    @staticmethod
    def map_coordinates_to_camera_position(map_x: int, map_y: int):
        map_x = -map_x
        map_y = -map_y
        camera_x = PL_X_SHIFT + (map_x - map_y) * TILE_SIZE_HALF
        camera_y = PL_Y_SHIFT + (map_x + map_y) * 0.5 * TILE_SIZE_HALF
        return camera_x, camera_y

    @staticmethod
    def camera_pos_to_map_pos(camera: Camera, x_movement=0, y_movement=0):
        camera_x = camera.x_shift - x_movement
        camera_y = camera.y_shift - y_movement
        map_x = (PL_Y_SHIFT_DOUBLE + PL_X_SHIFT - camera_x - 2 * camera_y) / TILE_SIZE
        map_y = (PL_Y_SHIFT_DOUBLE - PL_X_SHIFT + camera_x - 2 * camera_y) / TILE_SIZE
        return map_x, map_y

    @staticmethod
    def camera_pos_to_map_pos_round(camera: Camera, x_movement=0, y_movement=0):
        camera_x = camera.x_shift - x_movement
        camera_y = camera.y_shift - y_movement
        map_x = (PL_Y_SHIFT_DOUBLE + PL_X_SHIFT - camera_x - 2 * camera_y) / TILE_SIZE
        map_y = (PL_Y_SHIFT_DOUBLE - PL_X_SHIFT + camera_x - 2 * camera_y) / TILE_SIZE
        return round(map_x), round(map_y)

    def perform_attack(self):
        self.state = CreatureState.attack
        self.velocity.x = 0
        self.velocity.y = 0

    def get_attack_rect(self):
        direction_multiplier = 0
        if self.direction.name == "left":
            direction_multiplier = -1
        if self.direction.name == "right":
            direction_multiplier = 1
        return self.collide_rect.move(direction_multiplier * 7 * SCALE, -6 * SCALE)

    def perform_movement(self, mouse_pos,camera,terrain_around,width, height):
        if self.state != CreatureState.attack:
            dx = self.playerSprite.rect.centerx - mouse_pos[0]
            dy = self.playerSprite.rect.centery - mouse_pos[1]
            self.velocity.x = -dx if abs(dx) > MOUSE_IDLE_DELTA else 0
            self.velocity.y = -dy if abs(dy) > MOUSE_IDLE_DELTA else 0
            if self.velocity.x != 0 or self.velocity.y != 0:
                self.state = CreatureState.walk
                self.velocity.normalize_ip()
                self.velocity *= self.speed
                self.direction = CreatureDirection.right if self.velocity.x > 0 else CreatureDirection.left

                # move_rect_x:Rect = self.collide_rect.move(self.velocity.x * MOVE_COLLIDE_RECT_OFFSET, 0)
                # move_rect_y:Rect= self.collide_rect.move(0, self.velocity.y * MOVE_COLLIDE_RECT_OFFSET)
                # move_rect_x.collidepoint()
                # move_rect_y.collidepoint()
                #print(Player.camera_pos_to_map_pos(camera))
                #print("velocity x and y", self.velocity.x, self.velocity.y)
                #print("moved: ", Player.camera_pos_to_map_pos(camera, self.velocity.x, self.velocity.y))

                map_pos_x_move = Player.camera_pos_to_map_pos_round(camera, x_movement= self.velocity.x*2)
                map_pos_y_move = Player.camera_pos_to_map_pos_round(camera, y_movement=self.velocity.y*2)
                move_rect_x = self.collide_rect.move(self.velocity.x * MOVE_COLLIDE_RECT_OFFSET, 0)
                move_rect_y = self.collide_rect.move(0, self.velocity.y * MOVE_COLLIDE_RECT_OFFSET)
                #print(terrain_around)

                # check collision with terrain objects
                collide_x=map_pos_x_move in terrain_around and move_rect_x.colliderect(terrain_around[map_pos_x_move].get_taken_place_rect(camera))
                collide_y=map_pos_y_move in terrain_around and move_rect_y.colliderect(terrain_around[map_pos_y_move].get_taken_place_rect(camera))
                if collide_x:
                    self.velocity.x = 0
                if collide_y:
                    self.velocity.y = 0
                if collide_x and collide_y:
                    self.state = CreatureState.idle

                #check map borders
                collide_x = map_pos_x_move[0] < 0 or map_pos_x_move[0] >= width  or map_pos_x_move[1] < 0 or map_pos_x_move[1] >= height
                collide_y =map_pos_y_move[0] < 0 or map_pos_y_move[0] >= width or map_pos_y_move[1] < 0 or map_pos_y_move[1] >= height
                print(map_pos_x_move," ",map_pos_y_move)
                if collide_x:
                    self.velocity.x = 0
                if collide_y:
                    self.velocity.y = 0
                if collide_x and collide_y:
                    self.state = CreatureState.idle
            else:
                self.state = CreatureState.idle

    def update_attack_status(self):
        if self.state == CreatureState.attack and self.playerSprite.is_animation_end():
            self.state = CreatureState.idle

    def state_str(self):
        return self.state.name + "_" + self.direction.name

    def update(self, dt):
        self.update_attack_status()
        self.playerSprite.upd(dt, self.state_str())
