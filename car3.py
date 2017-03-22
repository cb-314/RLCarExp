import pymunk
import pygame
from pygame.locals import *
from pymunk import pygame_util
from pymunk.vec2d import Vec2d

class Car:
  def __init__(self, space, position):
    self.mass = 1.0
    self.size = (20, 10)
    self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, self.size)) 
    self.body.position = position
    self.poly = pymunk.Poly.create_box(self.body, self.size)
    space.add(self.body, self.poly)
  def accelerate(self, force):
    car.body.apply_force_at_local_point((force, 0.0), (-self.size[0]/2.0, 0.0))
  def front_wheel(self, steer_angle=0.0):
    velocity_wheel = self.body.velocity_at_local_point((self.size[0]/2.0, 0.0))
    steer_vector = Vec2d(1.0, 0.0)
    steer_vector.rotate(self.body.angle + steer_angle)
    friction_parallel = -0.1*velocity_wheel.dot(steer_vector)
    friction_perpendicular = -1.0*velocity_wheel.dot(steer_vector.perpendicular())
    friction = Vec2d(friction_parallel, friction_perpendicular)
    car.body.apply_force_at_local_point(friction, (self.size[0]/2.0, 0.0))
  def back_wheel(self):
    velocity_wheel = self.body.velocity_at_local_point((-self.size[0]/2.0, 0.0))
    steer_vector = Vec2d(1.0, 0.0)
    steer_vector.rotate(self.body.angle)
    friction_parallel = -0.1*velocity_wheel.dot(steer_vector)
    friction_perpendicular = -1.0*velocity_wheel.dot(steer_vector.perpendicular())
    friction = Vec2d(friction_parallel, friction_perpendicular)
    car.body.apply_force_at_local_point(friction, (-self.size[0]/2.0, 0.0))

if __name__ == "__main__":
  pygame.init()
  screen = pygame.display.set_mode((800, 800))
  clock = pygame.time.Clock()

  space = pymunk.Space() 
  space.gravity = (0, 0)

  car = Car(space, (300, 300))

  draw_options = pygame_util.DrawOptions(screen)
  for i in range(3000):
    if i < 200:
      car.accelerate(10.0)
      car.front_wheel()
      car.back_wheel()
    if i > 200 and i < 1000:
      car.accelerate(10.0)
      car.front_wheel(0.1)
      car.back_wheel()
    if i > 1000:
      car.accelerate(10.0)
      car.front_wheel()
      car.back_wheel()
    
    space.step(1/100.0)
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(100)
