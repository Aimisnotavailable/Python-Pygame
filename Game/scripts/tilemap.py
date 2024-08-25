import pygame
import json
import random
from scripts.water import Water

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

PHYSICS_TILES = {'grass', 'stone', 'sand'}
AUTO_TILE_TYPES = {'grass', 'stone', 'sand'}

COLORS = {
            'grass' : [(95, 193, 0 ),
                       (86, 170, 5),
                       (67, 136, 0),
                       (181, 110, 76),
                       (96, 59, 42),
                       (143, 86, 59),],
            'stone' : [(194, 194, 209),
                       (126, 126, 143),
                       (67, 67, 79),
                       (96, 96, 112),],
            'sand'  : [(186, 163, 74),
                        (216, 188, 80),
                        (160, 137, 49),],

}

TILE_TYPES = {'solid' : PHYSICS_TILES, 'liquid' : 'water'}


class TileMap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []
        self.water_map = {}
        self.interactive_water = {}
        self.nearby_water = {}

    def extract(self, id_pairs, keep=True):
        results = []

        for tile in self.offgrid_tiles.copy():
            
            if (tile['type'], tile['variant']) in id_pairs:
                results.append(tile.copy())
                results[-1]['pos'] = tile['pos'].copy()
                print(results[-1])
                if not keep:
                    self.offgrid_tiles.remove(tile)

        for loc in self.tilemap.copy():
            tile = self.tilemap[loc]
            
            if (tile['type'], tile['variant']) in id_pairs:
                results.append(tile.copy())
                results[-1]['pos'] = tile['pos'].copy()
                results[-1]['pos'][0] *= self.tile_size
                results[-1]['pos'][1] *= self.tile_size

                if not keep:
                    del self.tilemap[loc]

        return results
            


    def render(self, surf, offset=(0,0), grid_enabled=False):
        for tile in self.offgrid_tiles:
            img_rect = self.game.assets[tile['type']][tile['variant']].get_rect(centerx=tile['pos'][0] - offset[0], bottom=tile['pos'][1] - offset[1])
            surf.blit(self.game.assets[tile['type']][tile['variant']], img_rect)

        for x in range(offset[0] // self.tile_size -48, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size -48, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if grid_enabled:
                    pygame.draw.rect(surf, (0, 0, 0), (x * self.tile_size - offset[0], y * self.tile_size - offset[1], self.tile_size , self.tile_size), 1)

                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

                if loc in self.water_map:
                    self.nearby_water[loc] = (x, y)
            
    def render_water(self, surf, offset=(0, 0)):

        for loc in self.nearby_water.copy():
            x, y = self.nearby_water[loc]
            tile = self.water_map[loc]

            if tile['interactive']:
                water = self.interactive_water[loc]
                water.render(surf, pos=(x * self.tile_size, y * self.tile_size), offset=offset)
            else:
                surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))

            del self.nearby_water[loc]
            
            
    def tiles_around(self, pos, type):   
        physics_tiles = []
        tile_loc = (int((pos[0])//self.tile_size), int((pos[1])//self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            key = str(tile_loc[0] + offset[0]) + ';' + str(tile_loc[1] + offset[1])
            if type == 'solid':
                if key in self.tilemap and self.tilemap[key]['type'] in PHYSICS_TILES:
                    physics_tiles.append(self.tilemap[key])
        return physics_tiles
    
    def solid_check(self, pos):
        tile_loc = str(int((pos[0] //self.tile_size))) + ";" + str(int((pos[1]//self.tile_size)))
        if tile_loc in self.tilemap:
            if self.tilemap[tile_loc]['type'] in PHYSICS_TILES:
                return True
            return False

    def tiles_rect_around(self, pos, type='solid'):
        tile_data = {'rects' : [], 'color' : []}
        for tile in self.tiles_around(pos, type):
            tile_data['rects'].append(pygame.Rect(tile['pos'][0] * self.tile_size, tile['pos'][1] * self.tile_size, self.tile_size, self.tile_size))
            tile_data['color'].append(random.choice(COLORS[tile['type']]))
        return tile_data

    
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
    
    def validate_water_blocks(self):

        for loc in self.water_map.copy():
            water = self.water_map[loc]
            check_loc = str(water['pos'][0]) + ';' + str(water['pos'][1] -1)

            if not check_loc in self.water_map:
                water['interactive'] = True
            else:
                water['interactive'] = False
        
        self.group_interactive_water()
    
    def group_interactive_water(self):
        for loc in self.water_map.copy():
            water = self.water_map[loc]
            
            if water['interactive']:
                if not loc in self.interactive_water:
                    self.interactive_water[loc] = Water()
            else:
                if loc in self.interactive_water:
                    del self.interactive_water[loc]
                
    def propogate_wave(self, water_loc, water_loc_int, velocity=(0,0), offset=(0,0), entity_rect=None):

        water_data = self.water_map[water_loc]
        
        if water_data['interactive']:
            water = self.interactive_water[water_loc]
            for i in range(len(water.springs)):
                pos = water.springs[i].pos
                if entity_rect.collidepoint((pos[0] + water_data['pos'][0] * self.tile_size + offset[0], pos[1] + water_data['pos'][1] * self.tile_size + offset[1])):
                    water.wave(i, force=-velocity[1] * 2)

            temp_loc = water_loc_int.copy()
            previous_water = water
            while(str(temp_loc[0]) + ";" + str(temp_loc[1]) in self.interactive_water):
                if(abs(water.springs[-1].force) > 0.01):
                    right_water_loc = str(temp_loc[0]) + ";" + str(temp_loc[1])
                    if right_water_loc in self.water_map:
                        right_water = self.interactive_water[right_water_loc]
                        right_water.wave(0, force=previous_water.springs[-1].force)
                        previous_water = right_water
                temp_loc[0] += 1

            temp_loc = water_loc_int.copy()
            previous_water = water
            while(str(temp_loc[0]) + ";" + str(temp_loc[1]) in self.interactive_water):
                if(abs(water.springs[0].force) > 0.001):
                    left_water_loc = str(temp_loc[0] - 1) + ";" + str(temp_loc[1])
                    if left_water_loc in self.water_map:
                        left_water = self.interactive_water[left_water_loc]
                        left_water.wave(-1, force=previous_water.springs[0].force)
                        previous_water = left_water
                temp_loc[0] -= 1

    def save(self, path):
        f = open(path, 'w')
        json.dump({'tilemap' : self.tilemap, 'tile_size' : self.tile_size, 'offgrid' : self.offgrid_tiles, 'watermap' : self.water_map}, f)
        f.close()

    def load(self, path):
        f = open(path, 'r')
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data['tilemap']
        self.tile_size = map_data['tile_size']
        self.offgrid_tiles = map_data['offgrid']
        self.water_map = map_data['watermap']
        self.group_interactive_water()
            
        
       
    
