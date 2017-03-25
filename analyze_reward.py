import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
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
  
  plt.title("angle vs. steer_angle vs. reward")
  plt.hexbin([p[0] for p in log], [p[1] for p in log], rewards, gridsize=100)
  plt.xlabel("angle")
  plt.ylabel("steerangle")
  plt.colorbar()
  plt.show()
