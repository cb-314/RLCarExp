from pygame.math import Vector2
import math
from matplotlib import pyplot as plt

carLocation = Vector2(0.0, 0.0)
carHeading = 0.0
carSpeed = 1.0
steerAngle = 0.0
wheelBase = 1.0
dt = 0.1

for i in range(10):
  frontWheel = carLocation + wheelBase/2.0 * Vector2(math.cos(carHeading), math.sin(carHeading) )
  backWheel = carLocation - wheelBase/2.0 * Vector2(math.cos(carHeading), math.sin(carHeading) )

  backWheel += carSpeed * dt * Vector2(math.cos(carHeading) , math.sin(carHeading))
  frontWheel += carSpeed * dt * Vector2(math.cos(carHeading+steerAngle) , math.sin(carHeading+steerAngle))

  carLocation = (frontWheel + backWheel)/2.0
  carHeading = math.atan2( frontWheel.y - backWheel.y , frontWheel.x - backWheel.x )

  plt.plot(carLocation.x, carLocation.y, "k.")
plt.show()
