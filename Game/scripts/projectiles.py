import math
import pygame
class Projectiles:

    def __init__(self, animation, rotation_angle, speed, angle, life, pos=(0, 0), spawn=None):
        self.animation = animation
        self.rotation_angle = rotation_angle
        self.speed = speed
        self.pos = list(pos)
        self.angle = angle
        self.life = life
        self.spawn = spawn
        self.y_vel = 0
        self.kill = False
       

    def update(self):
        self.y_vel = min(5, self.y_vel + 0.01) 
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed + self.y_vel
        self.life -=1
        return not self.life

    def render(self, surf, offset=(0, 0)):
        img = pygame.transform.rotate(self.animation.img(), self.rotation_angle)
        img_rect = img.get_rect(center=(self.pos[0] - offset[0], self.pos[1] - offset[1]))
        surf.blit(img, img_rect)
        self.animation.update()
    