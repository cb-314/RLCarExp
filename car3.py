import pymunk
import pygame
from pygame.locals import *
from pymunk import pygame_util
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

space = pymunk.Space()      # Create a Space which contain the simulation
space.gravity = (0, 0)     # Set its gravity

body = pymunk.Body(1, pymunk.moment_for_box(1, (10,5)))  # Create a Body with mass and moment
body.position = (300, 300)      # Set the position of the body

poly = pymunk.Poly.create_box(body, (10, 5)) # Create a box shape and attach to body
space.add(body, poly)       # Add both body and shape to the simulation

draw_options = pygame_util.DrawOptions(screen)

for i in range(1000):
  if i < 200:
    body.apply_force_at_local_point((0.0, 10.0), (10.0, 0.0))
  
  screen.fill((0, 0, 0))
  space.debug_draw(draw_options)
  space.step(1/100.0)
  pygame.display.flip()
  clock.tick(100)
