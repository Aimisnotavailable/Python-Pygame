import pygame
import sys
import os
import random
from scripts.utils import load_image, load_images
from scripts.tilemap import TileMap

RENDER_SCALE = 2
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
            self.render_scroll[0] += self.movement[0] * RENDER_SCALE
            self.render_scroll[1] += self.movement[1] * RENDER_SCALE
            current_image = self.assets['grass'][0].copy()
            current_image.set_alpha(100)
            self.display.blit(current_image, (5,5))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = int(((pos[0])//RENDER_SCALE + self.render_scroll[0])//self.tilemap.tile_size)
                    y = int(((pos[1])//RENDER_SCALE + self.render_scroll[1])//self.tilemap.tile_size)
                    key = str(x) + ";" + str(y)

                    if event.button == 1:
                        if not(key in self.tilemap.tilemap):
                            self.tilemap.tilemap[key] = {"type": "grass", "variant": 0, "pos": [x, y]}
                    
                    if event.button == 3:
                        if key in self.tilemap.tilemap:
                            del self.tilemap.tilemap[key]


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = -1
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 1

                    if event.key == pygame.K_DOWN:
                        self.movement[1] = 1
                    if event.key == pygame.K_UP:
                        self.movement[1] = -1

                    if event.key == pygame.K_k:
                        self.tilemap.save("data/maps/map.json")
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 0

                    if event.key == pygame.K_DOWN:
                        self.movement[1] = 0
                    if event.key == pygame.K_UP:
                        self.movement[1] = 0
                
                    
            self.tilemap.render(self.display, offset=self.render_scroll)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)   
    
Game().run()