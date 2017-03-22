from pygame.math import Vector2
import math
from matplotlib import pyplot as plt

class Car:
  def __init__(self):
    # dynamic stuff
    self.position = Vector2(0.0, 0.0)
    self.velocity = Vector2(0.0, 0.0)
    # motor commandos
    self.steer_angle = 0.0
    self.motor_force = 1.0
    # parameters
    self.mass = 1.0
    self.wheelbase = 1.0
    self.wheel_friction = (1e-3, 1e-1)
  def update(self, dt=1e-2):
    total_force = vector2(0.0, 0.0)
    # update velocity
    self.velocity = self.velocity + total_force / self.mass * dt
    # update position
    self.position = self.position + self.velocity * dt


if __name__ = "__main__":
  for t in range(100):
    car.update(dt=1e-2)
    plt.plot(car.position.x, car.position.y, "k.")
  plt.gca().set_aspect("equal", "datalim")
  plt.show()
