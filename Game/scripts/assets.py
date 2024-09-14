import pygame
from scripts.utils import load_image, load_images, load_sound, load_sounds, Animation

class Assets:

    def __init__(self):
        water = []
        water.append(pygame.Surface((16, 16), pygame.SRCALPHA))
        water[0].fill((0, 0, 255, 100))
        self.assets = {
            
            'img' : {
                      "background" : { "background" : load_images("backgrounds"),
                                        "clouds" : load_images("clouds")
                                      },
                      "tooltips"   : { "cursor" : Animation(load_images("cursor"), image_dur=7),
                                        "inventory_slot" : load_images("inventory/slot")
                                      },

                      "blocks"     : { "grass"  : load_images("tiles/grass"),
                                        "stone"  : load_images("tiles/stone"),
                                        "sand"   : load_images("tiles/sand"),
                                        "water"  : water
                                      },
                      
                      "decors"     :{
                                      "tree"    : load_images("decors")
                                    },

                      "spawners"    : { "entity_spawner" : load_images("spawners")
                                      },
                                
                      "entity_animation" : {
                                      "player/idle" : Animation(load_images("entities/player/idle"), image_dur=10),
                                      "player/jump" : Animation(load_images("entities/player/jump")),
                                      "player/run"  : Animation(load_images("entities/player/run"), image_dur=5),
                                      "player/fade" : Animation(load_images("entities/player/fade"), image_dur=3),
                                      "player/wall_slide" : Animation(load_images("entities/player/wall_slide/")),
                                      #player/attack" : Animation(load_images("entities/player/attack"), image_dur=5),
                                      
                                      "enemy/idle" : Animation(load_images("entities/enemy/idle"), image_dur=7),
                                      "enemy/damaged" : Animation(load_images("entities/enemy/damaged")),
                                      "enemy/run" : Animation(load_images("entities/enemy/run"), image_dur=5),
                                      "enemy/attack" : Animation(load_images("entities/enemy/attack"), image_dur=6),
                                      "enemy/hat"    : Animation(load_images("entities/enemy/hat"), image_dur=6),
                                  },

                      "particles" : { "particles/particles" : Animation(load_images("particles/particles")),
                                      "particles/dust" : Animation(load_images("particles/dust"), image_dur=2, loop=False),
                                      "particles/leaf" : Animation(load_images("particles/leaf"), image_dur=15, loop=False),
                                      "particles/snow" : Animation(load_images("particles/snow"), image_dur=15, loop=True),
                                    },
                      "christmas" : {
                                      "christmas/santa" : Animation(load_images("santa"), image_dur=5),
                      }
            },

            "sfx" : {
                      "background": {
                          "background_music" : load_sounds('music'),
                      },

                      "player" : {
                          "teleport" : load_sounds('sfx/entity_sfx/player/teleport')
                      },

                      "weapon" : {
                          "guns" : load_sounds('sfx/gun_sfx'),
                          "swords" : load_sounds('sfx/sword_sfx')
                      },

                      "tile" : {
                          'grass' : load_sounds('sfx/tile_sfx/grass'),
                          'sand'  : load_sounds('sfx/tile_sfx/sand'),
                          'stone' : load_sounds('sfx/tile_sfx/stone'),
                      },
                      },
            }
    

    def fetch(self, payload={}, fetch_all=False):
        assets = {}
        if fetch_all:
          file_types = list(self.assets)
          for file_type in file_types:
              for obj_type in self.assets[file_type]:
                assets.update(self.assets[file_type][obj_type])
          return assets
        else:
          for file_type in payload:
            if 'all' in payload[file_type]:
               for obj_type in self.assets[file_type]:
                  assets.update(self.assets[file_type][obj_type])
            else:
              for obj_type in payload[file_type]:
                assets.update(self.assets[file_type][obj_type])
          return assets 