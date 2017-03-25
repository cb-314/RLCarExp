import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import math
import cPickle

class CarModel:
  def __init__(self):
    self.position = np.array([0.0, 0.0])
    self.velocity = np.array([1.0, 0.0])
  def step(self, steer_angle, dt):
    c = math.cos(steer_angle)
    s = math.sin(steer_angle)
    rot = np.array([[c, -s], [s, c]])
    self.velocity = rot.dot(self.velocity)
    self.position = self.position + dt * self.velocity

class Car:
  def __init__(self, dt):
    self.dt = dt
    self.car_model = CarModel()
    self.steer_angle = 0.0
    self.reward = 0.0
    self.q_model = RandomForestRegressor(n_estimators=100)
    self.log = []
    self.rewards = []
  def logging(self):
    row = [math.atan2(self.car_model.velocity[1], self.car_model.velocity[0]), self.steer_angle]
    self.log.append(row)
    self.rewards.append(self.reward)
    if len(self.log) % 100000 == 0:
      with open("log2.pick", "wb") as out_file:
        cPickle.dump({"log": self.log, "rewards": self.rewards}, out_file)
  def step(self):
    steer_angle_space = np.linspace(-0.2, 0.2, 21)
    # epsilon-greedy
    epsilon = np.random.rand(1)[0]
    #epsilon
    if epsilon < 1e-2 or len(self.log) < 5000:
      self.steer_angle = np.random.choice(steer_angle_space)
    # greedy
    else:
      if len(self.log) % 1000 == 0:
        # retrain model
        self.q_model = KNeighborsRegressor(n_neighbors=100, weights="distance")
        self.q_model.fit(self.log, self.rewards)
      # use model to decide on action
      search = []
      for steer_angle in steer_angle_space:
        x = [[math.atan2(self.car_model.velocity[1], self.car_model.velocity[0]), steer_angle]]
        q = self.q_model.predict(x)[0]
        search.append([steer_angle, q])
      search.sort(key=lambda row: row[-1])
      best = search[-1]
      self.steer_angle = best[0]
    # update last_position and logging
    self.last_position = np.array(self.car_model.position)
    self.logging()
    # remember position
    last_position = np.array(self.car_model.position)
    # execute action
    self.car_model.step(self.steer_angle, self.dt)
    # calculate reward
    self.reward = self.car_model.position[0] - last_position[0]

if __name__ == "__main__":
  position_log = []

  car = Car(1e-2)
  
  plt.ion()
  t = 0
  while True:
    print t
    car.step()
    position_log.append(np.array(car.car_model.position))

    if t % 1000 == 0 and t >= 5000:
      plt.clf()
      plt.suptitle(str(t)+" "+str(np.sum(car.rewards)))
      plt.subplot(221)
      plt.title("trajectory")
      plt.plot([p[0] for p in position_log], [p[1] for p in position_log], "k-")
      plt.plot(position_log[-1][0], position_log[-1][1], "k.")
      plt.xlabel("x")
      plt.ylabel("y")
      plt.gca().set_aspect("equal", "datalim")
      plt.subplot(222)
      plt.title("steer_angle hist")
      plt.hist([p[1] for p in car.log])
      plt.subplot(223)
      plt.title("angle vs. steer_angle vs. reward")
      plt.hexbin([p[0] for p in car.log], [p[1] for p in car.log], car.rewards, gridsize=20)
      plt.xlabel("angle")
      plt.ylabel("steerangle")
      plt.colorbar()
      plt.subplot(224)
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
