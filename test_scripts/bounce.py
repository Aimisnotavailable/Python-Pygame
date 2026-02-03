import pygame
import math
import sys

class Bounce:

    def __init__(self):

        self.screen = pygame.display.set_mode((600,400))
        self.display = pygame.Surface((300, 200))

        pygame.init()
        self.clock = pygame.time.Clock()

        self.ball_pos = [100, 5]
        self.ball_velocity = [0, 0]
        self.damping = 0.95
        self.gravity = 1

        self.resting_length = 100
        self.spring_const = 0.06
        self.displacement = 0
        self.clicking = False
        self.pull_force = 0

    def run(self):

        while True:

            self.display.fill((100, 100, 100))

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicking = True
                if event.type == pygame.MOUSEBUTTONUP:
                    self.clicking = False
                    self.pull_force = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.ball_velocity[0] = -1
                    if event.key == pygame.K_RIGHT:
                        self.ball_velocity[0] = 1
                    if event.key == pygame.K_UP and self.ball_velocity:
                        self.ball_velocity[1] = -10

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.ball_velocity[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.ball_velocity[0] = 0

            if self.clicking:
                self.pull_force += 0.5

            self.displacement = self.ball_pos[1] - self.resting_length

            spring_force = -self.spring_const * self.displacement 
            total_force = spring_force + self.gravity + self.pull_force

            self.ball_velocity[1] = self.ball_velocity[1] * self.damping + total_force
            
            # pygame.draw.line(self.display, (0, 255, 0), (self.ball_pos[0], 100), self.ball_pos)
            # pygame.draw.circle(self.display, (0, 0, 0), (self.ball_pos[0], 100), 5)

            for i in range(0, 100, 5):
                pygame.draw.circle(self.display, (255, 255, 255), (self.ball_pos[0] + i * (2*i)/5, self.ball_pos[1]/ max(1, (i / 5))), 5)

            self.ball_pos = [self.ball_pos[0] + self.ball_velocity[0], self.ball_pos[1] + self.ball_velocity[1]]
            

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Bounce().run()
