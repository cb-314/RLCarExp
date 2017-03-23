import pymunk
import pygame
from pygame.locals import *
from pymunk import pygame_util
from pymunk.vec2d import Vec2d
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
import matplotlib.pyplot as plt
import xgboost as xgb
import math

class CarModel:
  def __init__(self, space, position):
    self.mass = 1.0
    self.size = (20, 10)
    self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, self.size)) 
    self.body.position = position
    self.poly = pymunk.Poly.create_box(self.body, self.size)
    space.add(self.body, self.poly)
  def drive(self, acceleration, brake, steer_angle):
    self.accelerate(acceleration)
    self.brake(brake)
    self.front_wheel(steer_angle)
    self.back_wheel()
  def accelerate(self, force):
    self.body.apply_force_at_local_point((force, 0.0), (-self.size[0]/2.0, 0.0))
  def brake(self, force):
    velocity = self.body.velocity_at_local_point((0.0, 0.0))
    heading = Vec2d(1.0, 0.0)
    heading.rotate(self.body.angle)
    if abs(velocity.dot(heading)) > 1e-3:
      sign = velocity.dot(heading) / abs(velocity.dot(heading))
      self.body.apply_force_at_local_point((-sign*force, 0.0), (0.0, 0.0))
  def front_wheel(self, steer_angle=0.0):
    velocity_wheel = self.body.velocity_at_local_point((self.size[0]/2.0, 0.0))
    steer_vector = Vec2d(1.0, 0.0)
    steer_vector.rotate(self.body.angle + steer_angle)
    friction_parallel = -0.1*velocity_wheel.dot(steer_vector)
    friction_perpendicular = -3.0*velocity_wheel.dot(steer_vector.perpendicular())
    friction = Vec2d(friction_parallel, friction_perpendicular)
    self.body.apply_force_at_local_point(friction, (self.size[0]/2.0, 0.0))
  def back_wheel(self):
    velocity_wheel = self.body.velocity_at_local_point((-self.size[0]/2.0, 0.0))
    steer_vector = Vec2d(1.0, 0.0)
    steer_vector.rotate(self.body.angle)
    friction_parallel = -0.1*velocity_wheel.dot(steer_vector)
    friction_perpendicular = -3.0*velocity_wheel.dot(steer_vector.perpendicular())
    friction = Vec2d(friction_parallel, friction_perpendicular)
    self.body.apply_force_at_local_point(friction, (-self.size[0]/2.0, 0.0))

class Car:
  def __init__(self, space, position):
    self.car_model = CarModel(space, position)
    self.last_position = Vec2d(self.car_model.body.position)
    self.acceleration = 50.0
    self.brake = 0.0
    self.steer_angle = 0.0
    self.reward = 0.0
    self.q_model = KNeighborsRegressor()
    self.log = []
    self.rewards = []
  def logging(self):
    row = [math.cos(self.car_model.body.angle), math.sin(self.car_model.body.angle), self.car_model.body.angular_velocity, self.car_model.body.velocity.x/200.0, self.car_model.body.velocity.y/200.0, self.steer_angle]
    self.log.append(row)
    self.rewards.append(self.reward)
  def step(self):
    steer_angle_space = np.linspace(-0.2, 0.2, 101)
    # calculate last reward
    self.reward = self.car_model.body.position.x - self.last_position.x
    # don't decide every timestep
    if len(self.log) % 10:
      # epsilon-greedy
      epsilon = np.random.rand(1)[0]
      #epsilon
      if epsilon < 1e-2 or len(self.log) < 500:
        self.steer_angle = np.random.choice(steer_angle_space)
      # greedy
      else:
        if len(self.log) % 1000 == 0:
          # retrain model
          self.q_model = KNeighborsRegressor(n_jobs=4)
          self.q_model.fit(self.log, self.rewards)
        # use model to decide on action
        try:
          search = []
          for steer_angle in steer_angle_space:
            x = [[math.cos(self.car_model.body.angle), math.sin(self.car_model.body.angle), self.car_model.body.angular_velocity, self.car_model.body.velocity.x/200.0, self.car_model.body.velocity.y/200.0, steer_angle]]
            q = q_model.predict(x)[0]
            search.append([steer_angle, q])
          search.sort(key=lambda row: row[-1])
          best = search[-1]
          self.steer_angle = best[0]
        except: # corner case for first training
          self.steer_angle = np.random.choice(steer_angle_space)
    # execute action
    self.car_model.drive(self.acceleration, self.brake, self.steer_angle)
    # update last_position and logging
    self.last_position = Vec2d(self.car_model.body.position)
    self.logging()

if __name__ == "__main__":
#  pygame.init()
#  screen = pygame.display.set_mode((1600, 800))
#  clock = pygame.time.Clock()
#  draw_options = pygame_util.DrawOptions(screen)

  space = pymunk.Space() 
  space.gravity = (0, 0)
 
  position_log = []

  car = Car(space, (200, 400))
  
  plt.ion()
  for i in range(1000000):
    car.step()
    position_log.append(car.car_model.body.position)

    if i % 1000 == 0:
      plt.clf()
      plt.plot([p.x for p in position_log], [p.y for p in position_log], "k-")
      plt.plot(position_log[-1].x, position_log[-1].y, "k.")
      plt.gca().set_aspect("equal", "datalim")
      plt.title(str(i)+" "+str(np.sum(car.rewards)))

      plt.pause(1e-3)
      plt.draw()

    # physical simulation
    space.step(1/100.0)
    # drawing etc
#    screen.fill((255, 255, 255))
#    space.debug_draw(draw_options)
#    pygame.display.flip()
#    clock.tick(50)
