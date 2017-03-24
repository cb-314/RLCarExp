import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
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
    self.last_position = np.array(self.car_model.position)
    self.steer_angle = 0.0
    self.reward = 0.0
    self.q_model = RandomForestRegressor(n_estimators=100)
    self.log = []
    self.rewards = []
  def logging(self):
    row = [self.car_model.velocity[0], self.car_model.velocity[1], self.steer_angle]
    self.log.append(row)
    self.rewards.append(self.reward)
    if len(self.log) % 100000 == 0:
      with open("log2.pick", "wb") as out_file:
        cPickle.dump({"log": self.log, "rewards": self.rewards}, out_file)
  def step(self):
    steer_angle_space = np.linspace(-0.2, 0.2, 21)
    # calculate last reward
    self.reward = self.car_model.position[0] - self.last_position[0]
    # epsilon-greedy
    epsilon = np.random.rand(1)[0]
    #epsilon
    if epsilon < 1e2 or len(self.log) < 5000:
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
          x = [self.velocity[0], self.velocity[1], self.steer_angle]
          q = q_model.predict(x)[0]
          search.append([steer_angle, q])
        search.sort(key=lambda row: row[-1])
        best = search[-1]
        self.steer_angle = best[0]
      except: # corner case for first training
        self.steer_angle = np.random.choice(steer_angle_space)
    # update last_position and logging
    self.last_position = np.array(self.car_model.position)
    self.logging()
    # execute action
    self.car_model.step(self.steer_angle, self.dt)

if __name__ == "__main__":
  position_log = []

  car = Car(1e-2)
  
  plt.ion()
  i = 0
  while True:
    car.step()
    position_log.append(np.array(car.car_model.position))

    if i % 1000 == 0:
      plt.clf()
      plt.plot([p[0] for p in position_log], [p[1] for p in position_log], "k-")
      plt.plot(position_log[-1][0], position_log[-1][1], "k.")
      plt.gca().set_aspect("equal", "datalim")
      plt.title(str(i)+" "+str(np.sum(car.rewards)))

      plt.pause(1e-3)
      plt.draw()
    i = i +1
