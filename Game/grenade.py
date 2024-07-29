import pygame
import sys
import math
import random

from scripts.rotation import Rotation
from scripts.sparks import Sparks



class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))

        pygame.init()

        self.clock = pygame.time.Clock()
        self.rotation = Rotation()

        self.sparks = []
    
    def run(self):

        while(True):
            
            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] // 2
            mpos[1] = mpos[1] // 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            
            self.display.fill((255, 255, 255))

            test_rect = pygame.Rect((150, 100, 10, 10))

            pygame.draw.rect(self.display,(0, 255, 0), test_rect)
            pygame.draw.circle(self.display, (0, 0, 0), mpos, 1)

            if test_rect.collidepoint(mpos) :
                for i in range(4):
                    angle = random.random() * math.pi * 2
                    speed = random.random() + 2
                    self.sparks.append(Sparks(angle, speed, mpos, (255,0 ,0)))
            
            for spark in self.sparks.copy():
                spark.render(self.display)

                if spark.update():
                    self.sparks.remove(spark)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()) , (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()