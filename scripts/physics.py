import math
import random

from scripts.particles import Particles

class Physics:
    """Axis-separated tile collision, gravity and drag.

    Defaults are the values this platformer was tuned with. A different game
    sets its own before entities are built.
    """

    def __init__(self, gravity=0.1, max_fall=5, drag=1, friction=0.1, water_drag=0.6):
        self.gravity = gravity
        self.max_fall = max_fall
        self.drag = drag
        self.friction = friction
        self.water_drag = water_drag

    def update(self, entity, tilemap, movement=(0, 0), offset=(0, 0), dt=1/60):
        # Every tuned value below was authored per frame at 60 FPS. frame keeps
        # those exact numbers so behaviour is unchanged at dt = 1/60 and
        # scales correctly when a frame runs long.
        frame = 60 * dt

        entity.movement = movement
        entity.collisions = {'up' : False, 'down' : False, 'right' : False, 'left' : False}
        entity.frame_movement = (movement[0] + entity.velocity[0], movement[1] + entity.velocity[1])

        entity.pos[0] += entity.frame_movement[0] * entity.drag
        entity_rect = entity.rect()
        tile_data = tilemap.tiles_rect_around(entity.pos)

        for i in range(len(tile_data['rects'])):
            rect = tile_data['rects'][i]
            color = tile_data['color'][i]
            if entity_rect.colliderect(rect):
                if entity.frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    entity.collisions['right'] = True

                if entity.frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    entity.collisions['left'] = True
                entity.pos[0] = entity_rect.x

        entity.pos[1] += entity.frame_movement[1] * entity.drag
        entity_rect = entity.rect()
        tile_data = tilemap.tiles_rect_around(entity.pos)

        for i in range(len(tile_data['rects'])):
            rect = tile_data['rects'][i]
            color = tile_data['color'][i]

            if entity_rect.colliderect(rect):
                if int(entity.drag):
                    spawn_particles = random.random() + int(abs(entity.velocity[1]))
                else:
                    spawn_particles = False

                if entity.frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    entity.collisions['down'] = True

                if entity.frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    entity.collisions['up'] = True

                entity.pos[1] = entity_rect.y

                if entity.type == 'player' or entity.type == 'enemy':
                    if spawn_particles > 0.6 and (entity.collisions['down'] or entity.collisions['up']):
                        if entity.action != 'idle':
                            x = entity.pos[0]
                            if entity.collisions['down']:
                                y = rect.top
                                angle = ((random.random() * math.pi) + math.pi)
                                speed = random.random() * random.random()
                                entity.effects.particles.append(Particles(entity.game, 'dust', angle, speed, (x, y), color_key=color))
                            elif entity.collisions['up']:
                                y = rect.bottom
                                angle = ((random.random()) * math.pi)
                                speed = random.random() * random.random()
                                entity.effects.particles.append(Particles(entity.game, 'dust', angle, speed, (x, y), color_key=color))

        water_loc_int = [int((entity.pos[0] //tilemap.tile_size)), int((entity.pos[1]//tilemap.tile_size))]
        water_loc = str(water_loc_int[0]) + ";" + str(water_loc_int[1])

        if water_loc in tilemap.water_map:
            entity.drag = self.water_drag
            tilemap.propogate_wave(water_loc, water_loc_int, velocity=entity.velocity, offset=offset, entity_rect=entity_rect)
        else:
            entity.drag = min(1, entity.drag + 0.01 * frame)

        if movement[0] > 0:
            entity.flip = False
        elif movement[0] < 0:
            entity.flip = True

        entity.velocity[1] = min(self.max_fall * entity.drag, entity.velocity[1] + self.gravity * frame)
        if entity.collisions['up'] or entity.collisions['down']:
            entity.velocity[1] = 0

        if entity.velocity[0] > 0:
            entity.velocity[0] = max(entity.velocity[0] - self.friction * frame, 0)
        elif entity.velocity[0] < 0:
            entity.velocity[0] = min(entity.velocity[0] + self.friction * frame, 0)

        entity.animation.update()

        entity.track = max(0, entity.track - 1)
