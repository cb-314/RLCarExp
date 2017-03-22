import pymunk
import pygame
from pygame.locals import *
from pymunk import pygame_util
pygame.init()
screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

class Car:
  def __init__(self, space, position):
    self.mass = 1.0
    self.size = (20, 10)
    self.steer_angle = 0.0
    self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, self.size)) 
    self.body.position = position
    self.poly = pymunk.Poly.create_box(self.body, self.size)
    space.add(self.body, self.poly)
  def accelerate(self, force):
    car.body.apply_force_at_local_point((force, 0.0), (-self.size[0]/2.0, 0.0))


if __name__ == "__main__":
  space = pymunk.Space() 
  space.gravity = (0, 0)

  car = Car(space, (300, 300))

  draw_options = pygame_util.DrawOptions(screen)

  for i in range(1000):
    if i < 200:
      car.accelerate(10.0) 
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)
    space.step(1/100.0)
    pygame.display.flip()
    clock.tick(100)
