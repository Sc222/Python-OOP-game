from enum import Enum
import pygame
from main.gui.constants import MOVE_COLLIDE_RECT_OFFSET, SCALE, \
    MONSTER_ATTACK_DELTA_Y, MONSTER_ATTACK_DELTA_X
from main.gui.game.game_utils import Camera
from main.gui.game.player import Player


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
class MonsterSprite(pygame.sprite.Sprite):

    def __init__(self, position, size, images):  # images is a dictionary of image lists (key is animation name)
        super(MonsterSprite, self).__init__()
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

    def draw(self, display, camera: Camera):
        display.blit(self.image, (self.rect.x + camera.x_shift, self.rect.y + camera.y_shift))


# здесь игровая логика
class Monster:
    def __init__(self, nickname, hp, mana, attack, defence, speed, level, xp, sprite, collide_rect, camera: Camera):
        self.nickname = nickname
        self.hp = hp
        self.mana = mana
        self.attack = attack
        self.defence = defence
        self.speed = speed
        self.playerLevel = level
        self.xp = xp
        self.monsterSprite = sprite
        self.collide_rect = collide_rect
        self.state = CreatureState.idle
        self.direction = CreatureDirection.right
        self.velocity = pygame.math.Vector2()

    def get_collide_rect(self, camera):
        return self.collide_rect.move(camera.x_shift, camera.y_shift)

    def get_hit_rect(self, camera):
        res = self.collide_rect.move(camera.x_shift, camera.y_shift)
        res.inflate_ip(10 * SCALE, 15 * SCALE)
        return res

    def check_hit(self, player: Player, camera: Camera):
        # print(self.state)
        if self.state == CreatureState.take_damage or self.state == CreatureState.die:
            # print("AAAAAAAAA")
            return
        hit_rect = self.get_hit_rect(camera)
        res = player.state.name == CreatureState.attack.name and hit_rect.colliderect(player.get_attack_rect())
        if res:
            # print("ATTACK SUCCESSFUL")
            self.decrease_hp(player.attack)
            print(self.state)
        return res

    def decrease_hp(self, attack):
        self.hp = self.hp - attack
        self.state = CreatureState.take_damage
        if self.hp <= 0:
            # self.monsterSprite.curr_index=0
            self.state = CreatureState.die

    def perform_attack(self):
        self.state = CreatureState.attack
        self.velocity.x = 0
        self.velocity.y = 0

    def perform_movement(self, player_pos, visible_terrain_ls, camera: Camera):
        if self.state != CreatureState.attack and self.state != CreatureState.take_damage and self.state != CreatureState.die:
            dx = self.monsterSprite.rect.centerx - player_pos[0] + camera.x_shift
            dy = self.monsterSprite.rect.centery - player_pos[1] + camera.y_shift
            self.velocity.x = -dx if abs(dx) > MONSTER_ATTACK_DELTA_X else 0
            self.velocity.y = -dy if abs(dy) > MONSTER_ATTACK_DELTA_Y else 0
            if abs(dx) < MONSTER_ATTACK_DELTA_X and abs(dy) < MONSTER_ATTACK_DELTA_Y:
                # attack
                self.perform_attack()
                return

            if self.velocity.x != 0 or self.velocity.y != 0:
                self.state = CreatureState.walk
                self.velocity.normalize_ip()
                self.velocity *= self.speed
                tmp_collide_rect = self.get_collide_rect(camera)
                self.direction = CreatureDirection.right if self.velocity.x > 0 else CreatureDirection.left
                for terrain in visible_terrain_ls:
                    move_rect_x = tmp_collide_rect.move(self.velocity.x * MOVE_COLLIDE_RECT_OFFSET, 0)
                    move_rect_y = tmp_collide_rect.move(0, self.velocity.y * MOVE_COLLIDE_RECT_OFFSET)
                    collide_x = move_rect_x.colliderect(terrain.get_taken_place_rect(SCALE))
                    collide_y = move_rect_y.colliderect(terrain.get_taken_place_rect(SCALE))
                    if collide_x:
                        # print("collides x")
                        self.velocity.x = 0
                    if collide_y:
                        # print("collides y")
                        self.velocity.y = 0
                    if collide_x and collide_y:
                        self.state = CreatureState.idle
                self.monsterSprite.rect.move_ip(self.velocity.x, self.velocity.y)
                self.collide_rect.move_ip(self.velocity.x, self.velocity.y)
            else:
                self.state = CreatureState.idle

    def update_attack_status(self):
        if (
                self.state == CreatureState.attack or self.state == CreatureState.take_damage) and self.monsterSprite.is_animation_end():
            self.state = CreatureState.idle

    def state_str(self):
        return self.state.name + "_" + self.direction.name

    def update(self, dt):
        if self.state == CreatureState.die and self.monsterSprite.is_animation_end():
            # self.monsterSprite.upd(dt, self.state_str())
            return
        self.update_attack_status()
        self.monsterSprite.upd(dt, self.state_str())
