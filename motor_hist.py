import numpy as np
import matplotlib.pyplot as plt
import cPickle
import sys
import math

if __name__ == "__main__":
  file_name = "log.pick"
  if ".pick" in sys.argv[1]:
    file_name = sys.argv[1]
  data = {}
  with open(file_name, "rb") as in_file:
    data = cPickle.load(in_file)
  log = np.array(data["log"])
  rewards = np.array(data["rewards"])

  angle = np.array([math.atan2(p[1], p[0]) for p in log])
  steer_angle = np.array([p[-1] for p in log])

  plt.hexbin(angle, steer_angle, gridsize=20)
  plt.show()
  
