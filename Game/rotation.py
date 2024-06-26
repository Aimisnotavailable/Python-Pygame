import pygame
import math
import sys
from scripts.utils import load_image

QUADRANTS = {(1, 0) : 0,
             (0, 0) : 180,
             (0, 1) : 180,
             (1, 1) : 360
             }

class Rotation:

    def run(self):
        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))
        self.img = load_image('items/weapons/guns/weapon_animation/dirt_gun/0.png')
        pygame.init()

        self.clock = pygame.time.Clock()
        angle = 0
        midpoint = (150, 100)
        mpos = (400, 372)
        self.flip_x = 0
        self.flip_y = 0
        original_size = self.img.get_size()
        while True:
            self.display.fill((100, 0, 100))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0]//2 , mpos[1]//2)
            
            self.flip_x = 1 if mpos[0] > midpoint[0] else 0
            self.flip_y = 1 if mpos[1] > midpoint[1] else 0

            quad = (self.flip_x, self.flip_y)

            angle = (-1 * math.atan((mpos[1] - midpoint[1]) / (mpos[0] - midpoint[0]) if (mpos[0] - midpoint[0]) != 0 else 1 ) * (180 / math.pi)) + QUADRANTS[quad]

            img = pygame.transform.rotate(self.img , angle)

            pygame.draw.line(self.display, (255, 255, 255), midpoint, (mpos[0], mpos[1]))
            new_size = img.get_size()
            offset = (original_size[0] - new_size[0] ,  original_size[1] - new_size[1])
            print(offset)
            self.display.blit(img, (midpoint[0] + offset[0], midpoint[1] + offset[1]))

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Rotation().run()