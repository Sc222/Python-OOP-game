from enum import Enum

import pygame

from main.gui.game_utils import Camera


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
        self.curr_state = "idle_right"
        self.rect = pygame.Rect(position, size)
        self.images = images
        self.image = images[self.curr_state][self.curr_index]  # 'image' is the current image of the animation.
        self.velocity = pygame.math.Vector2()
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def is_animation_end(self):
        return self.curr_index==len(self.images[self.curr_state])-1

    def update_time_dependent(self, dt, state: CreatureState, camera: Camera):
        prev_state = self.curr_state
        prev_state_dir=prev_state.split("_")[1]

        if state==CreatureState.idle or state==CreatureState.attack: # у idle и attack направление зависит от предыдущего состояния
            self.curr_state=state.name+"_"+prev_state_dir
        else:
            self.curr_state = state.name+"_right" if self.velocity.x>0 else state.name+"_left"

        self.current_time += dt
        if prev_state != self.curr_state:  # когда начинается другая анимация счетчик сбрасывается
            self.curr_index = 0

        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.curr_index = (self.curr_index + 1) % len(self.images[self.curr_state])
            self.image = self.images[self.curr_state][self.curr_index]

        # self.rect.move_ip(*self.velocity)

    def update(self, dt, state: CreatureState, camera: Camera):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        self.update_time_dependent(dt, state, camera)


# здесь игровая логика
class Player:
    def __init__(self, nickname, hp, mana, attack, defence, speed, playerLevel, xp, playerSprite, collide_rect):
        self.nickname = nickname
        self.hp = hp
        self.mana=mana
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.playerLevel = playerLevel
        self.xp = xp
        self.playerSprite = playerSprite
        self.collide_rect = collide_rect
