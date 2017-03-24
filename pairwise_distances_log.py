import numpy as np
import matplotlib.pyplot as plt
import cPickle
import sys
import math

import sklearn
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.preprocessing import MaxAbsScaler 

if __name__ == "__main__":
  file_name = "log.pick"
  if ".pick" in sys.argv[1]:
    file_name = sys.argv[1]
  data = {}
  with open(file_name, "rb") as in_file:
    data = cPickle.load(in_file)
  log = np.array(data["log"])
  rewards = np.array(data["rewards"])
  rewards = rewards.reshape(-1, 1)

  x_scaler = MaxAbsScaler()
  x_scaler.fit(log)
  log = x_scaler.transform(log)
  log = log/2.0

  hist = np.array(0, dtype=np.float64)
  bin_edges = np.array(0)
  n_samples = 0.0
  plt.ion()
  for i in range(1000):
    x, y = sklearn.utils.resample(log, rewards, n_samples=10000)
    dists = pairwise_distances(x)
    dists = dists.ravel()
    n_samples = n_samples + len(dists)
    hist_p = np.histogram(dists, bins=100, range=(0.0, 2.0))
    hist = hist + hist_p[0]
    bin_edges = hist_p[1]
    
    plt.clf()
    plt.bar(bin_edges[:-1], hist, width=2.0/100)
    plt.title(n_samples)
    plt.pause(1e-6)
    plt.draw()
  plt.ioff()
  plt.clf()
  plt.bar(bin_edges[:-1], hist, width=2.0/100)
  plt.title(n_samples)
  plt.show()
