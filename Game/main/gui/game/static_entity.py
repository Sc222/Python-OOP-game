

class StaticEntity:
    def __init__(self, image, start_x, start_y, can_walk_on):
        self.image = image
        self.start_x = start_x
        self.start_y = start_y
        self.draw_x = start_x
        self.draw_y = start_y
        self.can_walk_on = can_walk_on

    def draw(self, display, camera):
        display.blit(self.image, (self.draw_x + camera.x_shift, self.draw_y + camera.y_shift))

    def update(self, camera):
        self.draw_x = self.start_x + camera.x_shift
        self.draw_y = self.start_y + camera.y_shift
