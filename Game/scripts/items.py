import os
import math
import random
from scripts.utils import Animation, load_images
from scripts.entities import PhysicsEntities
from scripts.sparks import Sparks

BASE_IMG_PATH = 'data/images/'

class Weapon(PhysicsEntities):
    def __init__(self, game, name, w_type, w_path, p_path, size=(16, 16), is_dropped=False):
        super().__init__(game, name, size=size)
        self.name = name
        self.type = w_type
        self.atk = 1
        self.is_dropped = False
        self.velocity = [0, 0]

        self.weapon_path = w_path
        self.particle_path = p_path

        self.d_animation = Animation(load_images(f"items/weapons/{w_type}/drop_animation/{self.name}"), image_dur=10)
        self.animation = self.d_animation.copy()
        self.w_animation = None
        self.p_animation = None
        self.life = 1000
    
    def set_drop_status(self, pos, is_dropped=False):
        if is_dropped:
            self.is_dropped = is_dropped
            self.animation = self.drop_animation()
            self.pos = pos
        else:
            self.life = 1000
            self.is_dropped = is_dropped
    
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

    def render(self, surf, offset=(0,0)):
        if self.is_dropped:
            self.life -= 1
            surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))   

class Sword(Weapon):
    def __init__(self, game, name, is_dropped=False):
        type = 'swords'
        w_path = f'items/weapons/{type}/weapon_animation/{name}/'
        p_path = f'items/weapons/{type}/particle_animation/{name}/'

        super().__init__(game, name, type ,w_path, p_path)
        self.atk = 1
        self.is_dropped = False
        self.velocity = [0, 0]

        self.w_animation = {atk_type : Animation(load_images(f"{self.weapon_path}{atk_type}"), image_dur=10, loop=False) for atk_type in os.listdir(BASE_IMG_PATH + self.weapon_path)}
        self.p_animation =  {atk_type : Animation(load_images(f"{self.particle_path}{atk_type}"), image_dur=10, loop=False) for atk_type in os.listdir(BASE_IMG_PATH + self.particle_path)}
        self.t_animation = Animation(load_images(f"items/weapons/swords/throw_animation/{self.name}"), image_dur=10)

        self.is_thrown =  False


    def throw_animation(self):
        return self.t_animation.copy()
    
    def set_throw_status(self, pos, is_thrown=False):
        if is_thrown:
            self.is_thrown = is_thrown
            self.animation = self.throw_animation()
            self.pos = pos
        else:
            self.is_thrown = is_thrown


    def update(self):
        super().update()
        if (self.velocity[0] == 0 or self.collisions['left'] or self.collisions['right']) and self.is_thrown :
            for i in range(4):
                angle = (random.random() - 0.5)  + (math.pi if self.velocity[0] > 0 else 0)
                speed = (random.random() + 0.5) * 2
                self.game.sparks.append(Sparks(angle, speed, self.rect().center))

            self.set_drop_status(self.pos, is_dropped=True)    
            self.set_throw_status(self.pos, is_thrown=False)
            self.game.player.attacking = 0
        
    def render(self, surf, offset=(0,0)):
        self.update()
        super().render(surf, offset)
        if self.is_thrown:
            surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
            self.game.attack_rect = self.rect()

class Gun(Weapon):

    def __init__(self, game, name, size=(15,9), is_dropped=False):
        type = 'guns'
        w_path = f'items/weapons/{type}/weapon_animation/{name}/'
        p_path = f'items/weapons/{type}/particle_animation/{name}/'

        super().__init__(game, name, type, w_path, p_path)
        self.w_animation = Animation(load_images(self.weapon_path), image_dur=10, loop=False)
        self.p_animation =  {atk_type : Animation(load_images(f"{self.particle_path}{atk_type}"), image_dur=10) for atk_type in os.listdir(BASE_IMG_PATH + self.particle_path)}
        self.animation = self.w_animation.copy()
        self.pos = [0,0]
        
    def update(self):
        super().update()

    def render(self, surf, offset):
        self.update()
        surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
