import pygame
import json

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0,0), (-1, 1), (0, 1), (1, 1)]

class TileMap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def render(self, surf, offset=(0,0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

    def tiles_around(self, pos):   
        physics_tiles = []
        tile_loc = (int((pos[0])//self.tile_size), int((pos[1])//self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            key = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if key in self.tilemap:
                physics_tiles.append(self.tilemap[key])
        return physics_tiles
    
    def solid_check(self, pos):
        tile_loc = str(int((pos[0]//self.tile_size))) + ";" + str(int((pos[1]//self.tile_size)))
        
        if tile_loc in self.tilemap:
            return self.tilemap[tile_loc]

    def tiles_rect_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
    
        return rects
    
    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap' : self.tilemap, 'tile_size' : self.tile_size, 'offgrid' : self.offgrid_tiles}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
            
        
       
    
