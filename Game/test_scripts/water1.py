import pygame
from test_scripts.spring_t import Spring

class Water:
    def __init__(self):
        self.water_surf = pygame.Surface((160, 32), pygame.SRCALPHA)
        self.pull_force = 0
        self.springs=[Spring([x, 16]) for x in range(0, 161, 4)]

    def wave(self, index=0):
        
        self.springs[index].force = 1
        left = index - 1
        right = index + 1
       # Propagate wave to the left
        while left >= 0:
            self.springs[left].force = -self.springs[left+1].force * 0.4
            left -= 1
        
        # Propagate wave to the right
        while right < len(self.springs):
            self.springs[right].force = -self.springs[right-1].force * 0.4
            right += 1
        
    def update(self):
        for spring in self.springs:
            spring.update()

    def render(self, surf, offset=(0, 0)):
        self.water_surf.fill((255, 255, 255, 0))
        render_points = []
        
        for spring in self.springs:
            render_points.append(spring.pos)

        render_points.append((160, 32))
        render_points.append((0, 32))

        pygame.draw.polygon(self.water_surf, (0, 0, 255, 100), render_points)
        pygame.draw.aalines(self.water_surf, (255, 255, 255), False, render_points[0 : -2])

        surf.blit(self.water_surf, (160 - offset[0], 96 - offset[1]))
        self.update()