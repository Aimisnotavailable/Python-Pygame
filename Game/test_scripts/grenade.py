import pygame
import sys

from scripts.rotation import Rotation
from scripts.tilemap import *


class Game:

    def __init__(self):

        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))

        pygame.init()

        self.clock = pygame.time.Clock()
        self.rotation = Rotation()

        self.tilemap = TileMap(self)
        
    
    def run(self):

        while(True):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display.fill((255, 255, 255))
            self.tilemap.render(self.display)

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()) , (0, 0))
            pygame.display.update()


Game().run()