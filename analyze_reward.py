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
import h5py
import time

if __name__ == "__main__":
  t0 = time.time()
  log = []
  rewards = []
  with h5py.File("log2.hdf5", "r") as f:
    log = f[u"log"][:]
    rewards = f[u"rewards"][:]
  print "file load time", time.time() - t0

  scaler = StandardScaler()
  scaler.fit(log)

  knn = RadiusNeighborsRegressor(radius=5e-2)
  knn.fit(scaler.transform(log), rewards)

  va = np.linspace(-np.pi, np.pi, 101)
  sa = np.linspace(-0.2, 0.2, 101)
  q = np.empty((len(va), len(sa)))
  for i, v in enumerate(va):
    for j, s in enumerate(sa):
      q[j,i] = knn.predict(scaler.transform([[v, s]]))

  grad_q = np.gradient(q)

  plt.suptitle("angle vs. steer_angle vs. reward")
  plt.subplot(121)
  plt.title("0")
  plt.pcolormesh(va, sa, grad_q[0], vmin=np.percentile(grad_q[0].flatten(), 5), vmax=np.percentile(grad_q[0].flatten(), 95))
  plt.xlabel("angle")
  plt.ylabel("steerangle")
  plt.colorbar()
  plt.subplot(122)
  plt.title("1")
  plt.pcolormesh(va, sa, grad_q[1], vmin=np.percentile(grad_q[1].flatten(), 5), vmax=np.percentile(grad_q[1].flatten(), 95))
  plt.xlabel("angle")
  plt.ylabel("steerangle")
  plt.colorbar()
  plt.show()
