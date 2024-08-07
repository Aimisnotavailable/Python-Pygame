class WaterSpring:

    def __init__(self, pos, velocity=(0,0)):
        self.resting_length = 0

        self.pos = list(pos)
        self.velocity = list(velocity)
        self.damping = 0.95
        self.gravity = 0.8
        
        self.spring_const = 0.1
        self.displacement = 0
        self.total_force = 0
        self.force = 0
        
    def update(self):
        
        self.displacement = self.pos[1] - self.resting_length

        spring_force = -self.spring_const * self.displacement 
        
        self.total_force = spring_force + self.gravity + self.force

        self.velocity[1] = self.velocity[1] * self.damping + self.total_force

        self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]

        self.force = 0