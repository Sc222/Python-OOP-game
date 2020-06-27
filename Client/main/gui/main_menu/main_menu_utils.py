import pygame


class ScrollingBackgroundHorizontal(pygame.sprite.Sprite):
    def __init__(self, image, x, y, scroll_width):
        super(ScrollingBackgroundHorizontal, self).__init__()
        self.image = image
        self.x = x
        self.y = y
        self.animation_time = 15
        self.current_time = 0
        self.rect = self.image.get_rect()
        self.scroll_width = scroll_width

    def scroll(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.x -= 1
            if self.x < -self.scroll_width:
                self.x = self.scroll_width

    def update(self, dt):
        self.scroll(dt)

    def draw(self, display):
        display.blit(self.image, (self.x, self.y))


class PlayerMenu(pygame.sprite.Sprite):

    def __init__(self, position, images):  # images is a dictionary of image lists (key is animation name)
        super(PlayerMenu, self).__init__()
        self.curr_state = "menu_idle"
        size = (images[self.curr_state][0].get_width(), images[self.curr_state][0].get_height())
        self.rect = pygame.Rect(position, size)
        self.animation_time = 70
        self.current_time = 0
        self.curr_index = 0
        self.images = images
        self.image = images[self.curr_state][self.curr_index]  # 'image' is the current image of the animation.
        self.x = self.rect.centerx
        self.y = self.rect.centery

    def is_transformation_finished(self):
        return self.curr_index == len(self.images[self.curr_state]) - 1 and self.curr_state == "menu_transform"

    def start_transformation(self):
        self.curr_index = 0
        self.curr_state = "menu_transform"

    def stop_transformation(self):
        self.curr_index = 0
        self.curr_state = "menu_idle"

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.curr_index = (self.curr_index + 1) % len(self.images[self.curr_state])
            self.image = self.images[self.curr_state][self.curr_index]

    def draw(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
