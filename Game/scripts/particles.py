import pygame
import math
import random

class Particles:

    def __init__(self, game, type, angle, speed, pos=(0, 0)):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.animation = game.assets['particles' + '/' + type]

    def update(self):
        
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)

        return not self.speed

    def render(self, surf, offset=(0, 0)):
        rotated_img = pygame.transform.rotate(self.animation.img(), -self.angle * 180/math.pi)
        img_rect = rotated_img.get_rect(center=((self.pos[0] - offset[0], self.pos[1] - offset[1])))
        surf.blit(rotated_img, img_rect)
        self.animation.update()