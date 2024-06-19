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

        self.tile_variant = 0
        self.clicking = False
        self.right_clicking = False

    def run(self):
        running = True

        while running:

            self.display.fill((25, 201, 224))
            self.render_scroll[0] += self.movement[0] * RENDER_SCALE
            self.render_scroll[1] += self.movement[1] * RENDER_SCALE

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)

            tile_pos =(int((mpos[0] + self.render_scroll[0])//self.tilemap.tile_size), int((mpos[1] + self.render_scroll[1])//self.tilemap.tile_size))

            current_image = self.assets['grass'][self.tile_variant].copy()
            current_image.set_alpha(100)

            self.display.blit(current_image, (tile_pos[0] * self.tilemap.tile_size - self.render_scroll[0], tile_pos[1] * self.tilemap.tile_size - self.render_scroll[1]))
            self.display.blit(current_image, (5,5))

            key = str(tile_pos[0]) + ";" + str(tile_pos[1])
            
            print(key)
            if self.clicking:
                if not (key in self.tilemap.tilemap):
                    self.tilemap.tilemap[key] = {"type": "grass", "variant": self.tile_variant, "pos": [tile_pos[0], tile_pos[1]]}
            
            if self.right_clicking:
                if key in self.tilemap.tilemap:
                    del self.tilemap.tilemap[key]

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                    
                    if event.button == 3:
                        self.right_clicking = True
                    
                    if event.button == 4:
                        self.tile_variant = (self.tile_variant + 1) % len(self.assets['grass'])
                    
                    if event.button == 5:
                        self.tile_variant = ((self.tile_variant - 1)+ len(self.assets['grass'])) % len(self.assets['grass'])
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = -1
                    if event.key == pygame.K_d:
                        self.movement[0] = 1

                    if event.key == pygame.K_s:
                        self.movement[1] = 1
                    if event.key == pygame.K_w:
                        self.movement[1] = -1

                    if event.key == pygame.K_k:
                        self.tilemap.save("data/maps/map.json")
                    
                    if event.key == pygame.K_t:
                        self.tilemap.auto_tile()
                
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = 0
                    if event.key == pygame.K_d:
                        self.movement[0] = 0

                    if event.key == pygame.K_w:
                        self.movement[1] = 0
                    if event.key == pygame.K_s:
                        self.movement[1] = 0
                
                    
            self.tilemap.render(self.display, offset=self.render_scroll)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)   
    
Game().run()