import pygame
import math
import random

class Particles:

    def __init__(self, angle, speed, pos=(0, 0), color_key=(255, 255 ,255)):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.color_key = color_key
        # self.animation = game.assets['particles' + '/' + type]

    def update(self):
        
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)

        return not self.speed

    def render(self, surf, offset=(0, 0)):
        
        render_points = [
            (self.pos[0] - offset[0] + math.cos(self.angle) * self.speed , self.pos[1] - offset[1] + math.sin(self.angle) * self.speed ),
            (self.pos[0] - offset[0] + math.cos(self.angle + math.pi * 0.5) * self.speed , self.pos[1] - offset[1] + math.sin(self.angle) * self.speed ),
            (self.pos[0] - offset[0] + math.cos(self.angle + math.pi * 0.5) * self.speed , self.pos[1] - offset[1] + math.sin(self.angle + math.pi) * self.speed ),
            (self.pos[0] - offset[0] + math.cos(self.angle) * self.speed , self.pos[1] - offset[1] + math.sin(self.angle + math.pi) * self.speed ),
        ]

        pygame.draw.polygon(surf, self.color_key, render_points)
        # surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        # self.animation.update()