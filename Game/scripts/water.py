import pygame
import math
import copy
class Water:
    
    def __init__(self):
        self.water_surf = pygame.Surface((160, 32), pygame.SRCALPHA)
        self.line_points = [[x, 16] for x in range(160)]
        self.collide = False
        self.velocity = 0
        self.x_pos = 0

    def rect(self):
        return pygame.Rect(160, 112, 160, 16)

    def render(self, surf, offset=(0, 0)):
        
        self.water_surf.fill((255, 255, 255, 0))
        wave_points = copy.deepcopy(self.line_points)

        count = 0

        if self.velocity > 0:
            for i in range(max(0, self.x_pos - 15), min(160, self.x_pos + 15)):
                y = math.sin(count) * self.velocity
                wave_points[i][1] = max(1, self.line_points[i][1] - y)
                count+=0.1

            self.x_pos = min(160, (self.x_pos + 1))

        self.velocity = max(0, self.velocity - 0.1)
        render_points = [
            *wave_points,
            (160, 32),
            (0, 32)
        ]

        pygame.draw.polygon(self.water_surf, (0, 0, 255, 100), render_points)
        pygame.draw.aalines(self.water_surf, (255, 255, 255, 200), False, wave_points)

        surf.blit(self.water_surf, (160 - offset[0], 96 - offset[1]))
    
