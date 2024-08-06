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

        water = []
        water.append(pygame.Surface((16, 16)))
        water[0].fill((0, 0, 255))
        water2 = []
        water2.append(pygame.Surface((16, 16)))
        water2[0].fill((0, 255, 0))
        self.assets = {"grass" : load_images("tiles/grass"),
                       "stone" : load_images("tiles/stone"),
                       "water" : water,
                       "water2" : water2}
        

        self.tilemap = TileMap(self)
        self.tilemap.load("data/maps/map.json")
        self.tile_list = list(self.assets)

        self.tile_group = 0
        self.tile_variant = 0

        self.shift = False
        self.clicking = False
        self.right_clicking = False

        self.font = pygame.font.Font(size=15)

        
    def run(self):
        running = True

        while running:
            self.display.fill((255, 255, 255))
            self.render_scroll[0] += self.movement[0] * RENDER_SCALE
            self.render_scroll[1] += self.movement[1] * RENDER_SCALE

            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)

            tile_pos =(int((mpos[0] + self.render_scroll[0])//self.tilemap.tile_size), int((mpos[1] + self.render_scroll[1])//self.tilemap.tile_size))

            current_image = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_image.set_alpha(100)

            # for x in range(self.render_scroll[0] // self.tilemap.tile_size, (self.render_scroll[0] + self.display.get_width()) // self.tilemap.tile_size + 1):
            #     for y in range(self.render_scroll[1] // self.tilemap.tile_size, (self.render_scroll[1] + self.display.get_height()) // self.tilemap.tile_size + 1):
            #         pygame.draw.rect(self.display, (255, 255, 255), (x * self.tilemap.tile_size - self.render_scroll[0], y * self.tilemap.tile_size - self.render_scroll[1], self.tilemap.tile_size , self.tilemap.tile_size), 1)
                    
            key = str(tile_pos[0]) + ";" + str(tile_pos[1])
            
            if self.clicking:
                if self.tile_list[self.tile_group] == "water":
                    self.tilemap.water_map[key] = {"type": self.tile_list[self.tile_group], "variant": self.tile_variant, "pos": [tile_pos[0], tile_pos[1]], "interactive" : False}
                elif not (key in self.tilemap.tilemap):
                    self.tilemap.tilemap[key] = {"type": self.tile_list[self.tile_group], "variant": self.tile_variant, "pos": [tile_pos[0], tile_pos[1]]}
            
            if self.right_clicking:
                if key in self.tilemap.tilemap:
                    del self.tilemap.tilemap[key]
                if key in self.tilemap.water_map:
                    del self.tilemap.water_map[key]

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
                        if self.shift:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                            self.tile_variant = 0
                        else:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])
                    
                    if event.button == 5:
                        if self.shift:
                            self.tile_group = ((self.tile_group -1) + len(self.tile_list)) % len(self.tile_list)
                            self.tile_variant = 0
                        else:
                            self.tile_variant = ((self.tile_variant - 1)+ len(self.assets[self.tile_list[self.tile_group]])) % len(self.assets[self.tile_list[self.tile_group]])
                
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
                        self.tilemap.validate_water_blocks()

                    if event.key == pygame.K_r:
                        self.tilemap.tilemap = {}

                    if event.key == pygame.K_LSHIFT:
                        self.tile_group = 0
                        self.shift = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = 0
                    if event.key == pygame.K_d:
                        self.movement[0] = 0

                    if event.key == pygame.K_w:
                        self.movement[1] = 0
                    if event.key == pygame.K_s:
                        self.movement[1] = 0
                    
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
                
            self.tilemap.render(self.display, offset=self.render_scroll, grid_enabled=True)
            text  = self.font.render(str(mpos[0] + self.render_scroll[0]) + ';' + str(mpos[1] + self.render_scroll[1]), True, (255, 0, 255))
            self.display.blit(text, (0, 32))

            self.display.blit(current_image, (tile_pos[0] * self.tilemap.tile_size - self.render_scroll[0], tile_pos[1] * self.tilemap.tile_size - self.render_scroll[1]))
            self.display.blit(current_image, (5,5))

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))

            pygame.display.update()
            self.clock.tick(60)   
    
Game().run()