from pygame.math import Vector2
import math
from matplotlib import pyplot as plt

class Car:
  def __init__(self):
    # dynamic stuff
    self.position = Vector2(2.0, 1.0)
    self.velocity = Vector2(1.0, 0.0)
    self.heading = 0.1
    self.angular_velocity = 0.0
    # motor commandos
    self.steer_angle = 0.1
    self.motor_force = 1.0
    # parameters
    self.mass = 1.0
    self.wheel_base = 1.0
    self.wheel_friction = (1e-3, 1e-1)
    # thin cylinder spun around its center: L = 1/12 ml^2
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
  def plot(self):
    # calculate auxiliary positions
    front_wheel_position = self.position + self.wheel_base/2.0 * Vector2(math.cos(self.heading), math.sin(self.heading))
    back_wheel_position = self.position - self.wheel_base/2.0 * Vector2(math.cos(self.heading), math.sin(self.heading))
    # plot car
    plt.plot(self.position.x, self.position.y, "k*")
    plt.plot([back_wheel_position.x, front_wheel_position.x], [back_wheel_position.y, front_wheel_position.y], "k-")
    plt.arrow(front_wheel_position.x, front_wheel_position.y, math.cos(self.heading + self.steer_angle), math.sin(self.heading + self.steer_angle))
    
    plt.gca().set_xlim((0.0, 10.0))
    plt.gca().set_ylim((0.0, 10.0))


if __name__ == "__main__":
  car = Car()
  car.plot()
  plt.show()
#  for t in range(100):
#    car.motor_force = 0.1
#    car.update(dt=1e-2)
#    plt.plot(car.position.x, car.position.y, "k.")
#  plt.gca().set_aspect("equal", "datalim")
#  plt.show()
