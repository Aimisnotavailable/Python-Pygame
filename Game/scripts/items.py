import os
from scripts.utils import Animation, load_images

BASE_IMG_PATH = 'data/images/'
class Weapon():
    def __init__(self, name, is_dropped=False):
        self.name = name
        self.atk = 1
        self.pos = (0, 0)
        weapon_path = f'items/weapons/swords/weapon_animation/{self.name}/'
        particle_path = f'items/weapons/swords/particle_animation/{self.name}/'
        self.w_animation = {atk_type : Animation(load_images(f"{weapon_path}{atk_type}"), image_dur=6) for atk_type in os.listdir(BASE_IMG_PATH + weapon_path)}
        self.p_animation =  {atk_type : Animation(load_images(f"{particle_path}{atk_type}"), image_dur=10) for atk_type in os.listdir(BASE_IMG_PATH + particle_path)}
        self.d_animation = Animation(load_images(f"items/weapons/swords/drop_animation/{self.name}"), image_dur=10)
        self.is_dropped = True
    
    def weapon_animation(self):
        return self.w_animation.copy()

    def particle_animation(self):
        return self.p_animation.copy()

    def drop_animation(self):
        return self.d_animation.copy()
    
    def set_drop_status(self, pos, is_dropped=False):
        if is_dropped:
            self.is_dropped = is_dropped
            self.d_animation_c = self.drop_animation()
            self.pos = pos
        else:
            self.is_dropped = is_dropped

    def render(self, surf, offset=(0,0)):
        if self.is_dropped:
            surf.blit(self.d_animation_c.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
            self.d_animation_c.update()
    