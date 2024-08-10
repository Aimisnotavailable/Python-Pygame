import math
import random

class ScreenShake:
    def __init__(self):
        self.dur = 0
        self.magnitude = 0

    def set_shake_config(self, strength=5, dur=60):
        self.dur = dur
        self.magnitude = strength

    def screen_shake(self):
        shake_offset = [math.sin((random.random() - 0.5) * math.pi * 2 ) * self.magnitude , math.sin((random.random() - 0.5) * math.pi * 2)  * self.magnitude + 2]
        self.dur = max(0, self.dur - 1)
        return shake_offset