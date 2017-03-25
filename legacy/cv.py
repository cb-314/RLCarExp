import numpy as np
import matplotlib.pyplot as plt
import cPickle
import sys
import math

import sklearn
from sklearn.model_selection import KFold
from sklearn.preprocessing import MaxAbsScaler 
from sklearn.metrics import mean_squared_error

from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import SGDRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

def cv(model, x, y):
  errors = []
  kf = KFold(n_splits=10, shuffle=True)
  for train_index, test_index in kf.split(x):
    x_train, x_test = x[train_index], x[test_index]
    y_train, y_test = y[train_index], y[test_index]

    x_scaler = MaxAbsScaler()
    y_scaler = MaxAbsScaler()
   
    x_scaler.fit(x_train)
    y_scaler.fit(y_train)

    xx_train = x_scaler.transform(x_train)
    xx_test = x_scaler.transform(x_test)
    yy_train = y_scaler.transform(y_train)
    yy_test = y_scaler.transform(y_test)

    cv_model = sklearn.base.clone(model)
    cv_model.fit(xx_train, yy_train)

    yy_predicted = cv_model.predict(xx_test)

    error = math.sqrt(mean_squared_error(yy_test, yy_predicted))
    errors.append(error)
  return errors

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

  x, y = sklearn.utils.resample(log, rewards, n_samples=100000)

  errors = cv(KNeighborsRegressor(), x, y)
  print "KNN", np.mean(errors), np.std(errors)
  errors = cv(SGDRegressor(), x, y)
  print "SGD", np.mean(errors), np.std(errors)
  errors = cv(RandomForestRegressor(), x, y)
  print "RandomForest", np.mean(errors), np.std(errors)
  errors = cv(GradientBoostingRegressor(), x, y)
  print "GradientBoosting", np.mean(errors), np.std(errors)
