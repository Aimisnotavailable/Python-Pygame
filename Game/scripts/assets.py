import pygame
from scripts.utils import load_image, load_images, Animation

class Assets:

    def __init__(self):
        water = []
        water.append(pygame.Surface((16, 16), pygame.SRCALPHA))
        water[0].fill((0, 0, 255, 100))
        self.assets = {
            "background" : { "background" : load_image("background.png"),
                            "clouds" : load_image("clouds\cloud.png")
                           },
            "tooltips"   : { "cursor" : Animation(load_images("cursor"), image_dur=7),
                               "inventory_slot" : load_images("inventory/slot")
                           },

            "blocks"     : { "grass"  : load_images("tiles/grass"),
                             "stone"  : load_images("tiles/stone"),
                             "water"  : water
                           },

            "spawner"    : { "entity_spawner" : load_images("spawners")
                           },
                      
            "entity_animation" : {
                            "player/idle" : Animation(load_images("entities/player/idle"), image_dur=10),
                            "player/jump" : Animation(load_images("entities/player/jump")),
                            "player/run" : Animation(load_images("entities/player/run"), image_dur=5),
                            #player/attack" : Animation(load_images("entities/player/attack"), image_dur=5),
                            
                            "enemy/idle" : Animation(load_images("entities/enemy/idle"), image_dur=7),
                            "enemy/damaged" : Animation(load_images("entities/enemy/damaged")),
                            "enemy/run" : Animation(load_images("entities/enemy/run"), image_dur=5),
                            "enemy/attack" : Animation(load_images("entities/enemy/attack"), image_dur=6),
                       },
            "particles" : { "particles/particles" : Animation(load_images("particles/particles")) }
            }
    

    def fetch(self, obj_types=[], fetch_all=False):
        assets = {}
        if fetch_all:
            obj_types = list(self.assets)

        for obj_type in obj_types:
            assets.update(self.assets[obj_type])
        return assets