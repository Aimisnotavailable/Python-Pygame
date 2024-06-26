import pygame
import random
import math
from scripts.sparks import Sparks
from scripts.particles import Particles
from scripts.projectiles import Projectiles

class PhysicsEntities:

    def __init__(self, game, e_type, pos=(0,0), size=(16,16)):
        
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up' : False, 'down' : False, 'right' : False, 'left' : False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.air_time = 0

        self.last_movement = [0, 0]

        self.objects = []
        self.attacking = 0

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def perform_attack(self, atk_type, current_weapon):
        #if(self.air_time < 4):
        self.attacking = self.attack_cooldowns[atk_type]
        self.current_weapon = current_weapon
        self.atk_type = atk_type
        self.initialize_weapon(atk_type, current_weapon)
        #self.set_action('attack')
        #else:
           # self.set_action('jump')

    def initialize_weapon(self, atk_type, current_weapon):
        if atk_type == "normal_attack" or atk_type == "charged_attack":
            self.objects.append({'img': current_weapon.particle_animation()[atk_type].copy(), 'pos' : self.pos, 'type' : 'attack_radius'})
            self.objects.append({'img' : current_weapon.weapon_animation()[atk_type].copy(), 'pos' : self.pos, 'type' : 'weapon'})
        elif atk_type == "throw_meele_attack":
            return
        elif atk_type == "shoot_attack":
            self.objects.append({'img' : current_weapon.weapon_animation().copy(), 'pos' : (self.rect().centerx + (-7 if self.flip else -3), self.rect().centery), 'type' : 'weapon'})
            self.game.projectiles.append(Projectiles(current_weapon.particle_animation()[atk_type].copy().img(), speed=(-5 if self.flip else 5), life=1000, pos=self.rect().center))
    
    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def render(self, surf, offset=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))

    def update(self, tilemap, movement=(0,0)):
        self.movement = movement
        self.collisions = {'up' : False, 'down' : False, 'right' : False, 'left' : False}
        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.tiles_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x

        self.pos[1] += frame_movement[1]
        entity_rect = self.rect()
        for rect in tilemap.tiles_rect_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True

                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True
        
        self.velocity[1] = min(5, self.velocity[1] + 0.1)
        if self.collisions['up'] or self.collisions['down']:
            self.velocity[1] = 0
        
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        elif self.velocity[0] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        self.animation.update()

class Enemy(PhysicsEntities):
    def __init__(self, game, pos, size=(16,15)):
        super().__init__(game, 'enemy', pos, size)
        self.set_action('idle')
        self.walking = 0
        self.current_hp = 5
        self.max_hp = 5
        self.attacked =0

    def update(self, tilemap, movement=(0,0)):
        if self.walking and self.action != 'damaged':
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):
                if(self.collisions['right'] or self.collisions['left']):
                    self.flip = not self.flip
                movement = (movement[0] + (-0.5 if self.flip else 0.5), movement[1])
            else:
                self.flip = not self.flip
                self.velocity[0] = 0
            self.walking = max(0, self.walking - 1)
        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)
        
        self.attacked -= 1

        if self.attacked <= 0:
            self.attacked = 0

        if self.attacked > 0:
            self.set_action('damaged')
            movement = (movement[0] + (-0.3 if self.flip else 0.3), movement[1])
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')
        
        super().update(tilemap, movement)
    
    def render(self, surf, offset=(0,0)):
        super().render(surf, offset)
        pygame.draw.rect(surf, (0, 255, 0), pygame.Rect(self.pos[0] - offset[0] + (5 * (self.max_hp - self.current_hp)), self.pos[1] - offset[1], 5 * self.current_hp, 5))
        pygame.draw.rect(surf, (255, 0, 0), pygame.Rect(self.pos[0] - offset[0], self.pos[1] - offset[1], 5 * (self.max_hp - self.current_hp), 5))

class Player(PhysicsEntities):

    def __init__(self, game, pos, size=(8, 16)):
        super().__init__(game,'player', pos, size)
        self.attack_cooldowns = {'normal_attack' : 30, 'charged_attack' : 30, 'throw_meele_attack' : 50, 'shoot_attack' : 10}
        self.set_action('idle')

        self.attack_type = 0
        self.atk_type = ''

        self.is_initialized = False
        self.charge_duration = 30

        self.dashing = 0
        self.dash_duration = 10
        self.dash_multiplier = 1

        self.atk_type_count_meele = 2
        self.shooting = False

    def start_charge(self, is_initialized=False):
        self.is_initialized = is_initialized
    
    def dash(self):
        if self.dashing >= 1:
            self.velocity[0] = -8  if self.flip else 8
            if self.dashing == 1 or self.dashing == int((self.dash_duration * self.dash_multiplier)):
                for i in range(30):
                    angle = (random.random() + 0.5) * math.pi * 2
                    speed = (random.random() + 0.5) * 2
                    self.game.sparks.append(Sparks(angle, speed, self.rect().center, self.current_weapon.color))
                
            else:
                for i in range(4):
                    angle = (random.random() - 0.5) * math.pi * 0.5 + (math.pi if not self.flip else 0)
                    speed = (random.random() + 0.5) * 2
                    self.game.sparks.append(Sparks(angle, speed, self.rect().center, self.current_weapon.color))

            self.dashing -= 1
        return self.dashing

    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement)

        self.air_time += 1
        self.attack_type = min(self.attack_type + 1, self.charge_duration * self.atk_type_count_meele - 1)
        self.attacking = max(0, self.attacking - 1)
        
        if not self.is_initialized:
            self.attack_type = 0
        if self.collisions['down']:
            self.air_time = 0

        if self.attacking > 0:
            if self.attacking == 1:
                self.start_charge(is_initialized=False)
                self.set_action('idle')

            if self.atk_type == "charged_attack":
                if self.attacking == 29:
                    self.dashing = int(self.dash_duration * (1 + ((self.attack_type - self.charge_duration) / self.charge_duration) * 0.5))
                    self.attack_type = 0
                if self.dashing:
                    self.dash()
                else:
                    self.velocity[0] = 0
        elif self.air_time > 4:
            self.set_action('jump')
        elif self.movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0,0)):
        # Charge tooltip
        if self.is_initialized and self.attacking == 0:
            pygame.draw.rect(surf, (255, 0, 0) if self.attack_type < self.charge_duration else (0, 255, 0) if self.attack_type < self.charge_duration * self.atk_type_count_meele - 1 else (0, 0, 255), pygame.Rect(self.pos[0] - offset[0] - (self.charge_duration * self.atk_type_count_meele - 1 - self.attack_type) //5, self.pos[1] - offset[1] - 10, self.attack_type //5, 3))

        if(self.attacking != 0):
            for object in self.objects:
                if self.dashing <= 0:
                    surf.blit(pygame.transform.flip(object['img'].img(), self.flip, False), (object['pos'][0] - offset[0] + (-10 if self.flip else 10), object['pos'][1] - offset[1] - 5))
                if (object['type'] == 'attack_radius'):
                    self.game.attack_rect = pygame.Rect(object['pos'][0] + (-10 if self.flip else 10), object['pos'][1], 16, 16)
                object['img'].update()
                if object['img'].done:
                    self.objects.remove(object)
        if not self.dashing:
            super().render(surf, offset)