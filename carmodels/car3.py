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
    self.log = {}
    self.log["front"] = []
    self.log["center"] = []
    self.log["back"] = []
    self.logging()
  def drive(self, acceleration, brake, steer_angle):
    self.accelerate(acceleration)
    self.brake(brake)
    self.front_wheel(steer_angle)
    self.back_wheel()
    self.logging()
  def logging(self):
    temp = Vec2d(self.size[0]/2.0, 0.0)
    temp.rotate(self.body.angle)
    self.log["front"].append(self.body.position + temp)
    self.log["center"].append(self.body.position)
    self.log["back"].append(self.body.position - temp)
  def accelerate(self, force):
    car.body.apply_force_at_local_point((force, 0.0), (-self.size[0]/2.0, 0.0))
  def brake(self, force):
    velocity = self.body.velocity_at_local_point((0.0, 0.0))
    heading = Vec2d(1.0, 0.0)
    heading.rotate(self.body.angle)
    if abs(velocity.dot(heading)) > 1e-3:
      sign = velocity.dot(heading) / abs(velocity.dot(heading))
      car.body.apply_force_at_local_point((-sign*force, 0.0), (0.0, 0.0))
  def front_wheel(self, steer_angle=0.0):
    velocity_wheel = self.body.velocity_at_local_point((self.size[0]/2.0, 0.0))
    steer_vector = Vec2d(1.0, 0.0)
    steer_vector.rotate(self.body.angle + steer_angle)
    friction_parallel = -0.1*velocity_wheel.dot(steer_vector)
    friction_perpendicular = -3.0*velocity_wheel.dot(steer_vector.perpendicular())
    friction = Vec2d(friction_parallel, friction_perpendicular)
    car.body.apply_force_at_local_point(friction, (self.size[0]/2.0, 0.0))
  def back_wheel(self):
    velocity_wheel = self.body.velocity_at_local_point((-self.size[0]/2.0, 0.0))
    steer_vector = Vec2d(1.0, 0.0)
    steer_vector.rotate(self.body.angle)
    friction_parallel = -0.1*velocity_wheel.dot(steer_vector)
    friction_perpendicular = -3.0*velocity_wheel.dot(steer_vector.perpendicular())
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
    
    acceleration = 0.0
    brake = 0.0
    steer_angle = 0.0
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
      acceleration = 100.0
    if keys[pygame.K_DOWN]:
      brake = 200
    if keys[pygame.K_LEFT]:
      steer_angle = 0.1
    if keys[pygame.K_RIGHT]:
      steer_angle = -0.1
    pygame.event.pump()
    
    car.drive(acceleration, brake, steer_angle)

    space.step(1/100.0)
    screen.fill((255, 255, 255))
    space.debug_draw(draw_options)
    w, h = pygame.display.get_surface().get_size()
    pygame.draw.aalines(screen, [255,0,0], False, [(point.x, h-point.y) for point in car.log["front"][-500:]])
    pygame.draw.aalines(screen, [0,0,0], False, [(point.x, h-point.y) for point in car.log["center"][-500:]])
    pygame.draw.aalines(screen, [0,0,255], False, [(point.x, h-point.y) for point in car.log["back"][-500:]])
    pygame.display.flip()
    clock.tick(100)
