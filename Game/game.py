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
        self.weapons = [Sword('dirt_stick', self), Sword('slime_stick', self)]

        self.assets = {"background" : load_image("background.png"),
                       "inventory_slot" : load_images("inventory/slot"),
                       "clouds" : load_image("clouds\cloud.png"),
                       "grass" : load_images("tiles/grass"),
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

        self.pos = (self.display.get_width()//2, self.display.get_height()//2)
        self.weapon_pos = self.pos
        self.d_anim = self.assets['weapon']['dirt_stick'].drop_animation()

        self.player = Player(self, self.pos)
        self.enemies = [Enemy(self, self.pos)]
        self.items_nearby = []
        self.attack_rect = None

        self.inventory = Inventory(self.assets['inventory_slot'])
        self.inventory.item_list[self.inventory.current_selected] = self.current_weapon
        self.clouds = Clouds(self.assets['clouds'], count=30)

        self.gun = Gun(self, 'dirt_gun')
        self.sparks = []

        for loc in self.tilemap.tilemap:
            if random.randint(0, 20) == 1:
                self.enemies.append(Enemy(self, (self.tilemap.tilemap[loc]['pos'][0] * self.tilemap.tile_size, self.tilemap.tilemap[loc]['pos'][1] * self.tilemap.tile_size)))

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

                    if event.key == pygame.K_x and self.current_weapon is not None and self.player.attacking == 0:
                        self.player.set_attack(is_initialized=True)
                    
                    if event.key == pygame.K_e and self.current_weapon is not None and self.player.attacking == 0:
                        self.current_weapon.set_drop_status(self.player.pos.copy(), is_dropped=True)
                        self.items_nearby.append(self.current_weapon)
                        self.inventory.remove_item()

                        self.current_weapon = None
                    
                    if event.key == pygame.K_r and self.current_weapon is not None and self.player.attacking == 0:
                        self.current_weapon.velocity[0] = -5 if self.player.flip else 5

                        self.inventory.remove_item()
                        self.current_weapon.set_drop_status(self.player.pos.copy(), is_dropped=False)
                        self.current_weapon.set_throw_status(self.player.pos.copy(), is_thrown=True)

                        self.items_nearby.append(self.current_weapon)
                        self.player.set_action('throw', self.current_weapon)

                        self.player.attacking = 50
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
                    
                    if event.key == pygame.K_x and self.current_weapon is not None and self.player.attacking == 0:
                        if event.key == pygame.K_x and self.player.attacking <= 0 and self.current_weapon is not None:
                            self.player.attacking = 30
                            self.player.atk_type = self.player.atk_list[int(self.player.attack_type//self.player.charge_duration)]
                            self.player.set_action('attack', self.current_weapon.name)
            
            self.tilemap.render(self.display, offset=render_scroll)

            for spark in self.sparks.copy():
                spark.render(self.display, render_scroll)
                if spark.update():
                    self.sparks.remove(spark)

            self.player.update(self.tilemap, self.movement)
            self.player.render(self.display, offset=render_scroll)

            for enemy in self.enemies:
                enemy.update(self.tilemap)
                enemy.render(self.display, offset=render_scroll)
                pygame.draw.circle(self.display, (0, 0 if not self.tilemap.solid_check((enemy.rect().centerx + (-7 if enemy.flip else 7), enemy.pos[1] + 23)) else 255, 0), (enemy.rect().centerx + (-7 if enemy.flip else 7) - render_scroll[0], enemy.pos[1] + 23 - render_scroll[1]), 1)
            
            for item in self.items_nearby.copy():
                item.render(self.display, render_scroll)
                if item.life == 0:
                    self.items_nearby.remove(item)

            if self.player.attacking != 0:
                for enemy in self.enemies:
                    if enemy.rect().colliderect(self.attack_rect):
                        if enemy.attacked == 0:
                            enemy.current_hp -=1
                            enemy.attacked = 30
                            enemy.velocity[1] = -2
                            enemy.flip = not enemy.flip

                        if enemy.current_hp <= 0:
                            dropped_item = Sword('slime_stick', self)
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
            self.gun.render(self.display_2, render_scroll)
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)   
    
Game().run()