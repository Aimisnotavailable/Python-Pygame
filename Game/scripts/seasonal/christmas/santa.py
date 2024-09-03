import math
import pygame
class Santa:

    def __init__(self, animation, pos, angle, speed):
        self.animation = animation
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.done = False
    
    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed
        self.animation.update()

    def render(self, surf, offset):
        
        img = self.animation.img()
        size = img.get_size()
        img = pygame.transform.rotate(img, math.degrees(-self.angle))

        render_pos = ((self.pos[0] - offset[0]) % (surf.get_width() + size[0]) - size[0], (self.pos[1] - offset[1]) % (surf.get_height() + size[1]) - size[1])
        surf.blit(img, render_pos)
        self.update()