import math
import pygame
class Santa:

    def __init__(self, animation, pos, angle, speed):
        self.animation = animation
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.done = False
        self.depth = 0.1
    
    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed
        self.animation.update()

    def render(self, surf, offset):
        
        img = self.animation.img()
        size = img.get_size()
        img = pygame.transform.rotate(img, math.degrees(-self.angle))

        render_pos = ((self.pos[0] - offset[0] * self.depth) % (surf.get_width() + size[0]) - size[0], (self.pos[1] - offset[1] * self.depth) % (surf.get_height() + size[1]) - size[1])
        surf.blit(img, render_pos)
        self.update()
        if (render_pos[0] >= surf.get_width() - 1 or render_pos[0] <= 0 - size[0] + 1) or (render_pos[1] >= surf.get_height() - 1 or render_pos[1] <= 0 - size[1] + 1):
            self.done = True
        else:
            self.done = False