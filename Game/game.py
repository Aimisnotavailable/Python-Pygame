import pygame
import sys
import os
import random
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import TileMap
from scripts.entities import PhysicsEntities, Player, Enemy
from scripts.items import Weapon

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Game")

        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200))

        self.clock = pygame.time.Clock()

        self.movement = [0, 0]

        self.scroll = [0, 0]
        self.weapons = [Weapon('dirt_stick'), Weapon('slime_stick')]
        self.assets = {"grass" : load_images("tiles/grass"),
                       "player" : load_image("entities/player/player1.png"),
                       "player/idle" : Animation(load_images("entities/player/idle"), image_dur=10),
                       "player/jump" : Animation(load_images("entities/player/jump")),
                       "player/run" : Animation(load_images("entities/player/run"), image_dur=5),
                       "enemy" : load_image("entities/enemy/enemy.png"),
                       "enemy/idle" : Animation(load_images("entities/enemy/idle"), image_dur=7),
                       "enemy/damaged" : Animation(load_images("entities/enemy/damaged")),
                       "enemy/run" : Animation(load_images("entities/enemy/run"), image_dur=5),
                       "weapon" :{"dirt_stick" : self.weapons[0], "slime_stick": self.weapons[1]}
                    }
        
        self.current_weapon = self.weapons[0]
        self.tilemap = TileMap(self)
        self.tilemap.load("data/maps/map.json")

        self.pos = (self.display.get_width()//2, self.display.get_height()//2)
        self.weapon_pos = self.pos
        self.d_anim = self.assets['weapon']['dirt_stick'].drop_animation()

        self.player = Player(self, self.pos)
        self.enemies = [Enemy(self, self.pos)]
        self.items_nearby = []
        for loc in self.tilemap.tilemap:
            if random.randint(0, 5) == 1:
                self.enemies.append(Enemy(self, (self.tilemap.tilemap[loc]['pos'][0] * self.tilemap.tile_size, self.tilemap.tilemap[loc]['pos'][1] * self.tilemap.tile_size)))

    def run(self):
        running = True

        while running:

            self.display.fill((135, 206, 235))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = -1
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 1
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                    
                    if event.key == pygame.K_x and self.player.attacking == 0:
                        self.player.set_attack(is_initialized=True)
                    
                    if event.key == pygame.K_g and self.current_weapon is not None and self.player.attacking == 0:
                        self.current_weapon.set_drop_status(self.player.pos.copy(), is_dropped=True)
                        self.items_nearby.append(self.current_weapon)
                        self.current_weapon = None
                    
                    if event.key == pygame.K_p:
                        for item in self.items_nearby:
                            if (item.pos[0] >= self.player.pos[0] - self.tilemap.tile_size and item.pos[0] <= self.player.pos[0] + self.tilemap.tile_size) and (item.pos[1] >= self.player.pos[1] - self.tilemap.tile_size and item.pos[1] <= self.player.pos[1] + self.tilemap.tile_size):
                                if self.current_weapon is not None:
                                    self.current_weapon.set_drop_status(self.player.pos.copy(), is_dropped=True)
                                    self.items_nearby.append(self.current_weapon)
                                self.current_weapon = item
                                self.items_nearby.remove(self.current_weapon)
                                break

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0

                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 0
                    
                    if event.key == pygame.K_x and self.player.attacking == 0:
                        if event.key == pygame.K_x and self.player.attacking <= 0 and self.current_weapon is not None:
                            self.player.attacking = 30
                            self.player.atk_type = self.player.atk_list[int(self.player.attack_type//self.player.charge_duration)]
                            self.player.set_action('attack', self.current_weapon.name, atk_type=self.player.atk_type)

            self.tilemap.render(self.display, offset=render_scroll)
            self.player.update(self.tilemap, self.movement)
            self.player.render(self.display, offset=render_scroll)

            for enemy in self.enemies:
                enemy.update(self.tilemap)
                enemy.render(self.display, offset=render_scroll)
                pygame.draw.circle(self.display, (0, 0 if not self.tilemap.solid_check((enemy.rect().centerx + (-7 if enemy.flip else 7), enemy.pos[1] + 23)) else 255, 0), (enemy.rect().centerx + (-7 if enemy.flip else 7) - render_scroll[0], enemy.pos[1] + 23 - render_scroll[1]), 1)

            if self.player.action == "attack":
                for enemy in self.enemies:
                    if enemy.rect().colliderect(self.player.slash_rect):
                        if enemy.attacked == 0:
                            enemy.current_hp -=1
                            enemy.attacked = 30
                            enemy.velocity[1] = -2
                            enemy.flip = not enemy.flip
                            
                        if enemy.current_hp <= 0:
                            dropped_item = Weapon('slime_stick')
                            dropped_item.set_drop_status(enemy.pos,is_dropped=True)
                            self.items_nearby.append(dropped_item)
                            self.enemies.remove(enemy)
            for item in self.items_nearby:
                item.render(self.display, render_scroll)
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)   
    
Game().run()