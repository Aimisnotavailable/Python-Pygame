import pygame

class Transition:
    
    def __init__(self):
        self.dur = 80
        self.transition = False
        self.size = 200
        
    def update(self):
        if self.dur > 0:
            self.size += -5 if self.dur > 40 else 5
        else:
            self.dur = 80
            self.size = 200
            self.transition = False
    
    def render(self, surf):
        cover = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        cover.fill((0, 0, 0))
        pygame.draw.circle(cover, (0, 0, 0, 0), (surf.get_width()//2, surf.get_height()//2), self.size)

        surf.blit(cover, (0, 0))
        self.dur -= 1
        self.update()
        

