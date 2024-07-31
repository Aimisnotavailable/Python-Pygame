import pygame
import sys
import math
import random

from scripts.rotation import Rotation
from scripts.projectiles import Projectiles
from scripts.sparks import Sparks
from scripts.assets import Assets



class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))

        pygame.init()

        self.clock = pygame.time.Clock()
        self.rotation = Rotation()

        self.sparks = []
        self.projectiles = []
        self.assets = Assets().fetch()

        self.midpoint = (150, 100)
        
        self.cursor = self.assets['cursor'].copy()
    
    def draw_curve(self, surf, origin, angle, speed):

        m_points = list(origin).copy()
        y_vel = 0

        for i in range(51):
            y_vel = min(5, y_vel + 0.01) 
            m_points[0] += math.cos(angle) * speed
            m_points[1] += math.sin(angle) * speed + y_vel

            if i % 5 == 0:
                pygame.draw.circle(surf, (255, 255, 255), m_points, 1)

    def run(self):

        while(True):

            self.display.fill((0, 0, 0))

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] // 2
            mpos[1] = mpos[1] // 2

            angle = self.rotation.get_angle(self.midpoint, mpos)

            print(angle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                   img = pygame.Surface((10, 10))
                   img.fill((255, 255, 255))
                   img.set_colorkey((255,255 ,255))
                   pygame.draw.circle(img, (100, 100, 100), (5, 5), 5)
                   self.projectiles.append(Projectiles(img, 2, math.radians(angle * (-1 if self.rotation.flip_x else 1)), 100, self.midpoint))
            
            
            test_rect = pygame.Rect((*self.midpoint , 10, 10))

            pygame.draw.rect(self.display,(0, 255, 0), test_rect)

            

            img_rect = self.cursor.img().get_rect(center=mpos)
            self.display.blit(self.cursor.img(), img_rect)
            self.cursor.update()

            if test_rect.collidepoint(mpos) :
                for i in range(4):
                    angle = random.random() * math.pi * 2
                    speed = random.random() + 2
                    self.sparks.append(Sparks(angle, speed, mpos, (255,0 ,0)))
            
            for spark in self.sparks.copy():
                spark.render(self.display)

                if spark.update():
                    self.sparks.remove(spark)
            
            for projectile in self.projectiles.copy():
                projectile.render(self.display)

                if projectile.update():
                    self.projectiles.remove(projectile)

            self.draw_curve(self.display, self.midpoint, math.radians(angle * (-1 if self.rotation.flip_x else 1)), 2)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()) , (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()