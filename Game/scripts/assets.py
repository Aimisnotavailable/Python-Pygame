import pygame
from scripts.utils import load_image, load_images, Animation

class Assets:

    def __init__(self):
        water = []
        water.append(pygame.Surface((16, 16), pygame.SRCALPHA))
        water[0].fill((0, 0, 255, 100))
        self.assets = {"background" : load_image("background.png"),
                       "cursor" : Animation(load_images("cursor"), image_dur=7),
                       "inventory_slot" : load_images("inventory/slot"),
                       "clouds" : load_image("clouds\cloud.png"),
                       "grass" : load_images("tiles/grass"),
                       "stone" : load_images("tiles/stone"),
                       "water" : water,
                       "player" : load_image("entities/player/player.png"),
                       "player/idle" : Animation(load_images("entities/player/idle"), image_dur=10),
                       "player/jump" : Animation(load_images("entities/player/jump")),
                       "player/run" : Animation(load_images("entities/player/run"), image_dur=5),
                       #player/attack" : Animation(load_images("entities/player/attack"), image_dur=5),
                       "enemy" : load_image("entities/enemy/enemy.png"),
                       "enemy/idle" : Animation(load_images("entities/enemy/idle"), image_dur=7),
                       "enemy/damaged" : Animation(load_images("entities/enemy/damaged")),
                       "enemy/run" : Animation(load_images("entities/enemy/run"), image_dur=5),
                       "enemy/attack" : Animation(load_images("entities/enemy/attack"), image_dur=6),
                       "particles/particles" : Animation(load_images("particles/particles"))
                    }
    
    def fetch(self):
        return self.assets