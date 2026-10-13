import pygame
import sys
import math
import random
import copy
class Water:
    
    def __init__(self):

        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))

        self.water_surf = pygame.Surface((100, 30), pygame.SRCALPHA)
        self.box = pygame.Surface((20, 20))
        pygame.init()

        self.count = 0
        self.clock = pygame.time.Clock()
        self.line_points = [[x, 15] for x in range(100)]
        self.collide = False
        self.velocity = 0
        self.x_pos = 0

        self.stones = []

    def water(self, color=(0, 0, 255, 40)):
        
        wave_points = copy.deepcopy(self.line_points)

        count = 0

        if self.velocity > 0:
            for i in range(max(0, self.x_pos - 15), min(100, self.x_pos + 15)):
                y = math.sin(count) * self.velocity
                wave_points[i][1] = max(1, self.line_points[i][1] - y)
                count+=0.1

            self.x_pos = min(100, (self.x_pos + 1))
        render_points = [
            *wave_points,
            (102, 30),
            (0, 30)
        ]

        pygame.draw.polygon(self.water_surf, color, render_points)
        pygame.draw.aalines(self.water_surf, (0, 0, 0), False, wave_points)
        
    def run(self):

        while True:
            self.display.fill((100, 100, 100))
            self.water_surf.fill((255, 255, 255))
            
            mpos = list(pygame.mouse.get_pos())
            
            mpos[0] = mpos[0] // 2
            mpos[1] = mpos[1] // 2

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.stones.append([*mpos, 4, 4])
                
            box_rect = self.box.get_rect(center=(mpos[0], mpos[1]))

            pygame.draw.rect(self.display, (255, 255, 255), box_rect)

            water_rect = pygame.Rect(100, 115, 100, 15)

            color = (0, 0, 255, 40)
            
            

            for stone in self.stones.copy():

                stone[1] += 1
                pygame.draw.rect(self.display, (255, 255, 255), stone)
                if stone[1] >= 150:
                    self.stones.remove(stone)

                if self.velocity == 0:
                    if water_rect.collidepoint(stone[0:2]):
                        if not self.collide:
                            self.velocity = 10
                            self.x_pos = stone[0] - 100
                        self.collide = True
                    else:
                        self.collide = False

            #self.splash((100, 15))
            self.velocity = max(0, self.velocity - 0.1)
            self.water(color=color)
            #pygame.draw.rect(self.display, (255, 255, 255), water_rect)

            self.display.blit(self.water_surf, (100, 100))
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Water().run()