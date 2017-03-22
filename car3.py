import pymunk
import pygame
from pygame.locals import *
from pymunk import pygame_util
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

space = pymunk.Space() 
space.gravity = (0, 0)

# car
body = pymunk.Body(1, pymunk.moment_for_box(1, (20,10))) 
body.position = (300, 300) 
poly = pymunk.Poly.create_box(body, (20, 10))
poly.friction = 1
space.add(body, poly)

draw_options = pygame_util.DrawOptions(screen)

for i in range(1000):
  if i < 200:
    body.apply_force_at_local_point((0.0, 10.0), (10.0, 0.0))
  
  screen.fill((0, 0, 0))
  space.debug_draw(draw_options)
  space.step(1/100.0)
  pygame.display.flip()
  clock.tick(100)
