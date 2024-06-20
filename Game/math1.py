import math
import random
import pygame
import sys


screen = pygame.display.set_mode((600, 400))
display = pygame.Surface((300, 200))

pygame.init()
clock = pygame.time.Clock()

render_points = [
    [ 10 * math.cos(45) + 150, 10 * math.sin(45) + 150],
    [ 10 * math.cos(45 + math.pi * 0.5) + 100, 10 * math.sin(45 + math.pi * 0.5) + 100],
    [ 10 * math.cos(45 + math.pi) + 100, 10 * math.sin(45 + math.pi) + 100],
    [ 10 * math.cos(45 - math.pi * 0.5) + 100, 10 * math.sin(45 - math.pi * 0.5) + 100],
]

current_selected = 0
while True:

    screen.fill((100, 100 ,100))
    display.fill((255, 255, 255))
    pygame.draw.polygon(display, (0, 0, 0), render_points, 3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            print(render_points)
            if event.key == pygame.K_UP:
                    render_points[current_selected][1] -= 2
            
            if event.key == pygame.K_DOWN:
                    render_points[current_selected][1] += 2
            
            if event.key == pygame.K_LEFT:
                    render_points[current_selected][0] -= 2
            
            if event.key == pygame.K_RIGHT:
                    render_points[current_selected][0] += 2
                
        if event.type == pygame.MOUSEBUTTONDOWN:

            # if event.button == 1:
            #     for points in render_points:
            #          print(f'{math.acos((points[0])/10)} : {math.asin((points[1])/10)}')

            if event.button == 4:
                current_selected = (current_selected + 1) % 4

            print(current_selected)
    
    screen.blit(pygame.transform.scale2x(display, screen), (0, 0))
    pygame.display.update()
    clock.tick(60)
