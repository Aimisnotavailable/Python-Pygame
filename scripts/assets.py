import pygame
from scripts.utils import load_image, load_images, load_sound, load_sounds, Animation

class LazyAssets(dict):
    """Dict that loads an asset the first time it is read.

    Consumers keep using plain subscription -- assets['grass'] -- and nothing
    is read from disk until that line actually runs.
    """

    def __init__(self):
        dict.__init__(self)
        self.thunks = {}

    def add(self, key, thunk):
        self.thunks[key] = thunk

    def __missing__(self, key):
        if key not in self.thunks:
            raise KeyError(key)

        value = self.thunks[key]()
        self[key] = value

        return value

    def load_all(self):
        for key in list(self.thunks):
            self[key] = self.thunks[key]()

    def merge(self, thunks):
        for key in thunks:
            if key in self.thunks:
                raise KeyError(f"Duplicate asset key '{key}' in registry")
            self.add(key, thunks[key])

        return self


class Assets:

    def __init__(self):

        water = []
        water.append(pygame.Surface((16, 16), pygame.SRCALPHA))
        water[0].fill((0, 0, 255, 100))

        # Every leaf is a thunk -- the load happens on first read, not here.
        self.assets = {

            'img' : {
                      "background" : { "background" : lambda: load_images("backgrounds", scale=[450, 300]),
                                        "clouds" : lambda: load_images("clouds")
                                      },
                      "tooltips"   : { "cursor" : lambda: Animation(load_images("cursor"), image_dur=7),
                                        "inventory_slot" : lambda: load_images("inventory/slot")
                                      },

                      "blocks"     : { "grass"  : lambda: load_images("tiles/grass"),
                                        "stone"  : lambda: load_images("tiles/stone"),
                                        "sand"   : lambda: load_images("tiles/sand"),
                                        "water"  : lambda: water
                                      },

                      "decors"     :{ "tree"    : lambda: load_images("decors")
                                    },

                      "spawners"    : { "entity_spawner" : lambda: load_images("spawners")
                                      },

                      "entity_animation" : {
                                      "player/idle" : lambda: Animation(load_images("entities/player/idle"), image_dur=10),
                                      "player/jump" : lambda: Animation(load_images("entities/player/jump")),
                                      "player/run"  : lambda: Animation(load_images("entities/player/run"), image_dur=5),
                                      "player/fade" : lambda: Animation(load_images("entities/player/fade"), image_dur=3),
                                      "player/wall_slide" : lambda: Animation(load_images("entities/player/wall_slide/")),

                                      "enemy/idle" : lambda: Animation(load_images("entities/enemy/idle"), image_dur=7),
                                      "enemy/damaged" : lambda: Animation(load_images("entities/enemy/damaged")),
                                      "enemy/run" : lambda: Animation(load_images("entities/enemy/run"), image_dur=5),
                                      "enemy/attack" : lambda: Animation(load_images("entities/enemy/attack"), image_dur=6),
                                      "enemy/hat" : lambda: Animation(load_images("entities/enemy/hat"), image_dur=6),
                                  },

                      "particles" : { "particles/particles" : lambda: Animation(load_images("particles/particles")),
                                      "particles/dust" : lambda: Animation(load_images("particles/dust"), image_dur=2, loop=False),
                                      "particles/leaf" : lambda: Animation(load_images("particles/leaf"), image_dur=15, loop=False),
                                      "particles/snow" : lambda: Animation(load_images("particles/snow"), image_dur=15, loop=True),
                                    },
                      "christmas" : {
                                      "christmas/santa" : lambda: Animation(load_images("santa"), image_dur=5),
                      }
            },

            "sfx" : {
                      "background": {
                          "background_music" : lambda: load_sounds('music'),
                      },

                      "player" : {
                          "teleport" : lambda: load_sounds('sfx/entity_sfx/player/teleport')
                      },

                      "weapon" : {
                          "guns" : lambda: load_sounds('sfx/gun_sfx'),
                          "swords" : lambda: load_sounds('sfx/sword_sfx')
                      },

                      "tile" : {
                          'grass' : lambda: load_sounds('sfx/tile_sfx/grass'),
                          'sand'  : lambda: load_sounds('sfx/tile_sfx/sand'),
                          'stone' : lambda: load_sounds('sfx/tile_sfx/stone'),
                      },
                      },
            }

    def fetch(self, payload={}, fetch_all=False):
        return fetch(payload, fetch_all)


_registry = None

def get_registry():
    """One shared thunk registry. Building it costs nothing now that the
    leaves are callables, so every consumer can share the same table."""

    global _registry

    if _registry is None:
        _registry = Assets().assets

    return _registry


def fetch(payload={}, fetch_all=False):
    """Flattens the registry into a single lazily-resolved namespace."""

    registry = get_registry()
    assets = LazyAssets()

    if fetch_all:
        for file_type in registry:
            for obj_type in registry[file_type]:
                assets.merge(registry[file_type][obj_type])
        return assets

    for file_type in payload:
        if 'all' in payload[file_type]:
            for obj_type in registry[file_type]:
                assets.merge(registry[file_type][obj_type])
        else:
            for obj_type in payload[file_type]:
                assets.merge(registry[file_type][obj_type])

    return assets
