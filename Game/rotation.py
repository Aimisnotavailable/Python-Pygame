import pygame
import math
import sys
import random
from scripts.utils import load_image
from scripts.sparks import Sparks

QUADRANTS = {(1, 0) : 0,
             (0, 0) : 180,
             (0, 1) : 180,
             (1, 1) : 360
             }

class Rotation:
    def rect(self, pos, size):
        return pygame.Rect(pos[0], pos[1], size[0], size[1])
    
    def run(self):
        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))
        self.img = load_image('items/weapons/guns/weapon_animation/dirt_gun/0.png')
        pygame.init()

        self.clock = pygame.time.Clock()
        angle = 0
        midpoint = [150, 100]
        mpos = (400, 372)
        self.flip_x = 0
        self.flip_y = 0
        original_size = self.img.get_size()

        self.img_pos = midpoint
        self.sparks = []
        self.projectiles = []
        self.clicking = False

        self.cd = 0
        while True:
            self.display.fill((100, 0, 100))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0]//2 , mpos[1]//2)
            
            self.flip_x = 1 if mpos[0] > midpoint[0] else 0
            self.flip_y = 1 if mpos[1] > midpoint[1] else 0

            quad = (self.flip_x, self.flip_y)

            x = (mpos[0] - midpoint[0])
            y = (mpos[1] - midpoint[1])

            if x != 0:
                angle = int((math.atan(y/x) * (-1 if self.flip_x else 1) * (180 / math.pi) ) + QUADRANTS[quad])
            else:
                angle = 90 if self.flip_y else 270

            img = pygame.transform.rotate(self.img , angle)

            pygame.draw.line(self.display, (255, 255, 255), midpoint, (mpos[0], mpos[1]))

            img_rect = img.get_rect(center=(self.img_pos))

            self.display.blit(pygame.transform.flip(img, False ,  not self.flip_x), img_rect)
            print(angle)

            if self.clicking:
                if self.cd == 0:
                    # midpoint[0] += math.cos((-(angle + 180) * math.pi)/180) * 3
                    # midpoint[1] += math.sin((-(angle + 180) * math.pi)/180) * 3
                    sp_x = math.cos(((-angle if self.flip_x else angle) * math.pi)/180) * 10 + (midpoint[0])
                    sp_y = math.sin(((-angle if self.flip_x else angle) * math.pi)/180) * 10 + (midpoint[1])
                    for i in range(2):
                        s_angle = ((-angle if self.flip_x else angle) * math.pi)/180 + random.random() - 0.5
                        s_speed = random.random() + 2
                        self.sparks.append(Sparks(s_angle ,s_speed, (sp_x, sp_y)))
                    self.projectiles.append([[sp_x, sp_y], 2, ((-angle if self.flip_x else angle) * math.pi)/180, 300])
                    #self.cd = 10

            self.cd = max(0, self.cd - 1)
            for spark in self.sparks.copy():
                spark.render(self.display)
                if spark.update():
                    self.sparks.remove(spark)
            
            for projectile in self.projectiles.copy():
                projectile[0][0] += math.cos(projectile[2]) * projectile[1]
                projectile[0][1] += math.sin(projectile[2]) * projectile[1]
                pygame.draw.circle(self.display, (0, 0, 0), projectile[0], 3)
                projectile[-1] -= 1
                if not projectile[-1]:
                    self.projectiles.remove(projectile)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Rotation().run()