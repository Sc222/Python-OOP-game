from enum import Enum

import pygame

from game_utils import Camera


class CreatureState(Enum):
    idle = 0
    walk = 1
    attack = 2
    take_damage = 3
    die = 4


# здесь логика отрисовки
class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, position, size, images):  # images is a dictionary of image lists (key is animation name)
        super(PlayerSprite, self).__init__()
        self.animation_time = 70  # todo выставлять время анимации в зависимости от числа кадров в текущей анимации
        self.current_time = 0
        self.curr_index = 0
        self.curr_state = "idle_front_right"
        self.rect = pygame.Rect(position, size)
        self.images = images
        self.image = images[self.curr_state][self.curr_index]  # 'image' is the current image of the animation.
        self.velocity = pygame.math.Vector2()
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def update_time_dependent(self, dt, state: CreatureState, camera: Camera):
        prev_state = self.curr_state
        self.curr_state = state.name  ##todo comment this
        print("update : " + str(self.velocity.x) + " " + str(self.velocity.y))
        print(prev_state)
        print(state.name)

        if self.velocity.x > 0:  # Use the right images if sprite is moving right.
            self.curr_state = self.curr_state + "_" + "front" + "_" + "right"
        elif self.velocity.x < 0:
            self.curr_state = self.curr_state + "_" + "front" + "_" + "left"
        else:
            if prev_state.endswith("_front_right"):  ##todo ВЫНЕСТИ В МЕТОД
                self.curr_state = self.curr_state + "_front_right"
            elif prev_state.endswith("_front_left"):  ##todo back_left back_right etc\
                self.curr_state = self.curr_state + "_front_left"

        if self.velocity.x == 0 and self.velocity.y == 0:  ##idle depends on previous state
            self.curr_state = "idle"
            if prev_state.endswith("_front_right"):
                self.curr_state = self.curr_state + "_front_right"
            elif prev_state.endswith("_front_left"):  ##todo back_left back_right etc\
                self.curr_state = self.curr_state + "_front_left"

        self.current_time += dt
        if prev_state != self.curr_state:  # когда начинается другая анимация счетчик сбрасывается
            self.curr_index = 0

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.curr_index = (self.curr_index + 1) % len(self.images[self.curr_state])
            self.image = self.images[self.curr_state][self.curr_index]

        # self.rect.move_ip(*self.velocity)
        self.x += self.velocity.x
        self.y += self.velocity.y

    def update(self, dt, state: CreatureState, camera: Camera):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        self.update_time_dependent(dt, state, camera)


# здесь игровая логика
class Player:
    def __init__(self, nickname, hp, attack, defence, speed, playerLevel, xp, playerSprite):
        self.nickname = nickname
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.playerLevel = playerLevel
        self.xp = xp
        self.playerSprite = playerSprite
        # self.collision_rect = collision_rect todo is collision rect needed or sprite rect is enough?
