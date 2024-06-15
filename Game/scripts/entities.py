import pygame
import random

class PhysicsEntities:

    def __init__(self, game, e_type, pos, size):

        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {'up' : False, 'down' : False, 'right' : False, 'left' : False}

        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        self.air_time = 0

        self.last_movement = [0, 0]

    def set_action(self, action, weapon_name='dirt_stick'):
        if action != self.action:
            self.action = action
            if action != "attack":
                self.animation = self.game.assets[self.type + '/' + self.action].copy()
            else:
                self.weapon_animation = self.game.assets['weapon'][weapon_name].weapon_animation()
                self.weapon_particle_animation = self.game.assets['weapon'][weapon_name].particle_animation()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
    
    def render(self, surf, offset=(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0], self.pos[1] - offset[1]))

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
        elif self.velocity[1] < 0:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

        self.animation.update()

class Enemy(PhysicsEntities):
    def __init__(self, game, pos, size=(16,16)):
        super().__init__(game, 'enemy', pos, size)
    
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

    def __init__(self, game, pos, size=(16,16)):
        super().__init__(game,'player', pos, size)
        self.attacking = 0

    def update(self, tilemap, movement=(0,0)):
        super().update(tilemap, movement)

        self.air_time += 1
        self.attacking -= 1
        if self.collisions['down']:
            self.air_time = 0
        if self.attacking > 0:
            self.set_action('attack', self.game.current_weapon.name)
            self.weapon_particle_animation.update()
            self.weapon_animation.update()
        elif self.air_time > 4:
            self.set_action('jump')
            # if self.air_time > 60:
            #     self.pos = [self.game.display.get_width() // 2, self.game.display.get_height() // 2]
            #     self.air_time = 0
        elif self.movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

    def render(self, surf, offset=(0,0)):
        super().render(surf, offset)
        if(self.action == "attack"):
            slash_x = self.pos[0] - offset[0] + (-20 if self.flip else 20)
            slash_y = self.pos[1] - offset[1] - 5

            self.slash_rect = pygame.Rect(slash_x + offset[0], slash_y + offset[1], 8, 16)
            surf.blit(pygame.transform.flip(self.weapon_particle_animation.img(), self.flip, False), (slash_x, slash_y))
            surf.blit(pygame.transform.flip(self.weapon_animation.img(), self.flip, False), (self.pos[0] - offset[0] + (-10 if self.flip else 10), self.pos[1] - offset[1] - 5))
    
