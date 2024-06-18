import os
from scripts.utils import Animation, load_images
from scripts.entities import PhysicsEntities

BASE_IMG_PATH = 'data/images/'
class Weapon(PhysicsEntities):
    def __init__(self,name, game, is_dropped=False):
        super().__init__(game, name)
        self.name = name
        self.atk = 1

        weapon_path = f'items/weapons/swords/weapon_animation/{self.name}/'
        particle_path = f'items/weapons/swords/particle_animation/{self.name}/'
        self.w_animation = {atk_type : Animation(load_images(f"{weapon_path}{atk_type}"), image_dur=10, loop=False) for atk_type in os.listdir(BASE_IMG_PATH + weapon_path)}
        self.p_animation =  {atk_type : Animation(load_images(f"{particle_path}{atk_type}"), image_dur=10, loop=False) for atk_type in os.listdir(BASE_IMG_PATH + particle_path)}
        self.t_animation = Animation(load_images(f"items/weapons/swords/throw_animation/{self.name}"), image_dur=10)
        self.d_animation = Animation(load_images(f"items/weapons/swords/drop_animation/{self.name}"), image_dur=10)
        
        self.is_dropped = False
        self.is_thrown =  False

        self.velocity = [0, 0]

    def weapon_animation(self):
        return self.w_animation.copy()

    def particle_animation(self):
        return self.p_animation.copy()

    def drop_animation(self):
        return self.d_animation.copy()

    def throw_animation(self):
        return self.t_animation.copy()
    
    def set_drop_status(self, pos, is_dropped=False):
        if is_dropped:
            self.is_dropped = is_dropped
            self.animation = self.drop_animation()
            self.pos = pos
        else:
            self.is_dropped = is_dropped
    
    def set_throw_status(self, pos, is_thrown=False):
        if is_thrown:
            self.is_thrown = is_thrown
            self.animation = self.throw_animation()
            self.pos = pos
        else:
            self.is_thrown = is_thrown

    def update(self):
        super().update(self.game.tilemap)

        if (self.velocity[0] == 0 or self.collisions['left'] or self.collisions['right']) and self.is_thrown :
            self.set_drop_status(self.pos, is_dropped=True)    
            self.set_throw_status(self.pos, is_thrown=False)
            self.game.player.attacking = 0
        

    def render(self, surf, offset=(0,0)):
        self.update()
        if self.is_dropped:
            surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        if self.is_thrown:
            surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
            self.game.attack_rect = self.rect()
    