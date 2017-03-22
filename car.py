from pygame.math import Vector2
import math
from matplotlib import pyplot as plt

class Car:
  def __init__(self):
    self.carLocation = Vector2(0.0, 0.0)
    self.carHeading = 0.0
    self.carSpeed = 1.0
    self.steerAngle = 0.0
    self.wheelBase = 1.0
    self.frontWheel = self.carLocation + self.wheelBase/2.0 * Vector2(math.cos(self.carHeading), math.sin(self.carHeading) )
    self.backWheel = self.carLocation - self.wheelBase/2.0 * Vector2(math.cos(self.carHeading), math.sin(self.carHeading) )
  def update(self, dt):
    self.frontWheel = self.carLocation + self.wheelBase/2.0 * Vector2(math.cos(self.carHeading), math.sin(self.carHeading) )
    self.backWheel = self.carLocation - self.wheelBase/2.0 * Vector2(math.cos(self.carHeading), math.sin(self.carHeading) )
    self.backWheel += self.carSpeed * dt * Vector2(math.cos(self.carHeading) , math.sin(self.carHeading))
    self.frontWheel += self.carSpeed * dt * Vector2(math.cos(self.carHeading+self.steerAngle) , math.sin(self.carHeading+self.steerAngle))
    self.carLocation = (self.frontWheel + self.backWheel)/2.0
    self.carHeading = math.atan2( self.frontWheel.y - self.backWheel.y , self.frontWheel.x - self.backWheel.x )

car = Car()

for i in range(500):
  if i % 200 == 0:
    car.steerAngle = 0.1
  else:
    car.steerAngle = 0.0
  car.update(dt=0.01)
  plt.plot(car.carLocation.x, car.carLocation.y, "k.")
plt.gca().set_aspect("equal", "datalim")
plt.show()
