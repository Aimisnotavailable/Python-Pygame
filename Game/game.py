import pygame
import sys
import os
import random
import math
from scripts.utils import load_image, load_images, Animation, Background
from scripts.tilemap import TileMap
from scripts.entities import PhysicsEntities, Player, Enemy
from scripts.items import Weapon, Sword, Gun
from scripts.inventory import Inventory
from scripts.clouds import Clouds, Cloud
from scripts.sparks import Sparks
from scripts.particles import Particles
#from test_scripts.water1 import Water
from scripts.water import Water
from scripts.rotation import Rotation
from scripts.assets import Assets
from scripts.projectiles import Projectiles
from scripts.screenshake import ScreenShake
from scripts.transition import Transition
from scripts.sfx import SoundMixer

from scripts.seasonal.christmas.santa import Santa

BASE_IMG_PATH = 'data/images/'

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Game")
        pygame.mouse.set_visible(False)

        self.time = 0

        self.screen = pygame.display.set_mode((600, 400))
        self.display = pygame.Surface((300, 200), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((300, 200))
        self.night_mask = pygame.Surface((300, 200), pygame.SRCALPHA)

        self.clock = pygame.time.Clock()

        self.assets = Assets().fetch(payload={'img' : ['all']})
        
        self.cursor = self.assets['cursor'].copy()

        self.current_weapon = Gun(self, 'dirt_gun') # Sword(self,  'sword', color=(100, 100, 100)) # Sword(self, 'dirt_stick', color=(150, 75, 0))
        
        self.pos = (self.display.get_width()//2, self.display.get_height()//2)
        self.load()
        # self.weapon_pos = self.pos
        
        
        
        # self.inventory.item_list[1] = 

       

        # print(self.player.pos)
        # for loc in self.tilemap.tilemap:
        #     if random.randint(0, 20) == 1:
        #         self.enemies.append(Enemy(self, (self.tilemap.tilemap[loc]['pos'][0] * self.tilemap.tile_size, self.tilemap.tilemap[loc]['pos'][1] * self.tilemap.tile_size)))

    def load(self):

        self.tilemap = TileMap(self)
        self.tilemap.load("data/maps/map.json")
        self.movement = [0, 0]
 
        self.scroll = [0, 0]
        self.angle = 0

        self.sparks = []
        self.projectiles = []
        self.particles = []
        self.enemies = []
        self.items_nearby = []

        self.inventory = Inventory(self.assets['inventory_slot'])
        self.inventory.item_list[self.inventory.current_selected] = self.current_weapon
        self.inventory.item_list[1] = Sword(self, 'sword', color=(100, 100, 100))

        self.rotation = Rotation()
        self.screen_shake = ScreenShake()
        self.transition = Transition()
        self.background = Background(self.assets['background'])
        self.sound = SoundMixer(payload={'background' : ['all'], 'tile' : ['all'], 'player' : ['all']})
        self.sound.play('background_music', vol=0.3)
        self.water = Water()
        self.under_water = False
        self.clouds = Clouds(self.assets['clouds'][0], count=15)
        self.trees = self.tilemap.extract([('tree', 0), ('tree', 1)])
        self.zoom = 1.0
        self.zooming = 0
        self.santa = Santa(self.assets['christmas/santa'].copy(), (0, 0), 0, 2)

        for i in range(70):
            angle = random.random() * math.pi
            speed = random.random() + 3
            pos = [random.random() * self.display.get_width(), random.random() * self.display.get_height()]
            self.particles.append(Particles(self, 'snow', angle, speed, pos))

        for entity in self.tilemap.extract([('entity_spawner', 1), ('entity_spawner', 0)], keep=False):
            pos = entity['pos']
            if entity['variant'] == 1:
                self.player = Player(self, pos)
            else:
                self.enemies.append(Enemy(self, pos))

        self.tree_spawners = []

        for tree in self.trees:
            size = self.assets[tree['type']][tree['variant']].get_size()
            self.tree_spawners.append(pygame.Rect(tree['pos'][0], tree['pos'][1], *size))

        self.entity_track_rect = self.player.rect()
        self.fps = 60
    
    def run(self):
        running = True

        while running:
            self.display.fill((0,0,0,0))
            self.night_mask.fill((0, 0, 0, 140))

            mpos = list(pygame.mouse.get_pos())
            mpos[0] = mpos[0] // 2
            mpos[1] = mpos[1] // 2
            
            if not self.player.track:
                self.entity_track_rect = self.player.rect()
            else:
                self.entity_track_rect = pygame.Rect(*self.projectiles[-1].pos.copy(), 8 , 8)

            self.scroll[0] += ((self.entity_track_rect.centerx - self.display.get_width() / 2 / self.zoom - self.scroll[0]) / (15 if self.zoom <= 1 else 1)) 
            self.scroll[1] += ((self.entity_track_rect.centery - self.display.get_height() / 2 / self.zoom - self.scroll[1]) / (15 if self.zoom <= 1 else 1)) 
            render_scroll = [int(self.scroll[0]), int(self.scroll[1])]

            self.background.render(self.display_2)
            
            for spawner in self.tree_spawners:
                if random.random() * 599999 < spawner[2] * spawner[3]:
                    angle = random.random() * math.pi
                    speed = random.random() + 0.4
                    pos =  (spawner[0] -  random.random() * spawner[2], spawner[1] - random.random() * spawner[3])
                     
                    self.particles.append(Particles(self, 'leaf', angle, speed, pos, color_key=(20, 160, 10)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()   
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_a:
                        self.movement[0] = -2
                    if event.key == pygame.K_d:
                        self.movement[0] = 2
                    if (event.key == pygame.K_w or event.key == pygame.K_SPACE) and self.player.jumps: 
                        self.player.velocity[1] = -3
                        self.player.jumps -= 1
                    
                    if event.key == pygame.K_o:
                        self.sound.stop('background_music')
                        self.load()
                        self.transition.transition = True
                        
                    if event.key == pygame.K_1 and self.player.attacking == 0:
                        self.inventory.current_selected = 0
                        self.current_weapon = self.inventory.item_list[self.inventory.current_selected ]
                    
                    if event.key == pygame.K_2 and self.player.attacking == 0:
                        self.inventory.current_selected = 1
                        self.current_weapon = self.inventory.item_list[self.inventory.current_selected ]

                    if event.key == pygame.K_e and self.current_weapon is not None and self.player.attacking == 0:
                        self.current_weapon.set_drop_status(self.player.pos.copy(), is_dropped=True)
                        self.items_nearby.append(self.current_weapon)
                        self.inventory.remove_item()

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
                                self.items_nearby.remove(item)
                                self.current_weapon.set_drop_status(self.player.pos.copy(), is_dropped=False)
                                break

                    if event.key == pygame.K_r and self.current_weapon is not None and self.current_weapon.type == 'swords' and self.player.attacking == 0:
                        #self.current_weapon.velocity[0] = -5 if self.player.flip else 5

                        self.inventory.remove_item()
                        atk_type = 'throw_meele_attack'
                        self.player.perform_attack(atk_type, self.current_weapon)

                        self.current_weapon = None


                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = 0

                    if event.key == pygame.K_d:
                        self.movement[0] = 0

                if event.type == pygame.MOUSEBUTTONDOWN: 
                    if event.button == 1 and self.current_weapon is not None and self.player.attacking == 0:
                        # self.projectiles.append(Projectiles(self.assets['clouds'][1], speed=10, angle=0, life=10000, pos=(self.player.pos[0] - self.display.get_width(), self.player.pos[1]-15)))
                        if self.current_weapon.type == 'swords':
                            self.player.start_charge(is_initialized=True)
                        elif self.current_weapon.type == 'guns':
                            self.player.shooting = True
                            atk_type = 'shoot_attack'
                            self.player.perform_attack(atk_type, self.current_weapon)
                            self.screen_shake.set_shake_config(strength=4, dur=4)
                    
                    if event.button == 3 and self.current_weapon is not None and self.player.attacking == 0:
                        if self.current_weapon.type == 'guns':
                            atk_type='splash_attack'
                            self.player.perform_attack(atk_type, self.current_weapon)
                            self.screen_shake.set_shake_config(strength=7, dur=15)
                                    

                if event.type == pygame.MOUSEBUTTONUP:
                    if self.current_weapon is not None:
                        if event.button == 1:
                            if self.current_weapon.type == 'swords':
                                if self.player.attacking <= 0:
                                    atk_type = 'normal_attack' if self.player.attack_type < self.player.charge_duration else 'charged_attack'
                                    self.player.perform_attack(atk_type, self.current_weapon)
                            elif self.current_weapon.type == 'guns':
                                self.player.shooting = False
                        if event.button == 3:
                            if self.current_weapon.type == 'guns':
                                self.player.shooting = False

            if self.screen_shake.dur:
                shake_offset = self.screen_shake.screen_shake()
                render_scroll = (int(render_scroll[0] + shake_offset[0]), int(render_scroll[1] + shake_offset[1]))

            if self.santa.done:
                self.santa.angle = (random.random() + 0.5) * math.pi + math.pi
                self.santa.done = False
            else:
                self.santa.render(self.display, render_scroll)

            self.clouds.render(self.display_2, render_scroll)
            self.clouds.update()

            self.tilemap.render(self.display, offset=render_scroll)

            if self.player.shooting and self.player.attacking == 1:
                self.player.attacking = 1
                atk_type = 'shoot_attack'
                self.player.perform_attack(atk_type, self.current_weapon)
                self.screen_shake.set_shake_config(strength=2, dur=4) 

            for particle in self.particles.copy():
                particle.pos[0] += math.cos(particle.angle) * (math.sin(particle.animation.frame)*-1)
                if particle.render(self.display, render_scroll):
                    self.particles.remove(particle)
                

            for spark in self.sparks.copy():
                spark.render(self.display, render_scroll)
                if spark.update():
                    self.sparks.remove(spark)
            # print(self.assets[self.tilemap.tilemap['-11;2']['type']][self.tilemap.tilemap['-11;2']['variant']])
            for projectile in self.projectiles.copy():
                projectile.render(self.display, render_scroll)
                tile = self.tilemap.solid_check(projectile.pos)
                if tile:
                    for i in range(10):
                        angle =  (random.random() - 0.5) + (math.pi if projectile.speed > 0 else 0) + projectile.angle
                        speed = (random.random() + 2)
                        self.sparks.append(Sparks(angle, speed, projectile.pos, self.tilemap.colors[tile['type']][random.randint(0, len(self.tilemap.colors[tile['type']]) - 1 )]))

                    self.sound.play(tile['type'], loop=0, vol=0.8)
                    projectile.kill = True
                
                if projectile.update():
                    projectile.kill = True

                if not projectile.kill:
                    for enemy in self.enemies.copy():
                        if enemy.attacked:
                            continue
                        if enemy.rect().colliderect(pygame.Rect(projectile.pos, projectile.animation.img().get_size())):
                            projectile.kill = True
                            if enemy.attacked == 0:
                                enemy.damage()
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
                
                if projectile.kill:
                    if projectile.spawn:
                        projectile.spawn.set_drop_status(projectile.pos.copy(), is_dropped=True)
                        pos = [projectile.pos[0] + 24 * (1 if math.cos(angle) > 0 else -1), projectile.pos[1] + 8 * (1 if math.sin(angle) > 0 else -1)]
                        projectile.spawn.pos = pos.copy()
                        self.player.teleport(pos.copy())
                        self.sound.play('teleport', variant=0, loop=0) 
                        self.items_nearby.append(projectile.spawn)
                        self.zooming = 0

                    self.player.track = 0
                    self.projectiles.remove(projectile)
                    
                
            if self.player.dashing >= 1:
                for enemy in self.enemies.copy():
                    if enemy.rect().colliderect(self.player.rect()):
                        if enemy.attacked == 0:
                            enemy.damage()

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

            

            p_pos = [(self.player.pos[0] - render_scroll[0] + 5), (self.player.pos[1] - render_scroll[1] + 10)]
            self.angle = self.rotation.get_angle(p_pos, mpos)
            self.rotation.draw_curve(self.display, p_pos, math.radians(self.angle * (-1 if self.rotation.flip_x else 1)), 10)
            
            if self.current_weapon is not None:
                if not self.player.attacking or self.current_weapon.type == "guns":
                    img = self.rotation.img(self.current_weapon.animation.img(), self.angle)

                    # print(self.rotation.angle)
                    
                    if self.angle > 90 and self.angle < 270:
                        self.player.flip = True
                    else:
                        self.player.flip = False

                    # img_rect = img.get_rect(left=p_pos[0] + (-7 if self.player.flip else 12), top = p_pos[1] + 5)
                    
                    img_rect = img.get_rect(center=(p_pos[0] + math.cos(math.radians(self.angle * (-1 if self.rotation.flip_x else 1)))  * 10, p_pos[1] + math.sin(math.radians(self.angle * (-1 if self.rotation.flip_x else 1))) * 8))
                    self.display.blit(img, img_rect)
            
            
            # for i in range(len(self.water.springs)):
            #     if self.player.rect().collidepoint((self.water.springs[i].pos[0] + 160, self.water.springs[i].pos[1] + 96)) and self.player.action != "idle":
            #         self.water.wave(i)
            #         break
                
            for item in self.items_nearby.copy():
                item.render(self.display, render_scroll)
                if item.life == 0:
                    self.items_nearby.remove(item)

            for enemy in self.enemies:
                enemy.update(self.tilemap, offset=render_scroll)
                enemy.render(self.display, offset=render_scroll)
                pygame.draw.circle(self.display, (0, 0 if not self.tilemap.solid_check((enemy.rect().centerx + (-7 if enemy.flip else 7), enemy.pos[1] + 23)) else 255, 0), (enemy.rect().centerx + (-7 if enemy.flip else 7) - render_scroll[0], enemy.pos[1] + 23 - render_scroll[1]), 1)
            
            # if self.projectiles:
            #     pygame.draw.rect(self.display, (255, 255, 255), pygame.Rect(self.projectiles[0].pos[0] - render_scroll[0], self.projectiles[0].pos[1] - render_scroll[1], *self.projectiles[0].img.get_size()))
            # if self.player.attacking != 0 and self.player.atk_type != 'shoot_attack':
            #     for enemy in self.enemies.copy():
            #         if enemy.rect().colliderect():
            #             if enemy.attacked == 0:
            #                 enemy.current_hp -=1
            #                 enemy.attacked = 30
            #                 enemy.velocity[1] = -2
            #                 enemy.flip = not enemy.flip

            #             if enemy.current_hp <= 0:
            #                 dropped_item = Sword(self, 'slime_stick')
            #                 dropped_item.set_drop_status(enemy.pos,is_dropped=True)
            #                 self.items_nearby.append(dropped_item)
            #                 self.enemies.remove(enemy)
            #                 for i in range(30):
            #                     angle = (random.random() + 0.5) * math.pi * 2
            #                     speed = (random.random() + 0.5) + 1
            #                     self.sparks.append(Sparks(angle, speed, enemy.pos))

            self.inventory.render(self.display)
            self.player.update(self.tilemap, self.movement, offset=render_scroll)
            self.player.render(self.display, offset=render_scroll)     
            
            display_mask = pygame.mask.from_surface(self.display)
            display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))

            for offset in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
                self.display_2.blit(display_sillhouette, offset)
            
            self.display_2.blit(self.display, (0, 0))
            # self.water.render(self.display_2, render_scroll)
            cursor_rect = self.cursor.img().get_rect(center=mpos)
            self.display_2.blit(self.cursor.img(), cursor_rect)
            self.cursor.update()
            self.tilemap.render_water(self.display_2, render_scroll)

            if self.transition.transition:
                self.transition.render(self.display_2)

            if self.zooming:
                self.zoom = min(2, self.zoom + 0.01)
                self.fps  = 30
            else:
                self.zoom = max(1, self.zoom - 0.01)
                self.fps =  60
            self.zooming = max(0, self.zooming - 1)

            size =  list(self.screen.get_size())
            self.screen.blit(pygame.transform.scale(self.display_2, (size[0] * self.zoom, size[1] * self.zoom)), (0,0))
            # self.screen.blit(pygame.transform.scale(self.night_mask, self.screen.get_size()), (0, 0))
            # print(self.clock.get_fps())
            # print(self.clock.get_rawtime())
            # print(self.enemies[0].pos)
            pygame.display.update()
            self.clock.tick(self.fps)   
    
Game().run()


