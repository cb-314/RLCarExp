import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import PolynomialFeatures
import matplotlib.pyplot as plt
import math
import h5py
import pymunk
from pymunk.vec2d import Vec2d

class CarModelSimple:
  def __init__(self):
    self.position = np.array([0.0, 0.0])
    self.velocity = np.array([1.0, 0.0])
  def step(self, steer_angle, dt):
    c = math.cos(steer_angle)
    s = math.sin(steer_angle)
    rot = np.array([[c, -s], [s, c]])
    self.velocity = rot.dot(self.velocity)
    self.position = self.position + dt * self.velocity

class CarModelMunk:
  """ A simple car model, based on only two instead of four wheels. Both wheels
  are implemented as a single contact point with anisotropic friction.
  Speciffically, this means that friction against movement in one direction
  ("rolling") has a lot less (right now 30 times less) friction that in the
  perpendicular direction ("skidding"). Additionally, the front wheel can be
  rotated to some degree, which is modelled instantaneously. The heavy lifting
  of the physics calculations with impulses, moment of inertia, torques applied
  by the wheels, and so on is performend by pymuk by modelling the car as a
  simple box with one wheel at each end. The anisotropic friction is
  implemented by hand applying the forces directly as pymunk does not implement
  anisotropic friction. The dynamics seem to be allright with the current
  parametrization by playing a bit with it.
  
  If you want to check out the car model evolution check the folder carmodels.
  With carmodel3 you have more or less the current carmodelmunk and you have a
  pygame interface to play with it using the arrow keys. """
  def __init__(self):
    self.space = pymunk.Space() 
    self.space.gravity = (0, 0)
    self.mass = 1.0
    self.size = (20, 10)
    self.body = pymunk.Body(self.mass, pymunk.moment_for_box(self.mass, self.size)) 
    self.poly = pymunk.Poly.create_box(self.body, self.size)
    self.space.add(self.body, self.poly)
    self.position = np.array([self.body.position[0], self.body.position[1]])
    self.velocity = np.array([self.body.velocity[0], self.body.velocity[1]])
  def step(self, steer_angle, dt):
    self.drive(100.0, 0.0, steer_angle)
    self.space.step(dt)
    self.position = np.array([self.body.position[0], self.body.position[1]])
    self.velocity = np.array([self.body.velocity[0], self.body.velocity[1]])
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
  def __init__(self, dt):
    self.dt = dt
    self.car_model = CarModelMunk()
    self.steer_angle = 0.0
    self.reward = 0.0
    self.epsilon0 = 0.0
    self.q_model = RandomForestRegressor(n_estimators=100)
    self.log = []
    self.rewards = []
  def logging(self):
    row = [math.atan2(self.car_model.velocity[1], self.car_model.velocity[0]), self.steer_angle]
    self.log.append(row)
    self.rewards.append(self.reward)
    if len(self.log) % 10000 == 0:
      with h5py.File("log.hdf5", "w") as f:
        f.create_dataset("log", data=np.array(self.log), chunks=True, compression="gzip")
        f.create_dataset("rewards", data=np.array(self.rewards), chunks=True, compression="gzip")
  def step(self):
    steer_angle_space = np.linspace(-0.2, 0.2, 21)
    # epsilon-greedy
    epsilon = np.random.rand(1)[0]
    #epsilon
    if len(self.log) % 100 == 0 and len(self.log) > 0:
      # retrain model
      self.q_model = RandomForestRegressor()
      self.q_model.fit(self.log, self.rewards)
    if len(self.log) > 500:
      self.epsilon0 = 1e-2 + 5e-1 * math.exp(-2e-3*len(self.log))
    else:
      self.epsilon0 = 1.0
    if epsilon < self.epsilon0:
      self.steer_angle = np.random.choice(steer_angle_space)
    # greedy
    else:
      # use model to decide on action
      search = []
      for steer_angle in steer_angle_space:
        x = [[math.atan2(self.car_model.velocity[1], self.car_model.velocity[0]), steer_angle]]
        q = self.q_model.predict(x)[0]
        search.append([steer_angle, q])
      search.sort(key=lambda row: row[-1])
      best = search[-1]
      self.steer_angle = best[0]
    # remember velocity
    last_velocity = np.array(self.car_model.velocity)
    # execute action
    self.car_model.step(self.steer_angle, self.dt)
    # calculate reward
    self.reward = -abs(math.atan2(self.car_model.velocity[1], self.car_model.velocity[0])/np.pi) + abs(math.atan2(last_velocity[1], last_velocity[0])/np.pi)
    # logging
    self.logging()

if __name__ == "__main__":
  position_log = []

  car = Car(1e-2)
  
  plt.ion()
  t = 0
  while True:
    print t
    car.step()
    position_log.append(np.array(car.car_model.position))

#    # kicks
#    if t% 200 == 0 and t >500:
#      impulse = np.random.uniform(-200, 200)
#      car.car_model.body.apply_impulse_at_local_point((0.0, impulse), (car.car_model.size[0]/2.0, 0.0))

    if t % 100 == 0 and t >= 500:
      plt.clf()
      plt.suptitle(str(t)+" "+"{:.3f}".format(np.sum(car.rewards))+" "+"{:.3f}".format(car.epsilon0))
      plt.subplot(221)
      plt.title("trajectory")
      plt.plot([p[0] for p in position_log], [p[1] for p in position_log], "k-")
      plt.plot(position_log[-1][0], position_log[-1][1], "k.")
      plt.xlabel("x")
      plt.ylabel("y")
      plt.gca().set_aspect("equal", "datalim")
      plt.subplot(222)
      plt.title("angle vs. steer_angle vs. reward")
      plt.hist([p[1] for p in car.log])
      plt.subplot(223)
      plt.title("angle vs. steer_angle vs. reward")
      plt.hexbin([p[0] for p in car.log], [p[1] for p in car.log], car.rewards, gridsize=20)
      plt.xlabel("angle")
      plt.ylabel("steerangle")
      plt.colorbar()
      plt.subplot(224)
      plt.title("q_model")
      va = np.linspace(-np.pi, np.pi, 21)
      sa = np.linspace(-0.2, 0.2, 21)
      q = np.empty((len(va), len(sa)))
      for i, v in enumerate(va):
        for j, s in enumerate(sa):
          q[i,j] = car.q_model.predict([[v, s]])
      plt.pcolormesh(va, sa, q.T)
      cbar = plt.colorbar()
      cbar.set_label("q")
      plt.xlabel("angle")
      plt.ylabel("steerangle")
      plt.pause(1e-3)
      plt.draw()
    t = t +1
