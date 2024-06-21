class Projectiles:

    def __init__(self, img, speed, life, pos=(0, 0)):
        self.img = img
        self.speed = speed
        self.pos = list(pos)
        self.life = life

    def update(self):
        self.pos[0] += self.speed
        self.life -=1

        return not self.life

    def render(self, surf, offset):
        surf.blit(self.img, (self.pos[0] - offset[0], self.pos[1] - offset[1]))