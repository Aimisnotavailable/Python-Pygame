import pygame
import sys
import math
import random

class Spring:

    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((400, 300))

        self.resting_length = 100
        self.current_length = self.resting_length

        self.displacement = 0
        
        self.stiffness = 0.3
        self.force = 0
        self.mass = 1
        self.damping = 0.98

        self.clicking = False
        self.pos=[200, 100]
        self.bob_pos = [200, 200]
        self.velocity = 0
        pygame.init()

        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        
        
    
    def run(self):

        while True:
            
            self.display.fill((255, 255, 255))

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0]//2
            mpos[1] = mpos[1]//2

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

            self.displacement = self.current_length - self.resting_length

            if self.clicking:
                self.current_length+=1
            else:
                spring_force = (-self.stiffness * self.displacement)
                damping_force = self.damping * self.velocity

                total_force = spring_force + damping_force
                
                self.velocity += total_force

                self.bob_pos[1] += self.velocity

            pygame.draw.rect(self.display, (0, 0, 0), (*mpos, 4, 4))
            
            pygame.draw.line(self.display, (0, 0, 255), (200, self.pos[1]), (self.bob_pos))
            pygame.draw.circle(self.display, (255, 0, 0), self.pos, 5)
            pygame.draw.circle(self.display, (0, 255, 0), (self.bob_pos[0], self.bob_pos[1]), 5)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Spring().run()