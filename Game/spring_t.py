import pygame
import sys
import math
import random

class Spring:

    def __init__(self, pos, velocity=(0,0)):
        self.resting_length = 16

        self.pos = list(pos)
        self.velocity = list(velocity)
        self.damping = 0.95
        self.gravity = 0.8
        
        self.spring_const = 0.1
        self.displacement = 0
        self.total_force = 0
        
    def update(self, force=0):
        
        self.displacement = self.pos[1] - self.resting_length

        spring_force = -self.spring_const * self.displacement 
        self.total_force = spring_force + self.gravity + force

        self.velocity[1] = self.velocity[1] * self.damping + self.total_force

        self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]


    def render(self, surf):
        pygame.draw.circle(surf, (255, 255, 255), (self.pos[0], self.pos[1]), 5)
        self.update()
        
        
class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((600,400))
        self.display = pygame.Surface((300, 200))

        pygame.init()
        self.clock = pygame.time.Clock()
        self.clicking = False
        self.pull_force = 0
        self.springs=[]
        for i in range(0, 150, 15):
            self.springs.append(Spring((i + 100, 100)))
        pygame.mouse.set_visible(False)
    
    def wave(self, index=0):
        
        self.springs[index].update(-10)
        left = index
        right = index

        while right != len(self.springs) or left != -1:
            left = max(-1, left-1)
            right = min(len(self.springs), right + 1)
            
            if left != -1:
                self.springs[left].update(self.springs[left+1].total_force * 0.6)
            if right != len(self.springs):
                self.springs[right].update(self.springs[right-1].total_force * 0.6)

        
    def run(self):

        while True:

            self.display.fill((100, 100, 100))

            mpos = pygame.mouse.get_pos()
            mpos = [mpos[0]//2, mpos[1]//2]

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicking = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.clicking = False
                    self.pull_force = 0

                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_LEFT:
                #         self.ball_velocity[0] = -1
                #     if event.key == pygame.K_RIGHT:
                #         self.ball_velocity[0] = 1
                #     if event.key == pygame.K_UP and self.ball_velocity:
                #         self.ball_velocity[1] = -10

                # if event.type == pygame.KEYUP:
                #     if event.key == pygame.K_LEFT:
                #         self.ball_velocity[0] = 0
                #     if event.key == pygame.K_RIGHT:
                #         self.ball_velocity[0] = 0

            pygame.draw.circle(self.display, (0, 0, 0), mpos, 5)

            if self.clicking:
                self.pull_force += 0.5

            for i in range(len(self.springs)):
                pos = self.springs[i].pos
                spring_rect = pygame.Rect(pos[0], pos[1], 5, 5)
                if spring_rect.collidepoint(mpos):
                    self.wave(i)

                #self.springs[i].update()
                self.springs[i].render(self.display)
                
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

# Game().run()