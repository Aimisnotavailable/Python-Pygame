import pygame
import os

BASE_IMG_PATH = 'data/images/'
BASE_SFX_PATH = 'data/sounds/'

def load_image(path, scale=[]):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))

    if scale:
        img = pygame.transform.scale(img, scale)

    return img

def load_images(path, scale=[]):
    images = []

    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, scale=scale))
    return images

def load_sound(path):
    sound = pygame.mixer.Sound(BASE_SFX_PATH + path)
    return sound

def load_sounds(path):
    sounds = []
    
    for sound_name in sorted(os.listdir(BASE_SFX_PATH + path)):
        sounds.append(load_sound(path + '/' + sound_name))
    
    return sounds

class Animation:

    def __init__(self, images, image_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.image_duration = image_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.image_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, (self.image_duration * len(self.images)- 1))
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.image_duration)]
    
class Background:

    def __init__(self, imgs=[]):
        
        self.render_offset = [[0, 0] for i in range(len(imgs))]
        self.pos = [[0, 0] for i in range(len(imgs))]
        self.imgs = imgs
    
    def render(self, surf):
        for i in range(len(self.imgs)):

            self.render_offset[i][0] += (self.pos[i][0] - 0 - self.render_offset[i][0])
            self.render_offset[i][1] += (self.pos[i][1] - 0 - self.render_offset[i][1])

            damp_offset = [self.render_offset[i-1][0] if i > 0 else 0 , self.render_offset[i-1][1] if i > 0 else 0]
            surf.blit(self.imgs[i], (self.pos[i][0] - (self.render_offset[i][0] + damp_offset[0] * 0.5), self.pos[i][1] - (self.render_offset[i][1] + damp_offset[1] * 0.5)))   
