import os
import math
import random
from scripts.utils import Animation, load_images
from scripts.entities import PhysicsEntities
from scripts.sparks import Sparks
from scripts.sfx import SoundMixer

BASE_IMG_PATH = 'data/images/'

class Weapon(PhysicsEntities):
    def __init__(self, game, name, w_type, w_path, p_path, size=(16, 16), is_dropped=False, color=(255, 255, 255)):
        super().__init__(game, name, size=size)
        self.name = name
        self.type = w_type
        self.atk = 1
        self.is_dropped = False
        self.sound = SoundMixer(payload={'weapon' : [self.type]})
        self.color = color
        self.weapon_path = w_path
        self.particle_path = p_path

        self.d_animation = Animation(load_images(f"items/weapons/{w_type}/drop_animation/{self.name}", scale=[16, 8]), image_dur=10)
        self.animation = self.d_animation.copy()
        self.w_animation = None
        self.p_animation = None
        self.life = 1000
        self.attack_cooldowns = {'normal_attack' : 30, 'charged_attack' : 30, 'throw_meele_attack' : 50, 'shoot_attack' : 15, 'splash_attack' : 60}
    
    def set_drop_status(self, pos, is_dropped=False):
        if is_dropped:
            self.is_dropped = is_dropped
            self.animation = self.drop_animation()
        else:
            self.life = 1000
            self.is_dropped = is_dropped
        self.pos = pos
        
    def drop_animation(self):
        return self.d_animation.copy()
    
    def stash_animation(self):
        return self.d_animation.copy()
    
    def weapon_animation(self):
        return self.w_animation.copy()
    
    def particle_animation(self):
        return self.p_animation.copy()

    def update(self):
        super().update(self.game.tilemap)

    def play_sound(self, variant=0, vol=1.0):
        self.sound.play(self.type, variant=variant, loop=0, vol=vol)

    def render(self, surf, offset=(0,0)):
        if self.is_dropped:
            self.life -= 1
            surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))


class Sword(Weapon):
    def __init__(self, game, name, size=(15,9), is_dropped=False, color=(255, 255, 255)):
        type = 'swords'
        w_path = f'items/weapons/{type}/weapon_animation/{name}/'
        p_path = f'items/weapons/{type}/particle_animation/{name}/'

        super().__init__(game, name, type ,w_path, p_path, size=size, color=color)
        self.atk = 1
        self.is_dropped = False
        self.velocity = [0, 0]

        self.w_animation = {atk_type : Animation(load_images(f"{self.weapon_path}{atk_type}", scale=size), image_dur=10, loop=False) for atk_type in os.listdir(BASE_IMG_PATH + self.weapon_path)}
        self.p_animation =  {atk_type : Animation(load_images(f"{self.particle_path}{atk_type}"), image_dur=10, loop=False) for atk_type in os.listdir(BASE_IMG_PATH + self.particle_path)}
        # self.t_animation = Animation(load_images(f"items/weapons/swords/throw_animation/{self.name}"), image_dur=10)

    def render(self, surf, offset=(0,0)):
        self.update()
        super().render(surf, offset)

class Gun(Weapon):

    def __init__(self, game, name, size=(15,9), is_dropped=False):
        type = 'guns'
        w_path = f'items/weapons/{type}/weapon_animation/{name}/'
        p_path = f'items/weapons/{type}/particle_animation/{name}/'

        super().__init__(game, name, type, w_path, p_path, size=size)
        self.w_animation = Animation(load_images(self.weapon_path, scale=size), image_dur=10, loop=False)
        self.p_animation =  {atk_type : Animation(load_images(f"{self.particle_path}{atk_type}"), image_dur=10) for atk_type in os.listdir(BASE_IMG_PATH + self.particle_path)}
        self.animation = self.w_animation.copy()
        self.pos = [0,0]
        
    def update(self):
        super().update()

    def render(self, surf, offset=(0, 0)):
        self.update()
        super().render(surf, offset)
