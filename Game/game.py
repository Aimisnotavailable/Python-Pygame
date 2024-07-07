import pygame
import sys
import os
import random
import math
from scripts.utils import load_image, load_images, Animation
from scripts.tilemap import TileMap
from scripts.entities import PhysicsEntities, Player, Enemy
from scripts.items import Weapon, Sword, Gun
from scripts.inventory import Inventory
from scripts.clouds import Clouds
from scripts.sparks import Sparks
from scripts.particles import Particles
from water1 import Water

BASE_IMG_PATH = 'data/images/'

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Game")

        self.time = 0

        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((300, 200))

        self.clock = pygame.time.Clock()

        self.tilemap = TileMap(self)
        self.tilemap.load("data/maps/map.json")
        self.movement = [0, 0]

        self.scroll = [0, 0]
        self.assets = {"background" : load_image("background.png"),
                       "inventory_slot" : load_images("inventory/slot"),
                       "clouds" : load_image("clouds\cloud.png"),
                       "grass" : load_images("tiles/grass"),
                       "stone" : load_images("tiles/stone"),
                       "player" : load_image("entities/player/player.png"),
                       "player/idle" : Animation(load_images("entities/player/idle"), image_dur=10),
                       "player/jump" : Animation(load_images("entities/player/jump")),
                       "player/run" : Animation(load_images("entities/player/run"), image_dur=5),
                       #player/attack" : Animation(load_images("entities/player/attack"), image_dur=5),
                       "enemy" : load_image("entities/enemy/enemy.png"),
                       "enemy/idle" : Animation(load_images("entities/enemy/idle"), image_dur=7),
                       "enemy/damaged" : Animation(load_images("entities/enemy/damaged")),
                       "enemy/run" : Animation(load_images("entities/enemy/run"), image_dur=5),
                       "enemy/attack" : Animation(load_images("entities/enemy/attack"), image_dur=6),
                       "particles/particles" : Animation(load_images("particles/particles"))
                    }
        
        self.current_weapon = Sword(self, 'dirt_stick', color=(150, 75, 0))

        self.pos = (self.display.get_width()//2, self.display.get_height()//2)
        self.weapon_pos = self.pos

        self.player = Player(self, self.pos)
        self.enemies = []
        self.items_nearby = []
        self.attack_rect = None

        self.inventory = Inventory(self.assets['inventory_slot'])
        self.inventory.item_list[self.inventory.current_selected] = self.current_weapon
        self.inventory.item_list[1] = Sword(self,  'slime_stick', color=(10, 255, 10))

        self.clouds = Clouds(self.assets['clouds'], count=15)

        self.sparks = []
        self.projectiles = []

        self.water = Water()
        self.under_water = False

        # for loc in self.tilemap.tilemap:
        #     if random.randint(0, 20) == 1:
        #         self.enemies.append(Enemy(self, (self.tilemap.tilemap[loc]['pos'][0] * self.tilemap.tile_size, self.tilemap.tilemap[loc]['pos'][1] * self.tilemap.tile_size)))

    def run(self):
        running = True

        while running:
            self.display.fill((0,0,0,0))
            self.display_2.blit(self.assets['background'], (0, 0))
        
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.render(self.display_2, render_scroll)
            self.clouds.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = -2
                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 2
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                    
                    if event.key == pygame.K_1 and self.player.attacking == 0:
                        self.inventory.current_selected = 0
                        self.current_weapon = self.inventory.item_list[self.inventory.current_selected ]
                    
                    if event.key == pygame.K_2 and self.player.attacking == 0:
                        self.inventory.current_selected = 1
                        self.current_weapon = self.inventory.item_list[self.inventory.current_selected ]

                    if event.key == pygame.K_x and self.current_weapon is not None and self.current_weapon.type == 'swords' and self.player.attacking == 0:
                        self.player.start_charge(is_initialized=True)
                    
                    if event.key == pygame.K_c and self.current_weapon is not None and self.current_weapon.type == 'guns' and self.player.attacking == 0:
                        self.player.shooting = True
                        atk_type = 'shoot_attack'
                        self.player.perform_attack(atk_type, self.current_weapon)

                    if event.key == pygame.K_e and self.current_weapon is not None and self.player.attacking == 0:
                        self.current_weapon.set_drop_status(self.player.pos.copy(), is_dropped=True)
                        self.items_nearby.append(self.current_weapon)
                        self.inventory.remove_item()

                        self.current_weapon = None
                    
                    if event.key == pygame.K_r and self.current_weapon is not None and self.current_weapon.type == 'swords' and self.player.attacking == 0:
                        self.current_weapon.velocity[0] = -5 if self.player.flip else 5

                        self.inventory.remove_item()
                        self.current_weapon.set_drop_status(self.player.pos.copy(), is_dropped=False)
                        self.current_weapon.set_throw_status(self.player.pos.copy(), is_thrown=True)

                        self.items_nearby.append(self.current_weapon)
                        atk_type = 'throw_meele_attack'
                        self.player.perform_attack(atk_type, self.current_weapon)

                        self.current_weapon = None

                    if event.key == pygame.K_q:
                        for item in self.items_nearby:
                            if (item.pos[0] >= self.player.pos[0] - self.tilemap.tile_size and item.pos[0] <= self.player.pos[0] + self.tilemap.tile_size) and (item.pos[1] >= self.player.pos[1] - self.tilemap.tile_size and item.pos[1] <= self.player.pos[1] + self.tilemap.tile_size):
                                if self.current_weapon is not None:
                                    self.current_weapon.set_drop_status(self.player.pos.copy(), is_dropped=True)
                                    self.items_nearby.append(self.current_weapon)
                                item.animation = item.stash_animation()
                                self.inventory.item_list[self.inventory.current_selected] = item
                                self.current_weapon = item
                                self.items_nearby.remove(self.current_weapon)
                                break

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = 0

                    if event.key == pygame.K_RIGHT:
                        self.movement[0] = 0
                    
                    if event.key == pygame.K_x and self.current_weapon is not None and self.current_weapon.type == 'swords' and self.player.attacking == 0:
                        if event.key == pygame.K_x and self.player.attacking <= 0 and self.current_weapon is not None:
                            atk_type = 'normal_attack' if self.player.attack_type < self.player.charge_duration else 'charged_attack'
                            self.player.perform_attack(atk_type, self.current_weapon)
                    
                    if event.key == pygame.K_c and self.current_weapon is not None and self.current_weapon.type == 'guns':
                        self.player.shooting = False
            
            self.tilemap.render(self.display, offset=render_scroll)

            if self.player.shooting and self.player.attacking == 1:
                self.player.attacking = 10
                atk_type = 'shoot_attack'
                self.player.perform_attack(atk_type, self.current_weapon)

            for spark in self.sparks.copy():
                spark.render(self.display, render_scroll)
                if spark.update():
                    self.sparks.remove(spark)

            for projectile in self.projectiles.copy():
                projectile.render(self.display, render_scroll)
                if self.tilemap.solid_check(projectile.pos):
                    for i in range(4):
                        angle = (random.random() - 0.5) + (math.pi if projectile.speed > 0 else 0)
                        speed = (random.random() + 2)
                        self.sparks.append(Sparks(angle, speed, projectile.pos))
                    self.projectiles.remove(projectile)
                    
                    continue
                if projectile.update():
                    self.projectiles.remove(projectile)

                for enemy in self.enemies.copy():
                    if enemy.rect().collidepoint(projectile.pos):
                        self.projectiles.remove(projectile)
                        if enemy.attacked == 0:
                            enemy.current_hp -=1
                            enemy.attacked = 30
                            enemy.velocity[1] = -2
                            enemy.flip = not enemy.flip

                        if enemy.current_hp <= 0:
                            dropped_item = Sword(self, 'slime_stick', color=(255, 10, 10))
                            dropped_item.set_drop_status(enemy.pos,is_dropped=True)
                            self.items_nearby.append(dropped_item)
                            self.enemies.remove(enemy)
                            for i in range(30):
                                angle = (random.random() + 0.5) * math.pi * 2
                                speed = (random.random() + 0.5) + 1
                                self.sparks.append(Sparks(angle, speed, enemy.pos))
                        break

            self.player.update(self.tilemap, self.movement)
            self.player.render(self.display, offset=render_scroll)
            
            for i in range(len(self.water.springs)):
                if self.player.rect().collidepoint((self.water.springs[i].pos[0] + 160, self.water.springs[i].pos[1] + 96)) and not self.under_water:
                    self.water.wave(i)


                
            for item in self.items_nearby.copy():
                item.render(self.display, render_scroll)
                if item.life == 0:
                    self.items_nearby.remove(item)

            for enemy in self.enemies:
                enemy.update(self.tilemap)
                enemy.render(self.display, offset=render_scroll)
                pygame.draw.circle(self.display, (0, 0 if not self.tilemap.solid_check((enemy.rect().centerx + (-7 if enemy.flip else 7), enemy.pos[1] + 23)) else 255, 0), (enemy.rect().centerx + (-7 if enemy.flip else 7) - render_scroll[0], enemy.pos[1] + 23 - render_scroll[1]), 1)
            
            if self.player.attacking != 0 and self.player.atk_type != 'shoot_attack':
                for enemy in self.enemies.copy():
                    if enemy.rect().colliderect(self.attack_rect):
                        if enemy.attacked == 0:
                            enemy.current_hp -=1
                            enemy.attacked = 30
                            enemy.velocity[1] = -2
                            enemy.flip = not enemy.flip

                        if enemy.current_hp <= 0:
                            dropped_item = Sword(self, 'slime_stick')
                            dropped_item.set_drop_status(enemy.pos,is_dropped=True)
                            self.items_nearby.append(dropped_item)
                            self.enemies.remove(enemy)
                            for i in range(30):
                                angle = (random.random() + 0.5) * math.pi * 2
                                speed = (random.random() + 0.5) + 1
                                self.sparks.append(Sparks(angle, speed, enemy.pos))
                    
            self.inventory.render(self.display)
            
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))

            for offset in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
                self.display_2.blit(display_sillhouette, offset)

            self.display_2.blit(self.display, (0, 0))
            self.water.render(self.display_2, render_scroll)

            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)   
    
Game().run()