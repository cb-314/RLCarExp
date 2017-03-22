import pymunk
import pymunk.matplotlib_util
import matplotlib.pyplot as plt

space = pymunk.Space()      # Create a Space which contain the simulation
space.gravity = 0,-1000     # Set its gravity

body = pymunk.Body(1,1666)  # Create a Body with mass and moment
body.position = 50,100      # Set the position of the body

poly = pymunk.Poly.create_box(body) # Create a box shape and attach to body
space.add(body, poly)       # Add both body and shape to the simulation

plt.ion()
for i in range(100):
  space.step(0.01)
  plt.clf()
  plt.title(str(i))
  drawer = pymunk.matplotlib_util.DrawOptions(plt.gca())
  space.debug_draw(drawer)
  plt.gca().set_xlim((0, 1000))
  plt.gca().set_aspect("equal", "datalim")
  plt.pause(1e-6)
  plt.draw()
