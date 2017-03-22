from pygame.math import Vector2
import math
from matplotlib import pyplot as plt

class Car:
  def __init__(self):
    # dynamic stuff
    self.position = Vector2(0.0, 0.0)
    self.velocity = Vector2(1e-6, 0.0)
    self.heading = 0.0
    self.angular_velocity = 0.0
    # motor commandos
    self.steer_angle = 0.0
    self.motor_force = 1.0
    # parameters
    self.mass = 1.0
    self.wheel_base = 1.0
    self.wheel_friction = (1e-3, 1e-1)
    # thin cylinder spun around its center: L = 1/12 ml²
    self.angular_mass = 1.0/12.0 * self.mass * self.wheel_base * self.wheel_base 
  def update(self, dt=1e-2):
    total_force = Vector2(0.0, 0.0)
    total_force = total_force + self.motor_force * Vector2(math.cos(self.heading), math.sin(self.heading))
    # turning is more complicated than I thought because we need a heading direction and angular momentum and so on
    # which in turn makes the back wheen skidd etc.
    # update velocity
    self.velocity = self.velocity + total_force / self.mass * dt
    # update position
    self.position = self.position + self.velocity * dt


if __name__ == "__main__":
  car = Car()
  for t in range(100):
    car.motor_force = 0.1
    car.update(dt=1e-2)
    plt.plot(car.position.x, car.position.y, "k.")
  plt.gca().set_aspect("equal", "datalim")
  plt.show()
