import math
class Projectiles:

    def __init__(self, img, speed, angle, life, pos=(0, 0)):
        self.img = img
        self.speed = speed
        self.pos = list(pos)
        self.angle = angle
        self.life = life

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed
        self.life -=1

        return not self.life

    def render(self, surf, offset):
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))