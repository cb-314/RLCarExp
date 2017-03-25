import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neighbors import RadiusNeighborsRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import math
import cPickle
import sys

if __name__ == "__main__":
  file_name = "log.pick"
  if ".pick" in sys.argv[1]:
    file_name = sys.argv[1]
  data = {}
  with open(file_name, "rb") as in_file:
    data = cPickle.load(in_file)
  log = np.array(data["log"])
  rewards = np.array(data["rewards"])
 
  scaler = StandardScaler()
  scaler.fit(log)

  knn = RadiusNeighborsRegressor(radius=5e-2, weights="distance")
  knn.fit(scaler.transform(log), rewards)

  va = np.linspace(-np.pi, np.pi, 51)
  sa = np.linspace(-0.2, 0.2, 51)
  q = np.empty((len(va), len(sa)))
  for i, v in enumerate(va):
    for j, s in enumerate(sa):
      q[j,i] = knn.predict(scaler.transform([[v, s]]))

  grad_q = np.gradient(q)

  plt.title("angle vs. steer_angle vs. reward")
  plt.pcolormesh(va, sa, grad_q[0], vmin=-1e-5, vmax=1e-5)
  plt.xlabel("angle")
  plt.ylabel("steerangle")
  plt.colorbar()
  plt.show()
