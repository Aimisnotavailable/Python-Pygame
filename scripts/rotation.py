import pygame
import math
import sys
import random
from scripts.utils import load_image, load_images, Animation
from scripts.sparks import Sparks
from scripts.particles import Particles
from scripts.entities import Player

QUADRANTS = {(1, 0) : 0,
             (0, 0) : 180,
             (0, 1) : 180,
             (1, 1) : 360
             }

class Rotation:
    
    def rect(self, pos, size):
        return pygame.Rect(pos[0], pos[1], size[0], size[1])

    def get_angle(self, midpoint=(0, 0), mpos=(0, 0)):
        self.midpoint = midpoint
        self.mpos = mpos
        self.flip_x = 0
        self.flip_y = 0

        self.flip_x = 1 if self.mpos[0] > self.midpoint[0] else 0
        self.flip_y = 1 if self.mpos[1] > self.midpoint[1] else 0

        quad = (self.flip_x, self.flip_y)

        x = (self.mpos[0] - self.midpoint[0])
        y = (self.mpos[1] - self.midpoint[1])

        if x != 0:
            angle = int((math.atan(y/x) * (-1 if self.flip_x else 1) * (180 / math.pi) ) + QUADRANTS[quad])
        else:
            angle = 90 if self.flip_y else 270

        return angle
    
    def img(self, img, angle):
        self.image = img
        
        img = pygame.transform.scale(self.image, (16, 8))
        img = pygame.transform.flip(pygame.transform.rotate(img , angle), False, not self.flip_x)

        return img
    
        # img_rect = img.get_rect(center=(self.midpoint))

        # self.display.blit(pygame.transform.flip(img, False ,  not self.flip_x), img_rect)

    def draw_curve(self, surf, origin, angle, speed):
        m_points = list(origin).copy()
        y_vel = 0

        for i in range(5):
            y_vel = min(5, y_vel + 0.01) 
            m_points[0] += math.cos(angle) * speed
            m_points[1] += math.sin(angle) * speed + y_vel
            pygame.draw.circle(surf, (255, 255, 255), m_points, 1)       
