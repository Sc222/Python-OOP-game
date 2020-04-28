from enum import Enum

import pygame


class CreatureState(Enum):
    idle = 0
    walk = 1
    attack = 2
    take_damage = 3
    die = 4


# здесь логика отрисовки
class PlayerSprite(pygame.sprite.Sprite):

    def __init__(self, position, size, images):  # images is a dictionary of image lists (key is animation name)
        """
        Animated sprite object.

        Args:
            position: x, y coordinate on the screen to place the AnimatedSprite.
            images: Images to use in the animation.
        """
        super(PlayerSprite, self).__init__()
        self.animation_time = 70
        self.current_time = 0
        self.curr_index = 0
        self.curr_state = "idle_front_right"
        self.rect = pygame.Rect(position, size)
        self.images = images
        self.image = images[self.curr_state][self.curr_index]  # 'image' is the current image of the animation.
        self.velocity = pygame.math.Vector2(0, 0)
        self.current_frame = 0

    def update_time_dependent(self, dt, state: CreatureState):
        """
        Updates the image of Sprite every 6 frame (approximately every 0.1 second if frame rate is 60).
        """
        #print(state.name)

        prev_state = self.curr_state
        self.curr_state = state.name  ##todo comment this

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

        #if prev_state!=self.curr_state: ##todo is it needed?
        #    self.curr_index=0

       # print(dt)
        self.current_time += dt
       # print(str(self.current_time)+ "anim: "+str(self.animation_time))
        if self.current_time >= self.animation_time:
            self.current_time=0
            #self.current_frame = 0
            self.curr_index = (self.curr_index + 1) % len(self.images)
            #print(self.curr_state)
            self.image = self.images[self.curr_state][self.curr_index]

        self.rect.move_ip(*self.velocity)

    def update(self, dt, state: CreatureState):
        """This is the method that's being called when 'all_sprites.update(dt)' is called."""
        self.update_time_dependent(dt, state)


# здесь игровая логика
class Player:
    def __init__(self, nickname, hp, attack, defence, playerLevel, xp, playerSprite):
        self.nickname = nickname
        self.hp = hp
        self.attack = attack
        self.defence = defence
        self.playerLevel = playerLevel
        self.xp = xp
        self.playerSprite = playerSprite
        # self.collision_rect = collision_rect todo is collision rect needed or sprite rect is enough?
