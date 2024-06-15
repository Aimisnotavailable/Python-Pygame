from scripts.utils import Animation, load_images

class Weapon():
    def __init__(self, name, is_dropped=False):
        self.name = name
        self.atk = 1
        self.pos = (0, 0)
        self.w_animation = Animation(load_images(f"items/weapons/swords/weapon_animation/{self.name}"), image_dur=6)
        self.p_animation =  Animation(load_images(f"items/weapons/swords/particle_animation/{self.name}"), image_dur=10)
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
    