import pygame
import math
import random

class Particles:

    def __init__(self, game, type,  angle, speed, pos=(0, 0), color_key=(255, 255 ,255)):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.color_key = color_key
        self.type = type
        self.animation = game.assets['particles' + '/' + type].copy()
        self.animation.frame = random.randint(0, len(self.animation.images))
        

    def update(self):
        
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed * 1.5

    def render(self, surf, offset=(0, 0)):
        
        # render_points = [
        #     (self.pos[0] - offset[0] + math.cos(self.angle) * self.speed , self.pos[1] - offset[1] + math.sin(self.angle) * self.speed ),
        #     (self.pos[0] - offset[0] + math.cos(self.angle + math.pi * 0.5) * self.speed , self.pos[1] - offset[1] + math.sin(self.angle) * self.speed ),
        #     (self.pos[0] - offset[0] + math.cos(self.angle + math.pi * 0.5) * self.speed , self.pos[1] - offset[1] + math.sin(self.angle + math.pi) * self.speed ),
        #     (self.pos[0] - offset[0] + math.cos(self.angle) * self.speed , self.pos[1] - offset[1] + math.sin(self.angle + math.pi) * self.speed ),
        # ]

        # pygame.draw.polygon(surf, self.color_key, render_points)
        
        img_mask = pygame.mask.from_surface(self.animation.img())
        img = img_mask.to_surface(setcolor=(*self.color_key, 180), unsetcolor=(0, 0, 0, 0))
        #
        if self.type == 'snow':
            pygame.draw.circle(surf, (255, 255, 255), (((self.pos[0] - offset[0]) % (surf.get_width() + img.get_width()) - img.get_width(), (self.pos[1] - offset[1]) % (surf.get_height() + img.get_height()) -img.get_height())), random.random() * 3)
            #surf.blit(img, ((self.pos[0] - offset[0]) % (surf.get_width() + img.get_width()) - img.get_width(), (self.pos[1] - offset[1]) % (surf.get_height() + img.get_height()) -img.get_height()))
        else:
            surf.blit(img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        self.update()
        self.animation.update()

        return self.animation.done