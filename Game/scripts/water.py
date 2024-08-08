import pygame
from scripts.water_springs import WaterSpring

class Water:
    def __init__(self):
        self.water_surf = pygame.Surface((16, 16), pygame.SRCALPHA)
        self.pull_force = 0
        self.springs=[WaterSpring([x, 16]) for x in range(0, 17, 4)]
        self.horizontal_damping = 0.8

    def wave(self, index=0, push_force = 0, upward_force=1):
        
        self.springs[index].force = upward_force
        # self.springs[index].velocity[0] = push_force
        left = index - 1
        right = index + 1
       # Propagate wave to the left
        while left >= 0:
            self.springs[left].force = self.springs[left+1].force * 0.4
            # self.springs[left].velocity[0] = self.springs[left + 1].velocity[0] * self.horizontal_damping
            left -= 1
        
        # Propagate wave to the right
        while right < len(self.springs):
            self.springs[right].force = self.springs[right-1].force * 0.4
            # self.springs[right].velocity[0] = self.springs[right - 1].velocity[0] * self.horizontal_damping
            right += 1
        
    def update(self):
        for spring in self.springs:
            spring.update()

    def render(self, surf, pos=(0, 0), offset=(0, 0)):
        self.water_surf.fill((255, 255, 255, 0))
        render_points = []
        
        for spring in self.springs:
            render_points.append(spring.pos)

        render_points.append((16, 16))
        render_points.append((0, 16))

        pygame.draw.polygon(self.water_surf, (0, 0, 255, 100), render_points)
        pygame.draw.aalines(self.water_surf, (255, 255, 255), False, render_points[0 : -2])

        surf.blit(self.water_surf, (pos[0] - offset[0], pos[1] - offset[1]))
        self.update()