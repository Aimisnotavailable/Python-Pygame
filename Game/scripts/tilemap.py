import pygame

class TileMap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {"tilemap" : {"0;0":{"type": "grass", "variant": 0, "pos": [5, 5]}},
                        "tile_size": 16}
        self.offgrid_tiles = []

    def render(self, surf, offset=(0,0)):
        for x in range(offset[0] // self.tile_size, (offset[0] + surf.get_width()) // self.tile_size + 1):
            for y in range(offset[1] // self.tile_size, (offset[1] + surf.get_height()) // self.tile_size + 1):
                loc = str(x) + ';' + str(y)
                if loc in self.tilemap["tilemap"]:
                    tile = self.tilemap["tilemap"][loc]
                    print(tile)
                    surf.blit(self.game.assets[tile['type']][tile['variant']],(tile['pos'][0] * self.tile_size - offset[0], tile['pos'][1] * self.tile_size - offset[1]))
            
        
       
    
