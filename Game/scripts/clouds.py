import random
import pygame

from scripts.utils import load_image

RENDER_SCALE = 2

class Cloud:
    
    def __init__(self, img, speed, depth, pos=(0,0)):
        self.img = img
        self.pos = list(pos)
        self.speed = speed
        self.depth = depth
        rand = (random.random())
        self.size = (rand * RENDER_SCALE * self.img.get_width(), rand * RENDER_SCALE * self.img.get_height())

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0,0)):
        render_pos = ((self.pos[0] - offset[0] * self.depth), (self.pos[1] - offset[1] * self.depth))

        surf.blit(pygame.transform.scale(self.img, self.size), (render_pos[0] % (surf.get_width() + self.img.get_width()), render_pos[1] % (surf.get_height() + self.img.get_height())))

class Clouds:

    def __init__(self, img, count=20):
        self.clouds = []

        for i in range(count):
            self.clouds.append(Cloud(img, random.random() * 0.5 + 0.5, random.random() * 0.6 + 0.2, pos=(random.random() * 99999, random.random() * 99999)))
        
        self.clouds.sort(key=lambda x : x.size)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0,0)):
        for cloud in self.clouds:
            cloud.render(surf, offset)