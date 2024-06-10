import pygame
import sys
import os
import random
from scripts.utils import load_image, load_images
from scripts.tilemap import TileMap

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Game")

        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))

        self.clock = pygame.time.Clock()

        self.movement = [0, 0]

        self.render_scroll = [0, 0]

        self.assets = {"grass" : load_images("tiles/grass")}
        self.tilemap = TileMap(self)
        self.tilemap.load("data/maps/map.json")

    def run(self):
        running = True

        while running:

            self.display.fill((25, 201, 224))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[1] = -1
                    
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = 1
                    
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = -1

                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 1
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[1] = 0

                    if event.key == pygame.K_DOWN:
                        self.movement[1] = 0

                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0

                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 0
                    
            self.tilemap.render(self.display)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)   
    
Game().run()