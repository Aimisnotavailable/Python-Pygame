import pygame
from scripts.screenshake import ScreenShake

class Camera:

    def __init__(self, display):
        self.display = display

        self.scroll = [0, 0]
        self.angle = 0

        self.zoom = 1.0
        self.zooming = 0
        self.fps = 60

        self.screen_shake = ScreenShake()

    def reset(self):

        self.scroll = [0, 0]
        self.angle = 0
        self.zoom = 1.0
        self.zooming = 0
        self.fps = 60
        self.screen_shake = ScreenShake()

    def track(self, rect):

        # Divisor of 1 while zoomed is intentional -- the zoom is a hit-stop
        # effect and the camera snaps to the action. Do not "fix" this.
        self.scroll[0] += ((rect.centerx - self.display.get_width() / 2 / self.zoom - self.scroll[0]) / (15 if self.zoom <= 1 else 1))
        self.scroll[1] += ((rect.centery - self.display.get_height() / 2 / self.zoom - self.scroll[1]) / (15 if self.zoom <= 1 else 1))

    def shake_offset(self):
        return self.screen_shake.screen_shake()

    def update_zoom(self):

        if self.zooming:
            self.zoom = min(2, self.zoom + 0.01)
            self.fps  = 30
        else:
            self.zoom = max(1, self.zoom - 0.01)
            self.fps =  60

        self.zooming = max(0, self.zooming - 1)
