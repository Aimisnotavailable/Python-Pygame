import math

class Effects:

    def __init__(self):

        self.projectiles = []
        self.sparks = []
        self.particles = []

    def render(self, surf, offset=(0, 0)):

        for particle in self.particles.copy():
            particle.pos[0] += math.cos(particle.angle) * (math.sin(particle.animation.frame)*-1)
            if particle.render(surf, offset):
                self.particles.remove(particle)

        for spark in self.sparks.copy():
            spark.render(surf, offset)
            if spark.update():
                self.sparks.remove(spark)
