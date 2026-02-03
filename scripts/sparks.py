import pygame
import math
import random

class Sparks:

    def __init__(self, angle, speed, pos, color=(255, 255, 255), is_spread=False):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.color = color
        self.spread = []
        self.is_spread = is_spread
    
    def update(self):
        # if not self.is_spread and random.randint(0, 1) :
        #     self.spread.append(Sparks((random.random() - 0.5) * math.pi, self.speed / 2, self.pos, (0, 0, 0), True))

        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)

        return not self.speed
    
    def render(self, surf, offset=(0, 0)):

        # for spread in self.spread.copy():
        #     spread.render(surf, offset)
        #     print(spread.angle)
        #     if spread.update():
        #         self.spread.remove(spread)

        render_points = [
            (self.pos[0] - offset[0] + math.cos(self.angle) * self.speed * 3, self.pos[1] - offset[1] + math.sin(self.angle) * self.speed * 3),
            (self.pos[0] - offset[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5, self.pos[1] - offset[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5),
            (self.pos[0] - offset[0] + math.cos(self.angle + math.pi) * self.speed * 3, self.pos[1] - offset[1] + math.sin(self.angle + math.pi) * self.speed * 3),
            (self.pos[0] - offset[0] + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5, self.pos[1] - offset[1] + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5)
        ]

        pygame.draw.polygon(surf, self.color, render_points)