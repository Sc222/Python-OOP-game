from enum import Enum
import pygame
from main.gui.constants import MOUSE_IDLE_DELTA, MOVE_COLLIDE_RECT_OFFSET, SCALE


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

    def perform_movement(self, mouse_pos, visible_terrain_ls):
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
                for terrain in visible_terrain_ls:
                    move_rect_x = self.collide_rect.move(self.velocity.x * MOVE_COLLIDE_RECT_OFFSET, 0)
                    move_rect_y = self.collide_rect.move(0, self.velocity.y * MOVE_COLLIDE_RECT_OFFSET)
                    collide_x = move_rect_x.colliderect(terrain.get_taken_place_rect())
                    collide_y = move_rect_y.colliderect(terrain.get_taken_place_rect())
                    if collide_x:
                        # print("collides x")
                        self.velocity.x = 0
                    if collide_y:
                        # print("collides y")
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
