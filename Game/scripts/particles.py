import math

class Particles:

    def __init__(self, game, type, angle, speed, pos=(0, 0)):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed
        self.animation = game.assets['particles' + '/' + type]

    def update(self):
        
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)

        return not self.speed

    def render(self, surf, offset=(0, 0)):
        surf.blit(self.animation.img(), (self.pos[0] - offset[0], self.pos[1] - offset[1]))
        self.animation.update()