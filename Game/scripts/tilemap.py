import pygame
import json

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0,0), (-1, 1), (0, 1), (1, 1)]


AUTO_TILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])) : 0,
    tuple(sorted([(-1,0), (1, 0),(0, 1)])) : 1,
    tuple(sorted([(-1, 0), (1,0)])) : 1,
    tuple(sorted([(-1, 0), (0, 1)])) : 2,
    tuple(sorted([(-1, 0)])) : 2,
    tuple(sorted([(0,-1), (1, 0), (0, 1)])) : 3,
    tuple(sorted([(-1,0), (0,-1), (1, 0), (0, 1)])) : 4,
    tuple(sorted([(0,-1), (-1, 0), (0, 1)])) : 5,
    tuple(sorted([(1, 0), (0, -1)])) : 6,
    tuple(sorted([(-1, 0), (1, 0), (0, -1)])) : 7,
    tuple(sorted([(-1, 0), (0, -1)])) : 8
}

PHYSICS_TILES = {'grass', 'stone'}
AUTO_TILE_TYPES = {'grass', 'stone'}

class TileMap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def render(self, surf, offset=(0,0), grid_enabled=False):
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if grid_enabled:
                    pygame.draw.rect(surf, (0, 0, 0), (x * self.tile_size - offset[0], y * self.tile_size - offset[1], self.tile_size , self.tile_size), 1)

                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

    def tiles_around(self, pos):   
        physics_tiles = []
        tile_loc = (int((pos[0])//self.tile_size), int((pos[1])//self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            key = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if key in self.tilemap and self.tilemap[key]['type'] in PHYSICS_TILES:
                physics_tiles.append(self.tilemap[key])
        return physics_tiles
    
    def solid_check(self, pos):
        tile_loc = str(int((pos[0] //self.tile_size))) + ";" + str(int((pos[1]//self.tile_size)))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return True
            return False

    def tiles_rect_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            rects.append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
        return rects
    
    def auto_tile(self):
        
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbours = set()

            for shift in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                check_loc = str(tile['pos'][0] + shift[0]) + ';' + str(tile['pos'][1] + shift[1])
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]['type'] == tile['type']:
                        neighbours.add(shift)
            neighbours = tuple(sorted(neighbours))

            if (tile['type'] in AUTO_TILE_TYPES) and (neighbours in AUTO_TILE_MAP):
                tile['variant'] = AUTO_TILE_MAP[neighbours]

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
            
        
       
    
